import pandas as pd
import numpy as np
import torch
from sklearn.metrics import roc_auc_score
from opensoundscape.ml.shallow_classifier import quick_fit
import hashlib
import datetime
import getpass


def create_train_sizes(df):
    rows_to_remove_per_iteration = 10
    dataframes_list = {}

    # Start with the original DataFrame as the largest train size
    label = f"train_size_{len(df)}"
    dataframes_list[label] = df.copy()

    # Subsequently remove rows to reduce size
    current_df = df.copy()
    iteration = 1
    while len(current_df) > rows_to_remove_per_iteration * 2:
        # Separate into positive and negative groups
        df_neg = current_df[current_df["present"] == False]
        df_pos = current_df[current_df["present"] == True]

        if len(df_neg) < rows_to_remove_per_iteration or len(df_pos) < rows_to_remove_per_iteration:
            print("Not enough rows to continue sampling.")
            break

        neg_to_remove = df_neg.sample(n=rows_to_remove_per_iteration, random_state=iteration)
        pos_to_remove = df_pos.sample(n=rows_to_remove_per_iteration, random_state=iteration)
        rows_to_remove = pd.concat([neg_to_remove, pos_to_remove])
        current_df = current_df.drop(rows_to_remove.index)

        label = f"train_size_{len(current_df)}"
        dataframes_list[label] = current_df.copy()

        iteration += 1

    return dataframes_list


def process_species_model(species, model_name, audio_dir, results_dir, batch_size, epoch, learning_rate):
    """
    Processes a given species and model by training and evaluating the model.
    """
    train_df = pd.read_csv(f"{audio_dir}/{species}/train_files.csv")
    test_df = pd.read_csv(f"{audio_dir}/{species}/test_files.csv")
    
    if model_name == 'Perch':
        train_df['file'] = train_df['file'].str.replace('data', 'data_5s')
        test_df['file'] = test_df['file'].str.replace('data', 'data_5s')
        pd.set_option('display.max_colwidth', 100)
        print(train_df)
    
    train_df['file'] = train_df['file'].astype(str)
    test_df['file'] = test_df['file'].astype(str)
    train_df.set_index("file", inplace=True)
    test_df.set_index("file", inplace=True)
    
    # Create train sizes
    dataframes_list = create_train_sizes(train_df)
    
    # Load model
    model = torch.hub.load('kitzeslab/bioacoustics-model-zoo', model_name, trust_repo=True)
    model.change_classes(['present'])
    
    results = []
    
    # Iterate through train sizes and train/test
    for train_size, i in dataframes_list.items():
        train = pd.DataFrame(i)
        emb_train = model.embed(train, return_dfs=False, batch_size=batch_size, num_workers=0)
        emb_val = model.embed(test_df, return_dfs=False, batch_size=batch_size, num_workers=0)
        
        quick_fit(model.network, emb_train, train.values, emb_val, test_df.values, steps=1000)
        
        predictions = model.network(torch.tensor(emb_val).float()).detach().numpy()
        score = roc_auc_score(test_df.values, predictions, average=None)
        
        results.append({'train_size': train_size, model_name: score})
    
    # Train size 0
    emb_val0 = model.embed(test_df, return_dfs=False, batch_size=batch_size, num_workers=0)
    predictions0 = model.network(torch.tensor(emb_val0).float()).detach().numpy()
    score0 = roc_auc_score(test_df.values, predictions0, average=None)
    results.append({'train_size': 'train_size_0', model_name: score0})
    
    # Generate unique hash
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    username = getpass.getuser()
    unique_hash = hashlib.md5(f"{timestamp}_{username}".encode()).hexdigest()[:8]
    
    results_df = pd.DataFrame(results)
    results_df.to_csv(f"{results_dir}/{species}-{model_name}-{batch_size}-{epoch}-{learning_rate}.csv", index=False)


def run_training(species_list, model_list, audio_dir, results_dir, batch_size, epoch, learning_rate):
    """
    Runs the training process for multiple species and models.
    """
    for species in species_list:
        for model_name in model_list:
            process_species_model(species, model_name, audio_dir, results_dir, batch_size, epoch, learning_rate)
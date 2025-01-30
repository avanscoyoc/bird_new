import pandas as pd

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
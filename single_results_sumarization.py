import os
import pandas as pd
import subprocess
import argparse


# 定义 main 函数
def main(root_dir):
    # First loop: Process each subdirectory and create individual summary files
    for subdir in os.listdir(root_dir):
        subdir_path = os.path.join(root_dir, subdir)

        if os.path.isdir(subdir_path):
            # Construct the output file name for the summary file, saving directly in root_dir
            output_file = f"Summary.csv"

            # Run eval.py for the current subdirectory
            print(f"Running eval.py for {subdir}...")
            try:
                subprocess.run(
                    ["python", "eval.py", "--root", subdir_path, "--output_file", output_file],
                    check=True
                )
                print(f"Successfully ran eval.py for {subdir}")
            except subprocess.CalledProcessError as e:
                print(f"Error running eval.py for {subdir}: {e}")

    # Walk through second-level directories to find .csv files
    for root, dirs, files in os.walk(root_dir):
        # Only process subdirectories one level deep
        if os.path.relpath(root, root_dir).count(os.sep) == 0:
            for file in files:
                if file.endswith(".csv") and not file.startswith("mean_std_"):  # Skip already processed files
                    input_file_path = os.path.join(root, file)
                    output_file_path = os.path.join(root, f"mean_std_{file}")

                    # Process the CSV file
                    try:
                        # Read the CSV file
                        df = pd.read_csv(input_file_path)

                        # Group by 'cdr' and compute mean and std
                        grouped = df.groupby('cdr')[['rmsd', 'seqid', 'dG_gen', 'dG_ref', 'ddG', 'hydro', 'pred_ddg']]
                        mean_df = grouped.mean()
                        std_df = grouped.std()

                        # Combine mean and std into one DataFrame with the format mean ± std
                        result_df = mean_df.copy()
                        for col in mean_df.columns:
                            result_df[col] = mean_df[col].round(3).astype(str) + " ± " + std_df[col].round(3).astype(str)

                        # Save the processed DataFrame to a new CSV (overwrite if exists)
                        result_df.to_csv(output_file_path, index=True)

                        print(f"Processed and saved mean ± std values for: {input_file_path} -> {output_file_path}")
                    except Exception as e:
                        print(f"Failed to process file {input_file_path}: {e}")


    # List to hold data from all Summary files
    all_data = []

    # Walk through second-level directories to find .csv files
    for root, dirs, files in os.walk(root_dir):
        # Only process subdirectories one level deep
        if os.path.relpath(root, root_dir).count(os.sep) == 0:
            for file in files:
                if file.startswith("Summary") and file.endswith(".csv"):
                    summary_file_path = os.path.join(root, file)
                    try:
                        # Read each Summary file into a DataFrame
                        df = pd.read_csv(summary_file_path)
                        all_data.append(df)
                        print(f"Loaded {summary_file_path}")
                    except Exception as e:
                        print(f"Error loading {summary_file_path}: {e}")

    # Merge all DataFrames into one
    if all_data:
        merged_df = pd.concat(all_data, ignore_index=True)

        # Save the merged data to all_summary.csv in the root directory
        all_summary_file = os.path.join(root_dir, "all_summary.csv")
        merged_df.to_csv(all_summary_file, index=False)
        print(f"All summary files merged into {all_summary_file}")

        # Group by 'cdr' and compute mean and std
        grouped = merged_df.groupby('cdr')[['seqid', 'rmsd', 'hydro', 'pred_ddg']]
        mean_df = grouped.mean()
        std_df = grouped.std()
        # Compute the proportion of values < 0 for 'hydro' and 'pred_ddg'
        proportion_neg = merged_df.groupby('cdr')[['hydro', 'pred_ddg']].apply(lambda x: (x < 0).sum() / len(x))


        # Combine mean and std into one DataFrame with the format mean ± std
        result_df = mean_df.copy()
        for col in mean_df.columns:
            result_df[col] = mean_df[col].round(3).astype(str) + " ± " + std_df[col].round(3).astype(str)

        # Add the proportion of negative values to the result DataFrame
        result_df['hydro_neg%'] = (proportion_neg['hydro'] * 100).round(2).astype(str)
        result_df['pred_ddg_neg%'] = (proportion_neg['pred_ddg'] * 100).round(2).astype(str)
        
        # Save mean_std_summary.csv with the computed mean ± std values
        mean_std_summary_file = os.path.join(root_dir, "mean_std_summary.csv")
        result_df.to_csv(mean_std_summary_file, index=True)
        print(f"Mean ± std summary saved to {mean_std_summary_file}")
    else:
        print("No Summary files found to merge.")



if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="Process subdirectories and generate summary files.")
    parser.add_argument("--root_dir", type=str, default="/data/yuangang/AD/antibody-diffusion-properties/results/examples/codesign_single_ddg_and_hydro_partial_0.5_Normalize_Normalize/7DK2_AB_C.pdb")
    # Parse arguments
    args = parser.parse_args()

    # Call the main function with the user-provided root_dir
    main(args.root_dir)
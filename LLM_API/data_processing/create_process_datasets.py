import logging
import os

import pandas as pd
from datasets import Dataset, DatasetDict
from instruct_datasets import Llama3InstructDataset
from huggingface_hub import login

# Constants
model_id = "meta-llama/Meta-Llama-3-8B-Instruct"  # ID for the model
access_token = "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"  # Hugging Face access token
login(token=access_token)  # Log in to Hugging Face hub with access token

# Column names to remove and rename in the dataset
REMOVE_COLUMNS = ["source", "focus_area"]
RENAME_COLUMNS = {"question": "input", "out": "output"}
INSTRUCTION = "Answer the question truthfully"  # Instruction for the dataset
# List of dataset paths
DATASETS_PATHS = [
    "/home/akhil/Downloads/prism/LLM_API/LLM-Medical-Finetuning/data/raw_data/output_file.csv"
]

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def process_dataset(dataset_path: str, model: str) -> pd.DataFrame:
    """
    Process the instruct dataset to be in the format required by the model.
    
    :param dataset_path: The path to the dataset.
    :param model: The model to process the dataset for.
    :return: The processed dataset as a pandas DataFrame.
    """
    logger.info(f"Processing dataset: {dataset_path} for {model} instruct model.")

    dataset = Llama3InstructDataset(dataset_path)  # Load dataset using a custom class
    dataset.drop_columns(REMOVE_COLUMNS)  # Remove unnecessary columns
    logger.info("Columns removed!")
    dataset.rename_columns(RENAME_COLUMNS)  # Rename columns to match the model requirements
    logger.info("Columns renamed!")
    dataset.create_instruction(INSTRUCTION)  # Add an instruction column
    logger.info("Instructions created!")
    dataset.drop_bad_rows(["input", "output"])  # Drop rows with missing input/output
    logger.info("Bad rows dropped!")
    dataset.create_prompt()  # Create a prompt column
    logger.info("Prompt column created!")
    return dataset.get_dataset()  # Return the processed dataset


def create_dataset_hf(dataset: pd.DataFrame) -> DatasetDict:
    """
    Create a Hugging Face dataset from the pandas dataframe.
    
    :param dataset: The pandas dataframe.
    :return: The Hugging Face dataset.
    """
    dataset.reset_index(drop=True, inplace=True)  # Reset index of the DataFrame
    return DatasetDict({"train": Dataset.from_pandas(dataset)})  # Convert to Hugging Face DatasetDict


if __name__ == "__main__":
    # Main script execution
    processed_data_path = "/home/akhil/Downloads/prism/LLM_API/LLM-Medical-Finetuning/data/processed_data"
    os.makedirs(processed_data_path, exist_ok=True)  # Create directory for processed data

    llama3_datasets = []
    for dataset_path in DATASETS_PATHS:
        dataset_name = dataset_path.split(os.sep)[-1].split(".")[0]  # Extract dataset name

        llama3_dataset = process_dataset(dataset_path, "llama3")  # Process the dataset

        llama3_datasets.append(llama3_dataset)  # Append processed dataset to list

        llama3_dataset = create_dataset_hf(llama3_dataset)  # Convert to Hugging Face dataset

        llama3_dataset.push_to_hub(f"llama3_{dataset_name}_instruct_dataset")  # Push dataset to Hugging Face hub

    llama3_dataset = pd.concat(llama3_datasets, ignore_index=True)  # Concatenate all processed datasets

    llama3_dataset = create_dataset_hf(llama3_dataset)  # Convert to Hugging Face dataset

    llama3_dataset.save_to_disk(
        os.path.join(processed_data_path, "llama3_instruct_dataset")
    )  # Save dataset to disk

    llama3_dataset.push_to_hub("llama3_instruct_dataset")  # Push dataset to Hugging Face hub

    # Create a short version of the dataset for quick testing or other purposes
    llama3_dataset_short = pd.concat(llama3_datasets, ignore_index=True)

    llama3_dataset_short = pd.concat(
        [llama3_dataset_short.iloc[:1000], llama3_dataset_short.iloc[-5000:-4000]],
        ignore_index=True,
    )  # Select specific rows for the short dataset
    llama3_dataset_short = create_dataset_hf(llama3_dataset_short)  # Convert to Hugging Face dataset
    llama3_dataset_short.save_to_disk(
        os.path.join(processed_data_path, "llama3_instruct_dataset_short")
    )  # Save short dataset to disk
    llama3_dataset_short.push_to_hub("llama3_instruct_dataset_short")  # Push short dataset to Hugging Face hub

import json
import streamlit as st
import torch
from datasets import load_dataset
from huggingface_hub import login
from transformers import TrainingArguments
from trl import SFTTrainer
from unsloth import FastLanguageModel

# Streamlit app title and description
st.title("Model Fine-tuning and Inference")
st.write("""
This Streamlit app allows you to fine-tune a language model and perform inference with the fine-tuned model.
""")

# User inputs for configuration
hugging_face_username = st.text_input("Hugging Face Username", "Anony0324")
base_model = st.text_input("Base Model", "unsloth/llama-3-8b-Instruct-bnb-4bit")
finetuned_model_info = st.text_input("Finetuned Model Info", "finetuned_model")
dataset_info = st.text_input("Dataset Info", "huggingface/dataset")
max_seq_length = st.number_input("Max Sequence Length", value=3000)
batch_size = st.number_input("Batch Size", value=2)
gradient_accumulation_steps = st.number_input("Gradient Accumulation Steps", value=4)
num_train_epochs = st.number_input("Number of Training Epochs", value=1)
learning_rate = st.number_input("Learning Rate", value=2e-4, format="%e")
hugging_face_token = st.text_input("Hugging Face Token", type="password")

# Login to Hugging Face
if hugging_face_token:
    login(token=hugging_face_token)
    st.success("Logged in to Hugging Face successfully")

@st.cache_resource
def load_model(base_model, max_seq_length, dtype, load_in_4bit):
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=base_model,
        max_seq_length=max_seq_length,
        dtype=dtype,
        load_in_4bit=load_in_4bit,
    )
    return model, tokenizer

@st.cache_resource
def get_peft_model(_model, r, target_modules, lora_alpha, lora_dropout, bias, use_gradient_checkpointing, use_rslora, use_dora, loftq_config):
    model = FastLanguageModel.get_peft_model(
        _model,
        r=r,
        target_modules=target_modules,
        lora_alpha=lora_alpha,
        lora_dropout=lora_dropout,
        bias=bias,
        use_gradient_checkpointing=use_gradient_checkpointing,
        random_state=42,
        use_rslora=use_rslora,
        use_dora=use_dora,
        loftq_config=loftq_config,
    )
    return model

@st.cache_resource
def load_dataset_train(dataset_info):
    dataset_train = load_dataset(dataset_info, split="train")
    return dataset_train

@st.cache_resource
def setup_trainer(_model, _tokenizer, _dataset_train, _training_args, _dataset_text_field, _max_seq_length):
    trainer = SFTTrainer(
        model=_model,
        tokenizer=_tokenizer,
        train_dataset=_dataset_train,
        dataset_text_field=_dataset_text_field,
        max_seq_length=_max_seq_length,
        dataset_num_proc=2,
        packing=False,
        args=_training_args,
    )
    return trainer

# Configuration for the model, LoRA, and training
config = {
    "hugging_face_username": hugging_face_username,
    "model_config": {
        "base_model": base_model,
        "finetuned_model": finetuned_model_info,
        "max_seq_length": max_seq_length,
        "dtype": torch.float16,
        "load_in_4bit": True,
    },
    "lora_config": {
        "r": 16,
        "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj",
                           "gate_proj", "up_proj", "down_proj"],
        "lora_alpha": 16,
        "lora_dropout": 0,
        "bias": "none",
        "use_gradient_checkpointing": True,
        "use_rslora": False,
        "use_dora": False,
        "loftq_config": None
    },
    "training_dataset": {
        "name": dataset_info,
        "split": "train",
        "input_field": "prompt",
    },
    "training_config": {
        "per_device_train_batch_size": batch_size,
        "gradient_accumulation_steps": gradient_accumulation_steps,
        "warmup_steps": 5,
        "max_steps": 0,
        "num_train_epochs": num_train_epochs,
        "learning_rate": learning_rate,
        "fp16": not torch.cuda.is_bf16_supported(),
        "bf16": torch.cuda.is_bf16_supported(),
        "logging_steps": 1,
        "optim": "adamw_8bit",
        "weight_decay": 0.01,
        "lr_scheduler_type": "linear",
        "seed": 42,
        "output_dir": "outputs",
    }
}

if st.button("Train Model"):
    with st.spinner("Loading model and tokenizer..."):
        model, tokenizer = load_model(
            config["model_config"]["base_model"],
            config["model_config"]["max_seq_length"],
            config["model_config"]["dtype"],
            config["model_config"]["load_in_4bit"]
        )

    with st.spinner("Setting up PEFT model..."):
        model = get_peft_model(
            model,
            r=config["lora_config"]["r"],
            target_modules=config["lora_config"]["target_modules"],
            lora_alpha=config["lora_config"]["lora_alpha"],
            lora_dropout=config["lora_config"]["lora_dropout"],
            bias=config["lora_config"]["bias"],
            use_gradient_checkpointing=config["lora_config"]["use_gradient_checkpointing"],
            use_rslora=config["lora_config"]["use_rslora"],
            use_dora=config["lora_config"]["use_dora"],
            loftq_config=config["lora_config"]["loftq_config"],
        )

    with st.spinner("Loading dataset..."):
        dataset_train = load_dataset_train(config["training_dataset"]["name"])

    with st.spinner("Setting up trainer..."):
        training_args = TrainingArguments(
            per_device_train_batch_size=config["training_config"]["per_device_train_batch_size"],
            gradient_accumulation_steps=config["training_config"]["gradient_accumulation_steps"],
            warmup_steps=config["training_config"]["warmup_steps"],
            max_steps=config["training_config"]["max_steps"],
            num_train_epochs=config["training_config"]["num_train_epochs"],
            learning_rate=config["training_config"]["learning_rate"],
            fp16=config["training_config"]["fp16"],
            bf16=config["training_config"]["bf16"],
            logging_steps=config["training_config"]["logging_steps"],
            optim=config["training_config"]["optim"],
            weight_decay=config["training_config"]["weight_decay"],
            lr_scheduler_type=config["training_config"]["lr_scheduler_type"],
            seed=config["training_config"]["seed"],
            output_dir=config["training_config"]["output_dir"],
        )

        trainer = setup_trainer(
            model,
            tokenizer,
            dataset_train,
            training_args,
            config["training_dataset"]["input_field"],
            config["model_config"]["max_seq_length"]
        )

    with st.spinner("Training the model..."):
        trainer.train()

    st.success("Model training complete!")

    with st.spinner("Saving the model..."):
        model.save_pretrained(config["model_config"]["finetuned_model"])
        model.push_to_hub(config["model_config"]["finetuned_model"], tokenizer=tokenizer)

    st.success("Model saved and pushed to Hugging Face Hub!")

if st.button("Generate Sample Inference"):
    with st.spinner("Loading fine-tuned model..."):
        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name=config["model_config"]["finetuned_model"],
            max_seq_length=config["model_config"]["max_seq_length"],
            dtype=config["model_config"]["dtype"],
            load_in_4bit=config["model_config"]["load_in_4bit"],
        )

    with st.spinner("Running inference..."):
        FastLanguageModel.for_inference(model)
        inputs = tokenizer(
            ["system Answer the question truthfully. user This is the question: Do you know about samsung galaxy"],
            return_tensors="pt"
        ).to("cuda")
        outputs = model.generate(**inputs, max_new_tokens=256, use_cache=True)
        result = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        st.write("Inference Result: ", result)

    st.success("Inference complete!")

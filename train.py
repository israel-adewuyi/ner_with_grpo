import os
import re
import time
import torch
import pandas as pd

from typing import Tuple
from dotenv import load_dotenv
from trl import GRPOConfig, GRPOTrainer
from datasets import load_dataset, Dataset
from data_loading import load_conll_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer
from rewards import (
        soft_format_reward_func,
        positive_entity_correctness_reward_func,
        negative_entity_correctness_reward_func,
        correctness_reward_func
)

load_dotenv()

class TrainingArgs:
    model_name: str = "Qwen/Qwen2.5-1.5B-Instruct"
    data_path: str = "data/conll03/mrc-ner.train"
    dataset: str = "conll"

def load_model(model_name: str) -> Tuple[AutoModelForCausalLM, AutoTokenizer]:
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    return model, tokenizer

def get_run_output_name(model_name: str, demo: bool) -> Tuple[str, str]:
    if not demo:
        output_dir=f"ckpts/{model_name.split('/')[-1]}-{time.strftime('%Y-%m-%d %H:%M:%S')}-sysprompt_3"
        run_name = f"{model_name.split('/')[-1]}-{time.strftime('%Y-%m-%d %H:%M:%S')}-sysprompt_3"
    else:
        output_dir=f"ckpts/demo_{model_name.split('/')[-1]}-{time.strftime('%Y-%m-%d %H:%M:%S')}-sysprompt_3"
        run_name = f"demo_{model_name.split('/')[-1]}-{time.strftime('%Y-%m-%d %H:%M:%S')}-sysprompt_3"
    return output_dir, run_name

if __name__ == "__main__":
    args = TrainingArgs()

    model, tokenizer = load_model(args.model_name)

    if args.dataset == "conll":
        data = load_conll_dataset(args.data_path)
    else:
        raise ValueError(f"{args.dataset} dataset is not recognized")
    
    output_dir, run_name = get_run_output_name(args.model_name, False)
    
    training_args = GRPOConfig(
        output_dir=output_dir,
        run_name=run_name,
        learning_rate=5e-6,
        adam_beta1 = 0.9,
        adam_beta2 = 0.99,
        weight_decay = 0.1,
        warmup_ratio = 0.1,
        lr_scheduler_type='cosine',
        logging_steps=1,
        bf16=True,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        num_generations=8,
        max_prompt_length=2048,
        max_completion_length=2048,
        num_train_epochs=4,
        save_strategy="epoch",
        max_grad_norm=0.1,
        report_to="wandb",
        log_on_each_node=False,
    )
    
    trainer = GRPOTrainer(
        model=model,
        processing_class = tokenizer,
        reward_funcs=[
            soft_format_reward_func,
            positive_entity_correctness_reward_func,
            negative_entity_correctness_reward_func,
            correctness_reward_func
        ],
        args=training_args,
        train_dataset=data,
    )
    
    trainer.train()
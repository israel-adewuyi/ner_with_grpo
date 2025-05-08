import os
import re
import pandas as pd
from typing import List, Tuple
from vllm import LLM, SamplingParams
from data_loading import load_conll_dataset

def extract_entities_from_xml(text: str) -> List[str]:
    """
    Extract entities from <entity> tags in the given text.
    Args:
        text: String containing XML with <entity> tags
    Returns:
        List of entities found (empty list if none found)
    """
    entity_matches = re.findall(r'<entity>(.*?)</entity>', text, re.DOTALL)
    
    if not entity_matches:
        return []
    
    entities_str = entity_matches[-1].strip()
    
    if not entities_str:
        return []
        
    entities = [e.strip() for e in entities_str.split(',') if e.strip()]
    return entities

def predict_entities(model: LLM, dataset: pd.DataFrame) -> List[List[str]]:
    """Predict entities for a dataset using vLLM for generation
    
    Args:
        model: Initialized vLLM model
        dataset: Dataset containing columns titled 'prompt' and 'answer'
        
    Returns:
        Tuple of (predictions, ground_truths) where:
        - predictions: List of predicted entity lists
        - ground_truths: List of ground truth entity lists
    """
    no_entities_count = 0
    prompts = [example['prompt'][0]['content'] for example in dataset]
    
    sampling_params = SamplingParams(
        temperature=0.0,
        top_p=0.8,
        max_tokens=2048,
        stop=["</entity>"],
        include_stop_str_in_output=True,
        n=1,
        seed=42
    )

    outputs = model.generate(prompts, sampling_params)
    predictions = []
    ground_truths = []
    
    for idx, output in enumerate(outputs):
        gt_text = dataset[idx]['answer']
        gt_entities = extract_entities_from_xml(gt_text)
        ground_truths.append(gt_entities)
        
        generated_texts = [out.text for out in output.outputs]

        for text in generated_texts:
            try:
                entities = extract_entities_from_xml(text)
                predictions.append(entities)
            except Exception as e:
                no_entities_count += 1
                predictions.append([])
                print(f"Error extracting entities: {e}")
                continue
    print(f"Out of {len(prompts)}, {no_entities_count} were unsuccessful")
    return predictions, ground_truths

def evaluate_predictions(predictions, ground_truths):
    """Calculate precision, recall and F1 score"""
    tp = fp = fn = 0
    
    for pred, gt in zip(predictions, ground_truths):
        pred_set = set(pred)
        gt_set = set(gt)
        
        tp += len(pred_set & gt_set)
        fp += len(pred_set - gt_set)
        fn += len(gt_set - pred_set)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'true_positives': tp,
        'false_positives': fp,
        'false_negatives': fn
    }
    

if __name__ == "__main__":
    model_path = "Qwen/Qwen2.5-1.5B-Instruct"  
    llm = LLM(
        model=model_path, 
        tensor_parallel_size=1,
        device="auto",
        max_model_len=2048,
        seed=42,
        gpu_memory_utilization=0.6,
        enforce_eager=True,
    )

    test_df = load_conll_dataset("data/conll03/mrc-ner.test", include_examples=True)
    print(f"There are {len(test_df)} rows in my dataset")

    f1_scores, num_generations = 0.0, 16
    
    for itr in range(num_generations):
        predictions, ground_truths = predict_entities(llm, test_df)
        metrics = evaluate_predictions(predictions, ground_truths)
        print(f"F1 result at iteration {itr} is {metrics['f1']}")
        f1_scores += metrics['f1']
        
    avg_f1_scores = f1_scores / num_generations
    print(f"Evaluation Metrics (F1): {avg_f1_scores}")

    results_df = pd.DataFrame({
        'f1': [avg_f1_scores],
    })
    
    results_df.to_csv(f"results/{model_path.split('/')[-1]}.csv", index=False)
    print("Predictions saved to results/conll03_entity_predictions.csv")
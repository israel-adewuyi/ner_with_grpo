import re
import os

from typing import List


def soft_format_reward_func(completions, **kwargs) -> list[float]:
    """Reward function that checks if the completion has a specific format."""
    pattern = r"<think>.*?</think>\s*<entity>.*?</entity>"
    responses = [completion[0]["content"] for completion in completions]
    matches = [re.match(pattern, r, flags=re.DOTALL) for r in responses] 
    return [0.5 if match else 0.0 for match in matches]

def extract_xml_answer(text: str) -> str:
    answer = text.split("<think>")[-1]
    answer = answer.split("</think>")[-1]
    return answer.strip()

def correctness_reward_func(prompts, completions, answer, **kwargs) -> list[float]:
    """Checks if the generation of the model exactly matches the ground truth"""
    responses = [completion[0]['content'] for completion in completions]
    q = prompts[0][-1]['content']
    extracted_responses = [extract_xml_answer(r) for r in responses]

    # ---------- LOGS -----------------------------
    debug_content = (
        f"\n{'-'*20}"
        f"\nQuestion:\n{q}"
        f"\nAnswer:\n{answer[0]}"
        f"\nResponse:\n{responses[0]}"
        f"\nExtracted:\n{extracted_responses[0]}\n"
    )
    
    file_path = f"logs/qwen2.5B-1.5_experiment3.txt"

    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            pass 
    
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(debug_content)
    rewards = [2.0 if r == str(a) else 0.0 for r, a in zip(extracted_responses, answer)]
    return rewards

def positive_entity_score_func(answer_entity_list: List[str], out_entity_list: List[str]) -> float:
    """Assigns 0.5 to correct entities included in the list of entities"""
    score = 0.0

    for entity in answer_entity_list:
        score += 0.5 if entity in out_entity_list else 0.0

    return score

def negative_entity_score_func(answer_entity_list: List[str], out_entity_list: List[str]) -> float:
    """Penalizes entities in the generation that are not in the ground truth"""
    score = 0.0

    for entity in out_entity_list:
        if entity not in answer_entity_list:
            score -= 0.5 

    return score

def extract_entity_contents(input_string: str) -> List[str]:
    """
    Extracts all content within <entity> and </entity> tags from the input string,
    then splits the content by commas and strips whitespace from each item.
    
    Args:
        input_string (str): The input string containing entity tags.
    
    Returns:
        list: A list of words split by commas from within the entity tags.
              Returns an empty list if the entity content is empty.
    """
    pattern = r"<entity>(.*?)</entity>"
    matches = re.findall(pattern, input_string)
    
    if not matches:
        return []  
    all_content = "".join(matches)
    
    words = [word.strip() for word in all_content.split(",") if word.strip()]
    
    return words


def positive_entity_correctness_reward_func(prompts, completions, answer, **kwargs) -> List[float]:
    responses = [completion[0]['content'] for completion in completions]
    extracted_responses = [extract_xml_answer(r) for r in responses]

    result = [positive_entity_score_func(extract_entity_contents(ans), extract_entity_contents(res)) for ans, res in zip(answer, extracted_responses)]
    return result

def negative_entity_correctness_reward_func(prompts, completions, answer, **kwargs) -> List[float]:
    responses = [completion[0]['content'] for completion in completions]
    extracted_responses = [extract_xml_answer(r) for r in responses]

    result = [negative_entity_score_func(extract_entity_contents(ans), extract_entity_contents(res)) for ans, res in zip(answer, extracted_responses)]
    return result
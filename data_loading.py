import json
import pandas as pd
from datasets import Dataset
from utils import ENTITY_EXAMPLES

SYSTEM_PROMPT = """
A conversation between User and Assistant. The User provides a string of words. The task of the Assistant is to identify all the {entity_label} entities 
in the given string and return the entities surrounded by an entity tag.
DESCRIPTION: {query}

The Assistant should reason about the entity class and each string/word in the given query and which of the words might belong to the class. 
It would also be important to pay attention to the context.

The reasoning process should be enclosed within <think> </think> tags, and the relevant words should be enclosed within <entity> </entity> tags.
i.e <think> reasoning process here </think> <entity> comma separated list of words that are locations</entity>

If none of the words match the entity type, simply return the entity tag with nothing in between.
If multiple words match the entity type, return them, separated by a comma, in the entity tag.

{example}

User: {context}
Assistant: 
"""

EVAL_SYSTEM_PROMPT = """
A conversation between User and Assistant. The User provides a string of words. The task of the Assistant is to identify all the {entity_label} entities 
in the given string and return the entities surrounded by an entity tag.
DESCRIPTION: {query}

The Assistant should reason about the entity class and each string/word in the given query and which of the words might belong to the class. 
It would also be important to pay attention to the context.

The reasoning process should be enclosed within <think> </think> tags, and the relevant words should be enclosed within <entity> </entity> tags.
i.e <think> reasoning process here </think> <entity> comma separated list of words that are locations</entity>

If none of the words match the entity type, simply return the entity tag with nothing in between.
If multiple words match the entity type, return them, separated by a comma, in the entity tag.

User: {context}
Assistant: 
"""

def load_conll_dataset(file_path: str, num_proc: int = 1, include_examples: bool = True) -> Dataset:
    """
        Loads the CoNLL-2003 dataset by instantiating the MRC_NER class and formatting the
        data to the desired input format. 

        Args:
            file_path (str): the local file path of the CoNLL dataset
            include_examples (bool): if to include few-shot examples or not. 
                If set to false, then the eval prompt is loaded and returned.

        Returns:
            A dataset.Dataset object
    """
    data = MRC_NER(file_path, True, False).get_dataset()
    
    def process_example(example):
        example_prompt = ENTITY_EXAMPLES.get(
            example["entity"]
        )

        if include_examples:
            return {
                'prompt': [
                    {'role': 'user', 'content': SYSTEM_PROMPT.format(
                        entity_label=example["entity"],
                        query=example["query"],
                        context=example["context"],
                        example=example_prompt
                    )}
                ],
                'answer': example['labels']
            }
        else:
            return {
                'prompt': [
                    {'role': 'user', 'content': EVAL_SYSTEM_PROMPT.format(
                        entity_label=example["entity"],
                        query=example["query"],
                        context=example["context"],
                    )}
                ],
                'answer': example['labels']
            }
    return data.map(
        process_example,
        num_proc=num_proc,
    )

class MRC_NER:
    """
        This class loads the dataset from local and formats it in a way that's 
        suitable for feeding transformers.

        Heavily modified but took some inspiration from https://github.com/ShannonAI/mrc-for-flat-nested-ner/blob/master/datasets/mrc_ner_dataset.py
    """
    def __init__(self, file_path: str, possible_only: bool, string_mode: bool):
        self.file_path = file_path
        self.possible_only = possible_only
        self.string_mode = string_mode
        
        self.all_data = json.load(open(file_path, encoding="utf-8"))
        if possible_only:
            self.all_data = [
                x for x in self.all_data if x["start_position"]
            ]

        self.label_to_str  = {
            "PER": "Person",
            "LOC": "Location",
            "ORG": "Organization",
            "MISC": "Miscellaneous"
        }

        self._post_process()

    def _post_process(self, ):
        self.processed_data = []
        for item in self.all_data:
            label = item["context"]
            entities = []
            
            for pos in item["span_position"]:
                start, end = pos.split(";")
                words = label.split(" ")
                temp_entity = words[int(start) : int(end) + 1]
                words[int(start)] = "<entity>" + words[int(start)]
                words[int(end)] = words[int(end)] + "</entity>" 
                label = " ".join(words)
                entities.append(" ".join(temp_entity))

            if not self.string_mode:
                label = " , ".join(entities)
                label = "<entity>" + label + "</entity>"

            entry = {
                "context": item["context"],
                "entity": self.label_to_str[item["entity_label"]],
                "query": item["query"],
                "labels": label
            }
            self.processed_data.append(entry)

        print(f"All {len(self.processed_data)} has been processed")
        self.dataset = Dataset.from_pandas(pd.DataFrame(self.processed_data))
        print(f"Converted {len(self.dataset)} entries to Dataset.")

    def get_dataset(self, ):
        return self.dataset
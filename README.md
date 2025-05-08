# Reinforcement Learning meets NER
Implementation accompanying the [https://israel-adewuyi.github.io/blog/2025/ner_with_rl/](blogpost)

## Repository structure
`utils.py` - Few shot examples from Deepseek, for each entity in CoNLL-2003
`train.py` - training pipeline
`rewards.py` - verifiers to assign rewards to generations from the model
`eval.py` - script to exaluate the model
`data/conll` - dataset downloaded from [https://github.com/ShannonAI/mrc-for-flat-nested-ner](here)

### Template .env file
```
CUDA_VISIBLE_DEVICES=cuda_device_id
WANDB_API_KEY=your_api_key
WANDB_PROJECT=your_project_name
```

## To run
- Clone the repo and cd into it
- Create virtual env activate it
- Install packages with `pip install > requirements.txt`
- Run `python train.py`

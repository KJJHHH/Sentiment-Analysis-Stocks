# Sentiment Analysis for Stocks
## Introduction
## Data 
## From Pretrained Model
### Data
### Models
- FinBert
    - Model Name: ~ 
    - Can Process data with tokens less than 512.
    - The pretrained model is finetuned from Bert model.
- FinGPT
    - Model Name: ~
    - The Models need permission to download. 
    - [Download Website](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf). 
    - The permission only last for 24 hours, after that need to apply again
    - Based on Llama, GPU is required: Not feasible now, build in Colab the ram will explode.
- Longformer
    - Model Name: ~ 
    - Can Process data with tokens up to 4096
    - Not finetuned to do financial tasks; some parameters (weights) cannot be downloaded successfully 
### Decide Scores
### Finetuning Pretrained Models
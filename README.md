# Text classification using BERT and spaCy

## Prerequisites

The project was created and tested on "Ubuntu Server 22.04.2 LTS". Other operating systems should be very similar. Some things differ on Windows.

### Default
1. Python3 (theoretically >= 3.8 for PyTorch 2.0; tested with Python3.10.6)
1. Good internet connection with enough traffic for the first run

### If you want to use GPU
additionally:
1. NVIDIA GPU with >= 6 GB of VRAM (ideally >=12 GB)
1. Installed NVIDIA GPU driver

### Using GPU over Docker
Attention: 
Using GPU over Docker is already a very sophisticated deployment. It requires you to ackquire some knowledge in this area.

additionally:
1. Installed `nvidia-container-runtime` package (https://github.com/NVIDIA/nvidia-container-runtime#installation)

## Installation

1. Clone repository from GitHub `git clone git@github.com:yevgenpapernyk/spacy_bert_classification_example.git`
1. Optional: Update pip, setuptools and wheel `pip install -U pip setuptools wheel`
1. Install requirements `pip install -Ur requirements.txt`

## Run
### Load dataset, train and evaluate
1. `source venv/bin/activate` to activate virtual environment
1. Update var `gpu_option` to `"--gpu-id 0"` in `project.yml` if you do not want to use a GPU
1. `python -m spacy project run train_and_eval` 

## How a similar project can be created

1. Create project directory and go inside `mkdir spacy_bert_example && cd spacy_bert_example`
1. Create virtual environment and activate it `python3 -m venv venv && source venv/bin/activate`. Works on Linux and Mac. Has to be done slightly different on Windows.
1. Optional: Update pip, setuptools and wheel `pip install -U pip setuptools wheel`
1. Install requirements `pip install -U spacy[cuda-autodetect,transformers,lookups]` (more possiblities at https://spacy.io/usage).
1. Go to https://spacy.io/usage/training#quickstart
1. Select
  - Language: German  *(alternatively: Multi-language --> more flexible, but lower score)*
  - Components: textcat  *(text classification)*
  - Text Classification: exclusive categories  *(if only one category is valid - eclusive label classification; multi-label clasification is used otherwise)*
  - Hardware: GPU (transformer)  *(not using BERT otherwise)*
  - Optimize for: efficiency  *(efficiency ist faster then accuracy, but it results in lower score)*
1. Click on copy button at the button of the config area
1. Create `config` directory
1. Create `config/base_config.cfg` file and paste the config into it
1. Run `python -m spacy init fill-config config/base_config.cfg config.cfg` to create the final verbose config which is then use by spaCy for training
1. Create a spacy `project.yml` file similar to that one in this repository


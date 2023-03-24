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

### Using GPU with Docker
Attention: 
Using GPU with Docker is already a very sophisticated deployment. It requires you to acquire some knowledge in this area.

additionally:
1. Installed `nvidia-container-toolkit`
    - https://gitlab.com/nvidia/container-toolkit/container-toolkit/
    - https://gitlab.com/nvidia/container-toolkit/container-toolkit/-/tree/main/cmd/nvidia-container-runtime

## Installation for training and local deployment

1. Clone repository from GitHub `git clone https://github.com/yevgenpapernyk/spacy_bert_classification_example.git`
1. Optional: Update pip, setuptools and wheel `pip install -U pip setuptools wheel`
1. Install requirements 
    - using CPU: `pip install -Ur requirements.txt`
    - using GPU: `pip install -Ur requirements_gpu.txt`

## Run
### Load dataset, train and evaluate
1. `source venv/bin/activate` to activate virtual environment
1. Update var `gpu_option` to `"--gpu-id 0"` in `project.yml` if you want to use a GPU
1. `spacy project run train_and_eval` 

### Deploy after training
#### Local deployment without Docker
`spacy project run deploy_local`

#### Deploy with docker (without GPU)
`docker compose up -d`

#### Deploy with docker and GPU
Please check the "Prerequisites" section to make sure everything is done properly to run a docker container with GPU support.
`docker compose -f docker-compose.gpu.yml up -d`

Watch logs with `docker compose -f docker-compose.gpu.yml logs -f` to make sure that the api uses the GPU.

## Use
After deploying the api using one described possibilities you can acess it by using on of the following urls in your browser:
- `http://localhost/bert-api/docs`: Swagger docs. You can also acess the different methods using the Swagger GUI.
- `http://localhost/bert-api/`: Get basic information about the deploment.
- `http://localhost/bert-api/classify-text?text=Some%20Text`: Classify a to one of the specified categories text using BERT. This is the essence of the whole project :)

## Directory structure
### Repository
- `project.yml`: A spaCy project file. It plays a central role in holding everthing together (non docker things). More info: https://spacy.io/usage/projects/
- `scripts/`: Scripts used by `project.yml`
    - `api.py`: FastAPI that uses the model and generates Swagger docs. Used by `project.yml` and by `Dockerfile`s
    - `load_data.py`: Used by `project.yml` to load, split and convert the data to `*.spacy` files.
- `config/`: 
    - `config.cfg`: Describes the training settings. 
    - `base_config.cfg`: The only purpose is to be basis for generating `config.cfg`. It is not used for further tasks.
- requirements
    - `requirements.txt`: Used to install python libs if no NVIDIA GPU is used.
    - `requirements_gpu.txt`: Used to install python libs if a NVIDIA GPU is used.
- `docker/`: Dockerfiles and nginx config

### Generated during the run of the spaCy project workflow
- `corpus/`: Loaded data
    - `train.spacy`: Training data. Directly used to train the model.
    - `dev.spacy`: Development data. Used to check model performance during the training to determine the best model and store to `model-best`.
    - `test.spacy`: Test data. A hould out set. Used to calculate the test score to determine how the model could perform in production.
- `models/`:
    - `model-best`: Best model of the last training run. Has the best score and should perform best.
    - `model-last`: Last model of the last training run. Just the last deep learning epoch. Should perform worse than `model-best`.
- `metrics/`: Evaluated metrics / scores of the `model-best`
    - `train.json`: Metrics using `train.spacy` data.
    - `dev.json`: Metrics using `dev.spacy` data.
    - `test.json`: Metrics using `test.spacy` data.

## How a similar project can be created

1. Create project directory and go inside `mkdir spacy_bert_example && cd spacy_bert_example`
1. Create virtual environment and activate it `python3 -m venv venv && source venv/bin/activate`. Works on Linux and Mac. Has to be done slightly different on Windows.
1. Optional: Update pip, setuptools and wheel `pip install -U pip setuptools wheel`
1. Install requirements (more possiblities at https://spacy.io/usage):
    - using CPU: `pip install -U spacy[transformers,lookups]`
    - using GPU: `pip install -U spacy[cuda-autodetect,transformers,lookups]`
1. Go to https://spacy.io/usage/training#quickstart
1. Select
    - **Language**: German  *(alternatively: Multi-language --> more flexible, but lower score)*
    - **Components**: textcat  *(text classification)*
    - **Text Classification**: exclusive categories  *(if only one category is valid - eclusive label classification; multi-label clasification is used otherwise)*
    - **Hardware**: GPU (transformer)  *(not using BERT otherwise)*
    - **Optimize for**: efficiency  *(efficiency ist faster then accuracy, but it results in lower score)*
1. Click on copy button at the button of the config area
1. Create `config` directory
1. Create `config/base_config.cfg` file and paste the config into it
1. Run `spacy init fill-config config/base_config.cfg config.cfg` to create the final verbose config which is then use by spaCy for training
1. Create a spacy `project.yml` file similar to that one in this repository


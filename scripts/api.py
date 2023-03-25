import asyncio
import os
import logging
import re
from pathlib import Path

import spacy
from fastapi import FastAPI
from fastapi.logger import logger


# logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# create api
app = FastAPI(
    title='BERT Text Classification API',
    root_path=os.getenv('FASTAPI_ROOT_PATH', ''),
)

# gpu
logger.info('Checking GPU')
is_gpu_in_use = spacy.prefer_gpu()
if is_gpu_in_use:
    logger.info('-> Using GPU')
else:
    logger.warning('-> GPU ist not used!')

# load model
logger.info('Loading model')
model_path = Path() / 'model'
logger.info(f'Model path: {model_path.resolve()}')
try:
    model = spacy.load(model_path)
except OSError:
    logger.error('Could not load model!')
    exit(1)


@app.get("/")
async def info():
    """Provide some basic information"""
    return {
       'name': app.title,
       'version': app.version,
       'is_gpu_in_use': is_gpu_in_use,
    }


@app.get('/classify-text/')
async def classify_text(text: str):
    # get predictions and sort by score descending
    doc = model(text)
    predictions = sorted(doc.cats.items(), key=lambda x: x[1], reverse=True)

    # create response
    best_label, best_score = predictions[0]
    result = {
        'text': text,
        'label': best_label,
        'score': best_score,
    }
    all_predictions = []
    for label, score in predictions:
        pred = {
            'label': label,
            'score': score,
        }
        all_predictions.append(pred)
    result['all_predictions'] = all_predictions

    return result


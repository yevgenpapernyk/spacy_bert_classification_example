FROM python:3.10-slim

ENV TZ="Europe/Berlin"

WORKDIR /app

# models volume
RUN mkdir models
VOLUME /app/models

# install packages
COPY requirements.txt ./
RUN sed -i 's/spacy.*/spacy[transformers,lookups]/g' requirements.txt
RUN pip install -r requirements.txt

# create user
ARG username=api
RUN useradd -m -s /bin/bash $username

# copy files and set permissions
COPY scripts/api.py .

# set user
USER $username

ENTRYPOINT python -m uvicorn api:app --host 0.0.0.0


from pathlib import Path

import spacy
from datasets import load_dataset
from sklearn.model_selection import train_test_split


class DataLoader:
    def __init__(self, language):
        self._train_p = Path() / 'train.spacy'
        self._dev_p = Path() / 'dev.spacy'
        self._test_p = Path() / 'test.spacy'
        self._nlp = spacy.blank(language)

    def load(self, dataset_name):
        print('Loading dataset')

        # load
        print(f'  └─> Loading "{dataset_name}" from huggingface datasets')
        dataset = load_dataset(dataset_name)

        # split
        train_data = dataset['train']
        test_data = dataset['test']

        # write to spacy docs
        #classes = self._find_all_classes(train_data)
        print(f'  └─> Found classes: {train_data.features["label"].names}')
        self._convert_and_store_docs(train_data, self._train_p)
        self._convert_and_store_docs(test_data, self._dev_p)
        # TODO: use test and dev sets correctly
        
        print(f'  └─> finished!')

    def _convert_and_store_docs(self, data, corpus_p):
        doc_bin = spacy.tokens.DocBin()

        # iterate over samples and convert to docs
        for sample in data:
            label_idx = sample['label']
            label = data.features['label'].int2str(label_idx)
            doc = self._create_doc(sample['text'], label, all_labels=data.features['label'].names)
            doc_bin.add(doc)

        # write docs to file
        print(f'  └─> {corpus_p}: {len(doc_bin)}')
        doc_bin.to_disk(corpus_p)
    
    def _create_doc(self, text, label, all_labels):
        # convert text
        doc = self._nlp(text)

        # set labels/categories (1.0 for true label; 0.0 for other)
        doc.cats = {l: float(l == label) for l in all_labels}
        
        return doc


if __name__ == '__main__':
    loader = DataLoader('de')
    loader.load('gnad10')


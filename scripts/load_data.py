from pathlib import Path

import spacy
from datasets import load_dataset


class DataLoader:
    def __init__(self, language):
        # paths
        corpus_dir = Path() / 'corpus'
        self._train_p = corpus_dir / 'train.spacy'
        self._dev_p = corpus_dir / 'dev.spacy'
        self._test_p = corpus_dir / 'test.spacy'
 
        # spacy
        self._nlp = spacy.blank(language)

    def load(self, dataset_name):
        print('Loading dataset')

        # load
        print(f'  └─> Loading "{dataset_name}" from huggingface datasets')
        dataset = load_dataset(dataset_name)

        # shuffle and split train and dev data
        temp_data = dataset['train'].shuffle(seed=42)
        dev_frac = 0.1
        n_train_samples = int(dev_frac * temp_data.num_rows)
        dev_data = temp_data.select(range(n_train_samples))
        train_data = temp_data.select(range(n_train_samples, temp_data.num_rows))

        # get test data
        test_data = dataset['test']

        # write to spacy docs
        #classes = self._find_all_classes(train_data)
        print(f'  └─> Found classes: {train_data.features["label"].names}')
        self._convert_and_store_docs(train_data, self._train_p)
        self._convert_and_store_docs(dev_data, self._dev_p)
        self._convert_and_store_docs(test_data, self._test_p)
        
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


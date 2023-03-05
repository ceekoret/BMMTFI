import os
import pandas as pd
import csv
import numpy as np

from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')


def calc_sent_finbert():
    nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer, device=0)

    # sentence_list = df.iloc[:size]['text'].tolist()
    sentence_list = ['Growth is not strong and don"t we have plenty of liquidity.',
                     'Growth is strong and we have plenty of liquidity.',
                     'Growth sucks and liquidity is rubbish.']
    results = nlp(sentence_list)
    print(results)  #LABEL_0: neutral; LABEL_1: positive; LABEL_2: negative

calc_sent_finbert()
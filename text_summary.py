# -- coding: utf-8 --
"""text_summary.ipynb

Automatically generated by Colaboratory.

Original file is located at
https://colab.research.google.com/drive/1nHKYIMGoxCuQPXpLIHNPCo7J6qvm0Vir

# Text summarization - Frequency based algorithm

# Preprocessing the texts
"""

import spacy 
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

# I added the word machine at the end of the last sentence
text = """Artificial intelligence is human like intelligence.
                   It is the study of intelligent artificial agents.
                   Science and engineering to produce intelligent machines.
                   Solve problems and have intelligence.
                   Related to intelligent behavior.
                   Developing of reasoning machines.
                   Learn from mistakes and successes.
                   Artificial intelligence is related to reasoning in everyday situations."""
                   
def summarizer(rawdocs):
    try:
        stopwords = list(STOP_WORDS)
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(rawdocs)
        tokens = [token.text for token in doc]
        word_freq = {}
        for word in doc:
            if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
                if word.text not in word_freq.keys():
                    word_freq[word.text] = 1
                else:
                    word_freq[word.text] += 1

        max_freq = max(word_freq.values())

        for word in word_freq.keys():
            word_freq[word] = (word_freq[word] / max_freq)

        sent_tokens = [sent for sent in doc.sents]

        sent_scores = {}
        for sent in sent_tokens:
            for word in sent:
                if word.text in word_freq.keys():
                    if sent not in sent_scores.keys():
                        sent_scores[sent] = word_freq[word.text]
                    else:
                        sent_scores[sent] += word_freq[word.text]

        select_len = int(len(sent_tokens) * 0.3)
        summary = nlargest(select_len, sent_scores, key=sent_scores.get)
        final_summary = [word.text for word in summary]
        summary = ' '.join(final_summary)
        return summary, doc, len(rawdocs.split()), len(summary.split())
    except Exception as e:
        print("Error in summarizer:", e)
        return "Error occurred while summarizing the text.", None, 0, 0

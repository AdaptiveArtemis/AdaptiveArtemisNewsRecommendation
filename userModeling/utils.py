import datetime
import logging
import re

import nltk
import numpy as np
import spacy

from django.utils import timezone
from nltk import word_tokenize, pos_tag
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from users.models import User, NewsLog

logger = logging.getLogger('userModeling')
nlp = spacy.load("en_core_web_sm")

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

POS_SCORE = {
    'NN': 3.0, 'NNS': 3.0, 'NNP': 3.0, 'NNPS': 3.0,   'PRP': 0.1,
    'PRP$': 0.1,
    'JJ': 0.1, 'RB': 0.1,
    'VB': 0.0, 'VBD': 0.0, 'VBG': 0.0, 'VBN': 0.0, 'VBP': 0.0, 'VBZ': 0.0
}

KEYWORD_BOOST = 7
DEC_COEE = 0.7


def compute_weighted_tfidf(text, keywords):
    tokens = word_tokenize(text)
    keyword_tokens = word_tokenize(keywords)
    all_tokens = tokens + keyword_tokens
    tagged_tokens = pos_tag(all_tokens)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([' '.join(all_tokens)])
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray().flatten()

    weighted_scores = {}
    for token, score in zip(feature_names, tfidf_scores):
        for word, pos in tagged_tokens:
            weight = POS_SCORE.get(pos, 1.0) * (KEYWORD_BOOST if word in keyword_tokens else 1)
            weighted_scores[token] = score * weight

    sorted_scores = sorted(weighted_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_scores

def spacy_preprocess(document):
    doc = nlp(document)
    tokens = [
        token.lemma_.strip().lower()  # 小写化和去除空格
        for token in doc
        if not token.is_stop and not token.is_punct and not token.like_num
        and token.is_alpha and len(token.lemma_) > 1  # 确保是字母且长度大于1
    ]
    return " ".join(tokens)


def update_user_prefer_lists2():
    today = timezone.now().date()
    start_of_today = timezone.make_aware(datetime.datetime.combine(today, datetime.time.min))
    end_of_today = timezone.make_aware(datetime.datetime.combine(today, datetime.time.max))
    today_logs = NewsLog.objects.filter(timestamp__range=(start_of_today, end_of_today))

    user_logs = {}
    for log in today_logs:
        user_logs.setdefault(log.user, []).append(log)

    for user, logs in user_logs.items():
        prefer_list = user.preferList if user.preferList else {}
        all_scores = {}
        for log in logs:
            processed_doc = spacy_preprocess(log.body)
            keywords_text = ' '.join(log.keywords1)
            weighted_scores = compute_weighted_tfidf(processed_doc, keywords_text)

            for keyword, score in weighted_scores:
                if keyword in all_scores:
                    all_scores[keyword] += score
                else:
                    all_scores[keyword] = score

        top_keywords = sorted(all_scores.items(), key=lambda item: item[1], reverse=True)[:15]

        for keyword, score in top_keywords:
            if keyword in prefer_list:
                prefer_list[keyword] += score
            else:
                prefer_list[keyword] = score

        user.preferList = prefer_list
        user.save()

        print(f"Updated preferList for user {user.username}: {user.preferList}")

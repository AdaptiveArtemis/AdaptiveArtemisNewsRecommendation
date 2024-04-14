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
    'NN': 3.0, 'NNS': 3.0, 'NNP': 3.0, 'NNPS': 3.0,
    'JJ': 0.2, 'RB': 0.2, 'VB': 0.2, 'VBD': 0.2,
    'VBG': 0.2, 'VBN': 0.2, 'VBP': 0.2, 'VBZ': 0.2
}

KEYWORD_BOOST = 5
DEC_COEE = 0.7

# def auto_dec_refresh(users):
#     for user in users:
#         if hasattr(user, 'preferList') and user.preferList:
#             new_pref_list = {}
#             # 对每个关键词应用衰减系数
#             for keyword, score in user.preferList.items():
#                 new_score = score * DEC_COEE
#                 if new_score >= MIN_SCORE:  # 仅保留分数大于等于10的关键词
#                     new_pref_list[keyword] = new_score
#
#             # 更新用户的喜好列表
#             user.preferList = new_pref_list
#             user.save()  # 保存更新


def compute_weighted_tfidf(text, keywords, topK=10):
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

    sorted_scores = sorted(weighted_scores.items(), key=lambda x: x[1], reverse=True)[:topK]
    return sorted_scores
# def update_user_prefer_lists():
#     today = timezone.now().date()
#     start_of_today = timezone.make_aware(datetime.datetime.combine(today, datetime.time.min))
#     end_of_today = timezone.make_aware(datetime.datetime.combine(today, datetime.time.max))
#     today_logs = NewsLog.objects.filter(timestamp__range=(start_of_today, end_of_today))
#
#     user_logs = {}
#     for log in today_logs:
#         user_logs.setdefault(log.user, []).append(log)
#
#     for user, logs in user_logs.items():
#         prefer_list = user.preferList if user.preferList else {}
#         # apply decay to user's prefer list
#         prefer_list = apply_decay_to_user(prefer_list)
#
#         # Prepare the document for TF-IDF calculations
#         documents = [preprocess_document(log.body) for log in logs]
#         logger.info(documents)
#         vectorizer = TfidfVectorizer(max_features=40, token_pattern=r'(?u)\b\w+\b', stop_words='english')
#         tfidf_matrix = vectorizer.fit_transform(documents)
#         logger.info(tfidf_matrix)
#
#         feature_names = vectorizer.get_feature_names_out()
#         avg_scores = tfidf_matrix.mean(axis=0).A1
#         feature_index = dict(zip(feature_names, avg_scores))
#         logger.info(feature_index)
#
#         # Update preferList with new keywords,adding to existing keywords, prefer_list is a dictionary
#         for keyword, score in feature_index.items():
#             if keyword in prefer_list:
#                 prefer_list[keyword] += score
#             else:
#                 prefer_list[keyword] = score
#
#         # Remove keywords with weight less than 0.02
#         min_weight = 0.02
#         prefer_list = {keyword: weight for keyword, weight in prefer_list.items() if weight >= min_weight}
#
#         # Save the updated prefer list, sorting to keep the highest scores first
#         user.preferList = dict(sorted(prefer_list.items(), key=lambda x: x[1], reverse=True))
#         user.save()
#
#         logger.info(f"Updated preferList for user {user.username}: {user.preferList}")


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
        # apply decay to user's prefer list
        # prefer_list = apply_decay_to_user(prefer_list)

        # Prepare the document for TF-IDF calculations
        documents = []
        for log in logs:
            processed_doc = spacy_preprocess(log.body)
            keywords_text = ' '.join(log.keywords1)
            full_text = processed_doc + ' ' + keywords_text
            weighted_scores = compute_weighted_tfidf(processed_doc, keywords_text)

            for keyword, score in weighted_scores:
                if keyword in prefer_list:
                    prefer_list[keyword] += score
                else:
                    prefer_list[keyword] = score

        min_score_threshold = 0.1
        prefer_list = {k: v for k, v in prefer_list.items() if v >= min_score_threshold}

        user.preferList = prefer_list
        user.save()

        print(f"Updated preferList for user {user.username}: {user.preferList}")

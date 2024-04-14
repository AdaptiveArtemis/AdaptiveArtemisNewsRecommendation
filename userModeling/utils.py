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
#     # 名词
#     'NN': 0.3, 'NNS': 0.3, 'NNP': 0.3, 'NNPS': 0.3,
#     # 形容词
#     'JJ': 0.2, 'JJR': 0.2, 'JJS': 0.2,
#     # 动词
#     'VB': 0.1, 'VBD': 0.1, 'VBG': 0.1, 'VBN': 0.1, 'VBP': 0.1, 'VBZ': 0.1,
#     # 副词
#     'RB': 0.1, 'RBR': 0.1, 'RBS': 0.1,
#     # 代词
#     'PRP': 0.05, 'PRP$': 0.05,
#     # 介词
#     'IN': 0.05,
#     # 连词
#     'CC': 0.05,
#     # 冠词
#     'DT': 0.0,
#     # 情态动词
#     'MD': 0.0,
#     # 存在词
#     'EX': 0.0,
#     # 助动词
#     'TO': 0.0,
#     # 物主助词
#     'POS': 0.0,
#     # 个人代词
#     'WP': 0.05, 'WP$': 0.05,
#     # 哪里，何时
#     'WRB': 0.05,
# # 其他（默认）
# 'other':0.05

'NN': 0.25, 'NNS': 0.5,       # 普通名词降低重复率
    'NNP': 2.0, 'NNPS': 2.0,     # 专用名词升高
    'PRP': 0.0,
    'PRP$': 0.0,
    'JJ': 0.1, 'RB': 0.1, 'IN': 0.0, 'DT': 0.0,
    'VB': 0.0, 'VBD': 0.0, 'VBG': 0.0, 'VBN': 0.0, 'VBP': 0.0, 'VBZ': 0.0

}

KEYWORD_BOOST = 10
DEC_COEE = 0.7


def compute_weighted_tfidf(text, keywords):
    tokens = word_tokenize(text)
    keyword_tokens = word_tokenize(keywords)
    logger.info(keyword_tokens)             # print
    all_tokens = tokens + keyword_tokens
    tagged_tokens = pos_tag(all_tokens)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([' '.join(all_tokens)])
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray().flatten()

    weighted_scores = {}
    for token, score in zip(feature_names, tfidf_scores):
        for word, pos in tagged_tokens:
            if token == word:  # 确保只处理当前token对应的词性
                weight = POS_SCORE.get(pos, 1.0)  # 获取词性对应的权重
                if weight == 0 or word == 'people':
                    continue  # 如果权重为0，则忽略这个词，不加入最终得分

                # 检查是否为关键词并应用加成
                initial_weight = weight  # 保存原始权重用于打印
                if word in keyword_tokens:
                    weight *= KEYWORD_BOOST  # 应用关键词加成
                    print(f"Token: {token}, Original Weight: {initial_weight}, Boosted Weight: {weight}")

                # 打印调试信息
                # print(f"Token: {token}, Original Weight: {initial_weight}, Boosted Weight: {weight}")

                calculated_score = score * weight  # 计算加权得分
                if calculated_score != 0:
                    weighted_scores[token] = calculated_score  # 只有得分不为0时才添加到字典

    # 对得分进行排序并取前topK个
    sorted_scores = sorted(weighted_scores.items(), key=lambda x: x[1], reverse=True)[:7]
    return sorted_scores

def spacy_preprocess(document):
    doc = nlp(document)
    tokens = [
        token.lemma_.strip().lower()  # 小写化和去除空格
        for token in doc
        if not token.is_stop and not token.is_punct and not token.like_num
        and token.is_alpha and len(token.lemma_) > 5  # 确保是字母且长度大于1
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

        top_keywords = sorted(all_scores.items(), key=lambda item: item[1], reverse=True)[:3] # 列表显示

        for keyword, score in top_keywords:
            if keyword in prefer_list:
                prefer_list[keyword] += score
            else:
                prefer_list[keyword] = score

        user.preferList = prefer_list
        user.save()

        # print(f"Updated preferList for user {user.username}: {user.preferList}")

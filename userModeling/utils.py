import datetime
import logging
import re

from django.utils import timezone
from sklearn.feature_extraction.text import TfidfVectorizer

from users.models import User, NewsLog

logger = logging.getLogger('userModeling')

def apply_decay_to_user(preferList, decay=0.8):
    """preferlist: list of tuples (keyword, weight)"""
    return {keyword: weight * decay for keyword, weight in preferList.items()}

def preprocess_document(document):
    document = re.sub(r'\s+', ' ', document)
    return document

def update_user_prefer_lists():
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
        prefer_list = apply_decay_to_user(prefer_list)

        # Prepare the document for TF-IDF calculations
        documents = [preprocess_document(log.body) for log in logs]
        vectorizer = TfidfVectorizer(max_features=40, token_pattern=r'(?u)\b\w+\b')
        tfidf_matrix = vectorizer.fit_transform(documents)
        logger.info(tfidf_matrix)

        feature_names = vectorizer.get_feature_names_out()
        avg_scores = tfidf_matrix.mean(axis=0).A1
        feature_index = dict(zip(feature_names, avg_scores))
        logger.info(feature_index)

        # Update preferList with new keywords,adding to existing keywords, prefer_list is a dictionary
        for keyword, score in feature_index.items():
            if keyword in prefer_list:
                prefer_list[keyword] += score
            else:
                prefer_list[keyword] = score

        # Remove keywords with weight less than 0.02
        min_weight = 0.02
        prefer_list = {keyword: weight for keyword, weight in prefer_list.items() if weight >= min_weight}

        # Save the updated prefer list, sorting to keep the highest scores first
        user.preferList = dict(sorted(prefer_list.items(), key=lambda x: x[1], reverse=True))
        user.save()

        logger.info(f"Updated preferList for user {user.username}: {user.preferList}")

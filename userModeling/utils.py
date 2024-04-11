import datetime
import json
import logging

from django.utils import timezone
from sklearn.feature_extraction.text import TfidfVectorizer

from users.models import User, NewsLog

def apply_decay_to_user(preferList, decay=0.8):
    """preferlist: list of tuples (keyword, weight)"""
    return {keyword: weight * decay for keyword, weight in preferList.items()}

def update_user_prefer_lists():
    today = timezone.now().date()
    # yesterday = today - timezone.timedelta(days=1)
    # start_of_yesterday = datetime.datetime.combine(yesterday, datetime.time.min)
    # end_of_yesterday = datetime.datetime.combine(yesterday, datetime.time.max)
    start_of_today = timezone.make_aware(datetime.datetime.combine(today, datetime.time.min))
    end_of_today = timezone.make_aware(datetime.datetime.combine(today, datetime.time.max))
    today_logs = NewsLog.objects.filter(timestamp__range=(start_of_today, end_of_today))
    # yesterday_logs = NewsLog.objects.filter(timestamp__range=(start_of_yesterday, end_of_yesterday))

    user_logs = {}
    for log in today_logs:
        user_logs.setdefault(log.user, []).append(log)

    for user, logs in user_logs.items():
        prefer_list = user.preferList if user.preferList else {}
        # apply decay to user's prefer list
        prefer_list = apply_decay_to_user(prefer_list)

        # Prepare the document for TF-IDF calculations
        documents = [log.body for log in logs]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(documents)
        feature_names = vectorizer.get_feature_names_out()
        feature_index = {name: index for index, name in enumerate(feature_names)}

        for log in logs:
            doc_keywords = log.keywords.split(',') if log.keywords else []

            for keyword in doc_keywords:
                keyword = keyword.strip()
                if keyword in feature_index:
                    keyword_index = feature_index[keyword]
                    doc_index = documents.index(log.body)
                    keyword_weight = tfidf_matrix[doc_index, keyword_index]
                    prefer_list[keyword] = prefer_list.get(keyword, 0) + keyword_weight
        # Iterate over each document and update the list of preferences
        # for doc_index, document in enumerate(documents):
        #     doc_keywords = logs.keywords.split(',') if logs.keywords else []
        #     for keyword in doc_keywords:
        #         keyword = keyword.strip()
        #         if keyword in feature_index:
        #             keyword_index = feature_index[keyword]
        #             keyword_weight = tfidf_matrix[doc_index, keyword_index]
        #             prefer_list[keyword] = prefer_list.get(keyword, 0) + keyword_weight

        # Make sure to keep only the top 5 weighted keywords
        prefer_list = dict(sorted(prefer_list.items(), key=lambda x: x[1], reverse=True)[:15])

        # Save the updated prefer list
        user.preferList = prefer_list
        user.save()

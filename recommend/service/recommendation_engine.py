import json
import torch
import numpy as np
from datetime import datetime, timedelta
from transformers import BertModel, BertTokenizer
from sklearn.metrics.pairwise import cosine_similarity

from users.models import User
from news.models import Article

class EmbeddingRecommender():

    def __init__(self, username):
        self.model = BertModel.from_pretrained('bert-base-uncased')
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.articles = self.retrieve_recent_articles()
        self.user = User.objects.get(username=username)

    # Function to get BERT embeddings for a text
    def get_bert_embeddings(self, text):
        inputs = self.tokenizer(text, return_tensors='pt')
        outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()
        return embeddings

    def get_weighted_bert_embeddings(self, tags, weights):
        weighted_embeddings = []
        for tag, weight in zip(tags, weights):
            tag_embedding = self.get_bert_embeddings(tag)
            weighted_embedding = tag_embedding * weight
            weighted_embeddings.append(weighted_embedding)
        return sum(weighted_embeddings)

    def keyword_intersection(self, article_keywords, user_keywords):

        # article_keywords = set([x.strip().lower() for x in article_keywords.split(",")])
        article_keywords = set(article_keywords)
        print(article_keywords)
        user_keywords = set([x.strip().lower() for x in user_keywords.keys()])
        print(user_keywords)
        return list(article_keywords.intersection(user_keywords))
    
    def get_most_relevant_keyword(self, article):

        article_keywords = article.keywords1
        user_prefer_list = self.user.preferList

        most_relevant_keywords = self.keyword_intersection(article_keywords, user_prefer_list)
        if len(most_relevant_keywords) > 0:
            return most_relevant_keywords[0]

        # TODO: The following code is very slow. Find a faster alternative
        # max_similarity = -1
        # most_relevant_keyword = None
        # for keyword in user_prefer_list.keys():
        #     keyword_embedding = self.get_bert_embeddings(keyword)

        #     # Calculate the cosine similarity between the keyword and each of the article's keywords
        #     for article_keyword in article_keywords.split(","):
        #         article_keyword_embedding = self.get_bert_embeddings(article_keyword)
        #         similarity = cosine_similarity(keyword_embedding, article_keyword_embedding)[0][0]

        #         # If this similarity is higher than the current max_similarity, update max_similarity and most_relevant_keyword
        #         if similarity > max_similarity:
        #             max_similarity = similarity
        #             most_relevant_keyword = keyword

        # return most_relevant_keyword if max_similarity > 0.9 else None
    
    def generate_recommendations(self, num_recommendations=5):
        # Retrieve user keyword tags and weights
        user_tags_dict = self.user.preferList
        user_tags = [tag for tag in user_tags_dict.keys()]
        user_weights = [weight for weight in user_tags_dict.values()]

        # Get BERT embeddings for user tags and article tags
        user_tags_embeddings = self.get_weighted_bert_embeddings(user_tags, user_weights)

        # Get article keyword tags and generate embeddings
        articles_used = []
        article_embeddings = []
        for article in self.articles:
            try:
                article_tags = ' '.join(article.keywords1)
                if not article_tags:
                    continue
                article_embedding = self.get_bert_embeddings(article_tags)
                article_embeddings.append(article_embedding)
                articles_used.append(article)
            except Exception as e:
                print(f"Error processing article: {article.title}, {str(e)}")

        # Calculate cosine similarity between user tags and article tags
        similarities = [
            cosine_similarity(user_tags_embeddings, article_embedding)[0][0] for article_embedding in article_embeddings
        ]

        # Get top n articles with highest similarity
        sorted_article_indices = np.argsort(similarities)
        top_article_indices = sorted_article_indices[-num_recommendations:]
        top_articles = []
        for index in top_article_indices:
            print(index)
            index = int(index)
            curr_article = articles_used[index]
            print(curr_article)
            most_relevant_keyword = self.get_most_relevant_keyword(curr_article)
            print(most_relevant_keyword)
            top_articles.append({
                "title": curr_article.title,
                "subtitle": curr_article.description,
                "link": curr_article.link,
                "relevant_keyword": most_relevant_keyword if most_relevant_keyword else None,
            })
        return top_articles
    
    def retrieve_recent_articles(self):
        # Retrieve articles with a pub_date within the last 2 days
        recent_articles = Article.objects.filter(timestamp__gte=datetime.now() - timedelta(days=2))
        return recent_articles

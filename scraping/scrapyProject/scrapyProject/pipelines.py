# Handle items and save data to database

import django
import os
import sys
import datetime
from scrapy.exceptions import DropItem
from asgiref.sync import sync_to_async

# 1)Configuring Environment Variables (items_pipeline add the setting)
sys.path.append(os.path.dirname(os.path.abspath('.')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'AdaptiveArtemisNewsRecommendation.settings'
django.setup()

# 2)Import your Django model
from news.models import Article

class ScrapyprojectPipeline:
    # Process the item and save it to the database
    # Use sync_to_async to wrap your database calls to run in an asynchronous environment
    async def process_item(self, item, spider):
        try:
            # Convert date format from string to datetime object
            pub_date = datetime.datetime.strptime(item['pubDate'], '%a, %d %b %Y %H:%M:%S %z')
            # Save to Django model using sync_to_async to make it compatible with async context
            await sync_to_async(self.save_article, thread_sensitive=True)(
                item,
                pub_date
            )
            return item
        except Exception as e:
            raise DropItem(f"Error saving article: {e}")

    # Helper function to save the article in a synchronous context
    def save_article(self, item, pub_date):
        # Update or create the article
        article, created = Article.objects.update_or_create(
            link=item['link'],
            defaults={
                'title': item['title'],
                'description': item['description'],
                'pub_date': pub_date,
                'image': item['image'],
                'keywords1': item.get('keywords', ''),
                'robots': item.get('robots', ''),
                'author': item.get('author', ''),
                'category': item.get('category', ''),
                'body': item.get('body', ''),
            }
        )
        if created:
            print(f'Article created: {article.title}')



    # Use sync_to_sync to wrap your database calls to run in an asynchronous environment
    # def process_item(self, item, spider):
    #     try:
    #         # 2.1)Converting date formats
    #         item['pubDate'] = datetime.datetime.strptime(item['pubDate'], '%a, %d %b %Y %H:%M:%S %z')
    #
    #         # 2.2)Create a new Article object
    #         article, created = Article.objects.update_or_create(
    #             link=item['link'],
    #             defaults=item
    #         )
    #         if created:
    #             print(f'Article created: {article.title}')
    #         return item
    #
    #     except Exception as e:
    #         raise DropItem(f"Error saving article: {e}")

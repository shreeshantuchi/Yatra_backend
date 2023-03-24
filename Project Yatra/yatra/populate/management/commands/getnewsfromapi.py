import requests
import json
from django.core.management.base import BaseCommand
from NewsandInfo.models import News

class Command(BaseCommand):
    help = 'Fetches news from News API and saves it to the database.'

    def handle(self, *args, **options):
        News.objects.all().delete()

        url="http://eventregistry.org/api/v1/article/getArticles"

        body={
        "locationUri":"https://en.wikipedia.org/wiki/Nepal",
        "lang":"eng",
        "categoryUri": ["dmoz/Recreation",
                        "dmoz/Arts",
                        "dmoz/Buisness/Hospitality",
                        "dmoz/Buisness/Environment",
                        "dmoz/Regional/Asia/Nepal/Travel_and_Tourism",
                        "dmoz/Regional/Asia/Nepal/Transportation"],
        "apiKey": "af1fcecc-78fb-4c63-85f9-bed098ee0ff1",
        "articlesSoryBy":["rel","date"],
        "hasDuplicateFilter":"skipDuplicates",
        "isDuplicateFilter":"skipDuplicates"
        }

        response=requests.get(url,json=body)

        if response.status_code == 200:
            m_news = response.json()
        else:
            self.stdout.write(self.style.ERROR('Error fetching news from API'))

    
    # Save the data into the model
        for result in m_news["articles"]["results"]:
            topic = result["title"]
            source_name = result["source"]['title']
            source_link = result["url"]
            image_url = result["image"]
            date = result["date"]

            self.stdout.write(self.style.SUCCESS('Creating news "{}"'.format(topic)))
            News.objects.create(
                topic=topic,
                source_link=source_link,
                source_name=source_name,
                image_url=image_url,
                description=result["body"],
                date=date
            )
        
        self.stdout.write(self.style.SUCCESS('News creation completed successfully.'))

        print("total results = ",m_news["articles"]["totalResults"])
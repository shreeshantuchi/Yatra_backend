import pandas as pd
from django.core.management.base import BaseCommand
from Food.models import Food

class Command(BaseCommand):
    help='import booms'


    def add_arguments(self, parser):
        pass
    
    def handle(self, *args, **options):
        df=pd.read_csv('datafood.csv')
        #Name,Average_price,Latitude,Longitude,keywords,phone_no,Review
        for NAME,AVGP,LAT,LON,KEY,PHONE,RVW in zip(df.Name,df.Average_price,df.Latitude,df.Longitude,df.keywords,df.phone_no,df.Review):
            models=Food(name=NAME,average_price=AVGP,phone_no=PHONE,latitude=LAT,longitude=LON,related_keywords=RVW)
            models.save()
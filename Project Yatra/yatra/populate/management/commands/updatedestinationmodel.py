import pandas as pd
from django.core.management.base import BaseCommand
from Destination.models import Destination

class Command(BaseCommand):
    help='import booms'


    def add_arguments(self, parser):
        pass
    
    def handle(self, *args, **options):
        df=pd.read_csv('Destinationdata.csv')
        #Name,Latitude,Longitude,Location,Description,is_area,average_price,realted_keywords,Ratings
        for NAME,LAT,LON,LOC,DES,ISA,AVGP,KEY,RATE in zip(df.Name,df.Latitude,df.Longitude,df.Location,df.Description,df.is_area,df.average_price,df.realted_keywords,df.Ratings):
            models=Destination(name=NAME,average_price=AVGP,description=DES,is_area=ISA,latitude=LAT,longitude=LON,related_keywords=KEY)
            models.save()
            
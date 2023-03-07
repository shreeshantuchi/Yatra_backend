import pandas as pd
from django.core.management.base import BaseCommand
from accounts.models import PoliceStation

class Command(BaseCommand):
    help='import booms'


    def add_arguments(self, parser):
        pass
    
    def handle(self, *args, **options):
        df=pd.read_csv('policestation.csv')
        for NAME,PHONE,LAT,LON in zip(df.name,df.phone,df.lat,df.lon):
            models=PoliceStation(name=NAME,phone_no=PHONE,latitude=LAT,longitude=LON)
            models.save()
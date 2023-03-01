import pandas as pd
from django.core.management.base import BaseCommand
from accounts.models import Country

class Command(BaseCommand):
    help='import booms'


    def add_arguments(self, parser):
        pass
    
    def handle(self, *args, **options):
        df=pd.read_csv('combined.csv')
        for NAME,FLAG_URL,SNAME in zip(df.Name,df.Flag,df.Code):
            models=Country(name=NAME,flag_url=FLAG_URL,short_name=SNAME)
            models.save()
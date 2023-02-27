import pandas as pd
from django.core.management.base import BaseCommand
from accounts.models import Country

class Command(BaseCommand):
    help='import booms'


    def add_arguments(self, parser):
        pass
    
    def handle(self, *args, **options):
        df=pd.read_csv('countries.csv')
        for NAME,SNAME in zip(df.Name,df.Code):
            models=Country(name=NAME,short_name=SNAME)
            models.save()
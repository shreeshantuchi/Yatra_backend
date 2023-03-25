from django.db import models
from django.contrib.contenttypes.fields import ContentType
from django.contrib.contenttypes.fields import GenericRelation


import os
from django.core.exceptions import ValidationError
from django.db.models import Q
import time
from geopy.geocoders import Nominatim

from reverse_geocoding import ReverseGeocoder


geolocator = Nominatim(user_agent="YATRA")

class Destination(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_area = models.BooleanField(default=False)
    average_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    related_keywords = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=15,null=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=15,null=True)
    location= models.CharField(max_length=255,blank=True,null=True)
    favorite_by=models.ManyToManyField('accounts.Yatri',related_name='favorite_destination',blank=True,default=None)

    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.location:
            time.sleep(2)
            reverse_gecoder = ReverseGeocoder()
            location_got = reverse_gecoder.get_address(self.latitude, self.longitude)
            self.location = location_got
        super().save(*args, **kwargs)

    
    


class DestinationImage(models.Model):
    def nameFile(instance,filename):
        full_name = f"{instance.destination.name or ''}"
        return f"Destination/{full_name}/{filename}"
     
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=nameFile,blank=True)
    image_url=models.URLField(blank=True)

    def __str__(self):
        return str(self.destination.name+'/'+str(self.id)+'/'+os.path.basename(self.image.name))
    
    class Meta:
        ordering=['destination','id','image']
        constraints = [
            models.CheckConstraint(
                check=Q(image__isnull=False) | Q(image_url__isnull=False),
                name='at_least_one_not_null'
            )
        ]


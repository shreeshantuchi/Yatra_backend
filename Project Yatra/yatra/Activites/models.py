from django.db import models
import os
from multiselectfield import MultiSelectField
from Destination.models import Destination
import time
from reverse_geocoding import ReverseGeocoder


class Activity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type_choices=[
        ('ENT','Entertainment'),
        ('SPT','Sports'),
        ('ADV','Adventure'),
        ('LOC','Local'),
        ('OTH','Others'),

    ]
    type= MultiSelectField(max_length=255,choices=type_choices,default='OTH')
    # images = models.ImageField(upload_to='destination_images/')
    phone_no=models.CharField(max_length=20,null=True,blank=True)
    average_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    related_keywords = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=15,null=True,blank=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=15,null=True,blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='activity', null=True, blank=True)
    location= models.CharField(max_length=255,blank=True,null=True)
    favorite_by=models.ManyToManyField('accounts.Yatri',related_name='favorite_activity',blank=True,default=None)


    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    
    
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.location:
            time.sleep(2)
            reverse_gecoder = ReverseGeocoder()
            if not self.latitude and not self.longitude:
                location_got = reverse_gecoder.get_address(self.destination.latitude,self.destination.longitude)
            else:
                location_got = reverse_gecoder.get_address(self.latitude,self.longitude)
            self.location = location_got
        super().save(*args, **kwargs)
    

class ActivityImage(models.Model):
    def nameFile(instance,filename):
        full_name = f"{instance.activity.name or ''}"
        return f"Destination/{full_name}/{filename}"
     
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=nameFile)


    def __str__(self):
        return str(self.activity.name+'/'+str(self.id)+'/'+os.path.basename(self.image.name))
    
    class Meta:
        ordering=['activity','id','image']
from django.db import models
import os,time
from multiselectfield import MultiSelectField
from Destination.models import Destination
from reverse_geocoding import ReverseGeocoder
from accounts.models import Yatri

class Food(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type_choices=[
        ('LOC', 'Local'),
        ('RST', 'Restaurant'),
        ('CAF', 'Cafe'),
        ('BAK', 'Bakery'),
        ('FTK', 'Food truck'),
        ('OTH','Others'),
        ('CONT','Continental'),
        ('FRN','French'),
        ('ITL','Italian'),
        ('IND','Indian'),
        ('EUR','European'),
        ('BAR','Bar'),
        ('ASN','Asian')
    ]
    type= MultiSelectField(max_length=50,choices=type_choices,default='OTH')
    phone_no=models.CharField(max_length=20,null=True,blank=True)
    average_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ratings = models.DecimalField(max_digits=2, decimal_places=1, default=3.0)
    related_keywords = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=15,null=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=15,null=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='food', null=True, blank=True)
    location= models.CharField(max_length=255,blank=True,null=True)
    favorite_by=models.ManyToManyField(Yatri,related_name='favorite_food',blank=True,default=None)


    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        try:
            if not self.location:
                time.sleep(2)
                reverse_gecoder = ReverseGeocoder()
                if not self.latitude and not self.longitude:
                    location_got = reverse_gecoder.get_address(self.destination.latitude,self.destination.longitude)
                else:
                    location_got = reverse_gecoder.get_address(self.latitude,self.longitude)
                self.location = location_got
                print(location_got)
                print('location saved')
            super().save(*args, **kwargs)
        except:
            pass


class FoodImage(models.Model):
    def nameFile(instance,filename):
        full_name = f"{instance.food.name or ''}"
        return f"Destination/{full_name}/{filename}"
     
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=nameFile)


    def __str__(self):
        return str(self.food.name+'/'+str(self.id)+'/'+os.path.basename(self.image.name))
    
    class Meta:
        ordering=['food','id','image']
from django.db import models
import os
from multiselectfield import MultiSelectField


class Food(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
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
    phone_no=models.CharField(max_length=20,default='XXXXXXXXXX')
    average_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    related_keywords = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,null=True)



    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


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
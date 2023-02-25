from django.db import models
import os

class Activity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    type_choices=[
        ('ENT','Entertainment'),
        ('SPT','Sports'),
        ('ADV','Adventure'),
        ('LOC','Local'),
        ('OTH','Others'),

    ]
    type= models.CharField(max_length=10,choices=type_choices,default='OTH')
    # images = models.ImageField(upload_to='destination_images/')
    phone_no=models.CharField(max_length=20,default='XXXXXXXXXX')
    average_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    related_keywords = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,null=True)



    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    

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
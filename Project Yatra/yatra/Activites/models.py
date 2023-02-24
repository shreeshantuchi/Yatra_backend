from django.db import models

class Activity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    type_choices=[
        ('ENT','Entertainment'),
        ('SPT','Sports'),
        ('ADV','Adventure'),
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
from django.db import models
from accounts.models import Interest

class News(models.Model):
    topic = models.CharField(max_length=100)
    source_name=models.CharField(max_length=200)
    source_link=models.URLField(null=True,blank=True)

    date=models.DateField()
    description = models.TextField()
    interest=models.ManyToManyField(Interest)
   
    # images = models.ImageField(upload_to='destination_images/')
    related_keywords = models.CharField(max_length=255, null=True, blank=True)
  


    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.topic+','+self.source_name+','+str(self.date)


class Info(models.Model):
    topic = models.CharField(max_length=100)
    source_name=models.CharField(max_length=200)
    source_link=models.URLField(null=True,blank=True)

    date=models.DateField()
    description = models.TextField()
    interest=models.ManyToManyField(Interest)
   
    # images = models.ImageField(upload_to='destination_images/')
    related_keywords = models.CharField(max_length=255, null=True, blank=True)
  


    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.topic+','+self.source_name+','+str(self.date)

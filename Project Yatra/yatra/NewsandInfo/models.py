from django.db import models
from accounts.models import Interest
import os

class News(models.Model):
    topic = models.CharField(max_length=100)
    source_name=models.CharField(max_length=200)
    source_link=models.URLField(null=True,blank=True)

    date=models.DateField()
    description = models.TextField()
    interest=models.ManyToManyField(Interest)
   
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
   
    related_keywords = models.CharField(max_length=255, null=True, blank=True)
  


    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.topic+','+self.source_name+','+str(self.date)


class NewsImage(models.Model):
    def nameFile(instance,filename):
        full_name = f"{instance.news.name or ''}"
        return f"Destination/{full_name}/{filename}"
     
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=nameFile)


    def __str__(self):
        return str(self.news.name+'/'+str(self.id)+'/'+os.path.basename(self.image.name))
    
    class Meta:
        ordering=['news','id','image']

class InfoImage(models.Model):
    def nameFile(instance,filename):
        full_name = f"{instance.info.name or ''}"
        return f"Destination/{full_name}/{filename}"
     
    info = models.ForeignKey(Info, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=nameFile)


    def __str__(self):
        return str(self.info.name+'/'+str(self.id)+'/'+os.path.basename(self.image.name))
    
    class Meta:
        ordering=['info','id','image']
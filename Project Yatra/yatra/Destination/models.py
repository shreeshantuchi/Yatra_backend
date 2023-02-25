from django.db import models
import os

class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_city = models.BooleanField(default=False)
    average_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    related_keywords = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,null=True)



    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    


class DestinationImage(models.Model):
    def nameFile(instance,filename):
        full_name = f"{instance.destination.name or ''}"
        return f"Destination/{full_name}/{filename}"
     
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=nameFile)


    def __str__(self):
        return str(self.destination.name+'/'+str(self.id)+'/'+os.path.basename(self.image.name))
    
    class Meta:
        ordering=['destination','id','image']
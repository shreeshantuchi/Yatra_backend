from django.db import models
from datetime import datetime
# from geopy.geocoders import Nominatim
# this geopy  needs to be resesrached further
import requests
from django.core.files import File
import urllib
import os


from django.contrib.auth.models import BaseUserManager, AbstractBaseUser



#Custom user manager class
class UserManager(BaseUserManager):
    def create_user(self, email, password=None,type='Y',password2=None):
        """
        Creates and saves a User with the given email, name, tc and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            type=type
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, name,tc and password.
        """
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user



#Custom User model
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    # name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    type=models.CharField(choices=[('Y','Yatri'),('G','Guide'),('E','Expert')], max_length=10,default='Y')

    created_at=models.DateTimeField(auto_now_add=True)
    Updated_at=models.DateTimeField(auto_now=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

#Interest model
class Interest(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=20,null=True)
    related_keywords=models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.name



#Country model for now the falgs are processed in the fornt end
class Country(models.Model):
    name = models.CharField(max_length=100)
    flag=models.ImageField(upload_to="Countries/", blank=True)
    flag_url=models.URLField(blank=True)
    short_name=models.CharField(max_length=30)

    def __str__(self):
        return self.name

#location model store latitue and lgoitude
#name is reverse gerated from the long and lat
class Location(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    # name = models.CharField(max_length=200, blank=True)
    

    def __str__(self):
        return str([self.longitude,self.latitude])

    # def save(self, *args, **kwargs):
    #     if not self.name:
    #         geolocator = Nominatim(user_agent='myapp')
    #         location = geolocator.reverse(f"{self.latitude}, {self.longitude}")
    #         self.name = location.address
    #     super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(max_length=200)
    short_name=models.CharField(max_length=30)

    def __str__(self):
        return self.name

#this is yartri model or profile for the users
#here the user are modeled as one to one feild
#country are modeled as one o
class Yatri(models.Model):
    def nameFile(instance,filename):
        full_name = f"{instance.first_name or ''}{instance.last_name or ''}"
        return f"yatriimages/{full_name}/{filename}"
    user=models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    profile_image=models.ImageField(null=True,blank=True,upload_to=nameFile)
    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    age = models.PositiveIntegerField(null=True)
    country = models.ForeignKey(Country, blank=True,null=True,on_delete=models.SET_NULL)
    phone_no=models.CharField(max_length=20,null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,blank=True,null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,blank=True,null=True)
    
    interests=models.ManyToManyField(Interest)



    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return str(self.user.email)
    


class SahayatriGuide(models.Model):
    def nameFile(instance,filename):
        full_name = f"{instance.first_name or ''}{instance.last_name or ''}"
        return f"shayatriimages/guide/{full_name}/{filename}"
    user=models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    profile_image=models.ImageField(null=True,blank=True,upload_to=nameFile)

    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    age = models.PositiveIntegerField(null=True,blank=True)
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    phone_no=models.CharField(max_length=20,null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,blank=True,null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,blank=True,null=True)
    
    interests=models.ManyToManyField(Interest)
    bio=models.TextField(max_length=255,null=True)

    average_cost_basis_choices=[
        ('PHr','per hour'),
        ('PDay','per hour'),
        ('PVst','per visit'),
        ('PPrsn','per person'),
    ]
    average_cost = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    
    cost_basis = models.CharField(
        max_length=10,
        choices=average_cost_basis_choices,
        blank=True,
        null=True,
        default=None,
    )
    
    
    #rlationship to destination model
    #ratings implementation

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    # class Meta:
    #     constraints = [
    #         models.CheckConstraint(
    #             check=(
    #                 models.Q(average_cost__isnull=True) |
    #                 models.Q(average_cost__isnull=False, cost_basis__isnull=False)
    #             ),
    #             name='cost_basis_if_average_cost_specified'
    #         )
    #     ]

    
    def __str__(self):
        return str(self.user.email)
    

class SahayatriExpert(models.Model):
    def nameFile(instance,filename):
        full_name = f"{instance.first_name or ''}{instance.last_name or ''}"
        return f"shayatriimages/expert/{full_name}/{filename}"
    user=models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    profile_image=models.ImageField(null=True,blank=True,upload_to=nameFile)
    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    age = models.PositiveIntegerField(null=True,blank=True)
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    phone_no=models.CharField(max_length=20,null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,blank=True,null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,blank=True,null=True)
    
    interests=models.ManyToManyField(Interest,related_name='interest_sahayatri')
    bio=models.TextField(max_length=255,null=True)
    expertise = models.CharField(max_length=200,null=True)
    
    
    average_cost_basis_choices=[
        ('PHr','per hour'),
        ('PSes','per session'),
        ('PProj','per visit'),
        ('PPrsn','per person'),
    ]
    average_cost = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    
    cost_basis = models.CharField(
        max_length=10,
        choices=average_cost_basis_choices,
        blank=True,
        null=True,
        default=None,
    )

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    # class Meta:
    #     constraints = [
    #         models.CheckConstraint(
    #             check=(
    #                 models.Q(average_cost__isnull=True) |
    #                 models.Q(average_cost__isnull=False, cost_basis__isnull=False)
    #             ),
    #             name='cost_basis_if_average_cost_specified'
    #         )
    #     ]
    
    def __str__(self):
        return str(self.user.email)
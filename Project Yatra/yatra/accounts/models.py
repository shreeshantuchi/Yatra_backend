from django.db import models
from datetime import datetime
# from geopy.geocoders import Nominatim
# this geopy  needs to be resesrached further


from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

#Custom user manager class
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, password2=None):
        """
        Creates and saves a User with the given email, name, tc and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
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
    created_at=models.DateTimeField(auto_now_add=True)
    Updated_at=models.DateTimeField(auto_now=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

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
    related_keywords=models.CharField(max_length=50,null=True)
    def __str__(self):
        return self.name


#Country model for now the falgs are processed in the fornt end
class Country(models.Model):
    name = models.CharField(max_length=100)
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
        return [self.longitude,self.latitude]

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
    user=models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    age = models.PositiveIntegerField(null=True)
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    phone_no=models.CharField(max_length=20,null=True)
   
    # location = models.ManyToManyField(Location)    
    interests=models.ManyToManyField(Interest)



    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return str(self.user.email)
    



class SahayatriGuide(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    age = models.PositiveIntegerField(null=True,blank=True)
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
   
    # location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)    
    interests=models.ManyToManyField(Interest)
    bio=models.TextField(max_length=255,null=True)
    average_cost=models.PositiveIntegerField(null=True)

    #rlationship to destination model
    #ratings implementation

    created_at=models.DateTimeField(auto_now_add=True)
    Updated_at=models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return str(self.first_name)
    

class SahayatriExpert(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    age = models.PositiveIntegerField()
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
   
    # location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)    
    interests=models.ManyToManyField(Interest,related_name='interest_sahayatri')
    bio=models.TextField(max_length=255,null=True)
    experties=models.ManyToManyField(Interest)
    average_cost=models.PositiveIntegerField(null=True)

    created_at=models.DateTimeField(auto_now_add=True)
    Updated_at=models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return str(self.first_name)
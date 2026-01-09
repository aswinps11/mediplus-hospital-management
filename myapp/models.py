from django.db import models

# Create your models here.
class UserData(models.Model):
    name=models.CharField(max_length=100,unique=True)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
    
class Doctor(models.Model):
    name=models.CharField(max_length=100)
    specialization= models.CharField(max_length=100)
    email=models.EmailField(max_length=100,unique=True,null=True)
    phone=models.IntegerField(blank=True,null=True)
    address=models.CharField(max_length=200,blank=True,null=True)
    image=models.ImageField(upload_to='doctors/')
    available_daysandtime=models.TextField(blank=True,null=True)
    biography=models.TextField(blank=True,null=True)
    education=models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.name
    
    
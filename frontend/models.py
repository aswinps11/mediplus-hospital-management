from django.db import models
from myapp.models import Doctor

# Create your models here.
class ContactMessage(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=20)
    subject=models.CharField(max_length=100)
    message=models.TextField()
    created_at =models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
class Newsletter(models.Model):
    email=models.EmailField(unique=True)
    subscribed_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Appointment(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=20)
    
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    
    date=models.DateField()
    message=models.TextField(blank=True)
    
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.doctor.name}"
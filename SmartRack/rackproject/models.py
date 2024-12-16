from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phonenumber = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=128)  # Store hashed passwords

    def __str__(self):
        return self.name

class Rack(models.Model):
    STATUS_CHOICES = [
        ('locked', 'Locked'),
        ('unlocked', 'Unlocked'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unlocked')
    address = models.TextField(blank=True, null=True)

class Rack_User(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    rack= models.ForeignKey(Rack, on_delete=models.CASCADE)
    locked_at = models.DateTimeField(auto_now_add=True)

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE)
    locked_at = models.DateTimeField(null=True, blank=True)  
    unlocked_at = models.DateTimeField(null=True, blank=True)
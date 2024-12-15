from django.db import models

# Create your models here.
class User(models.Model):
    user_id= models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phonenumber = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=128)  # Store hashed passwords

    def __str__(self):
        return self.name

class Rack(models.Model):
    rack_id = models.CharField(max_length=50, unique=True)
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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"Profile of {self.user.name}"

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE)
    locked_at = models.DateTimeField()
    unlocked_at = models.DateTimeField(auto_now_add=True)
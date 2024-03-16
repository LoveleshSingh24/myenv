from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    usernmae=models.OneToOneField(User,on_delete=models.CASCADE,null=True) #verbose name
    email_address=models.CharField(max_lenght=55,unique=True,null=True)
    bio = models.TextField(blank=True,null=True)
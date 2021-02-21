from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Crew(models.Model):
    crew_name = models.CharField(max_length=100, null=True, blank=True)
    tag_line = models.CharField(max_length=100, null=True, blank=True)
    netnet = models.CharField(max_length=100, null=True, blank=True)


class Users(models.Model):
    crew_name = models.ForeignKey(Crew, on_delete=models.CASCADE, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    about = models.CharField(max_length=1000, null=True, blank=True)
    netnet = models.CharField(max_length=1000, null=True, blank=True)
    avatar_img = models.FileField(upload_to='pics/', null=True, blank=True)
    affiliation = models.CharField(max_length=1000, null=True, blank=True)
    
    def __str__(self):
        return str(self.username)




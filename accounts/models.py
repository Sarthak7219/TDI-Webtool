from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager




class Profile(AbstractUser):

    username = None
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    profile_pic = models.ImageField(upload_to='images/profile_images', blank=True, null=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    objects = UserManager()

    def __str__(self):
        return self.email
    

from django.contrib.auth import get_user_model
User = get_user_model()


class Report_Excel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='excel_report')
    year = models.IntegerField()
    file = models.FileField(upload_to='user_excel_reports/')


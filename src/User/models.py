from django.db import models
from django.contrib.auth.models import AbstractUser

from profileEmp.models import profile

class nUser(AbstractUser):
    birthdate =models.DateField(null=True)
    CIN = models.CharField(max_length=10)
    phone =models.CharField(max_length=15,blank=True)
    is_admin=models.BooleanField(default=False)
    profile=models.OneToOneField(profile, on_delete=models.CASCADE,blank=True,null=True,related_name="emp")
    admin =models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True)
    
    
    REQUIRED_FIELDS=['email','first_name','CIN','last_name','birthdate','phone','admin']


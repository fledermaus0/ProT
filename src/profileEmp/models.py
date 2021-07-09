from django.db import models

class profile(models.Model):
    id_p=models.AutoField(primary_key=True)
    image = models.CharField(max_length=250,blank=True,null=True)
    CV= models.CharField(max_length=250,blank=True,null=True)
    domaine= models.CharField(max_length=50)
    XP=models.PositiveIntegerField(default=0)
    sal=models.FloatField("salary",null=True,help_text="the salary in $")
    

class achievment(models.Model):
    profile=models.OneToOneField('profile',on_delete=models.CASCADE,null=True,related_name="ach")
    Story1000=models.BooleanField(default=False)
    Task1000=models.BooleanField(default=False)
    project50=models.BooleanField(default=False)
    NoCancel=models.BooleanField(default=True)
    I300xp=models.BooleanField(default=False)
    D300xp=models.BooleanField(default=False)
    T300xp=models.BooleanField(default=False)
    Do300xp=models.BooleanField(default=False)
    Pr300xp=models.BooleanField(default=False)
    m300xp=models.BooleanField(default=False)
    
    


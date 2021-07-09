from django.db import models
from User.models import nUser
# Create your models here.
class Project(models.Model):
    id_pj=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100,unique=True)
    desc=models.TextField()
    type=models.CharField(max_length=3,choices=(('I','Interne'),('E','Externe'),('Ed','Educatif'),('Ot','other')))
    secteur=models.CharField(max_length=5,choices=(('RS','reseausociale'),('Blog','Bolg'),('E-com','e-commerce'),('VG','Video-games'),('AI','Artificial intelligence'),('onS','online-services'),('dig','digitalisation'),('Ot','other')))
    Device=models.CharField(max_length=3,choices=(('Mo','Mobile'),('Web','Web'),('De','desktop'),('Se','serveur'),('Em','Embedded system'),('Ot','other')))
    budget=models.FloatField(help_text="the salary in $")
    start_date=models.DateField(null=True,blank=True)
    date_limit=models.DateField(null=True,blank=True)
    create_date=models.DateField(auto_now_add=True,null=True)
    update_date=models.DateTimeField(blank=True,null=True)
    archieve=models.BooleanField(default=False)
    admin=models.ForeignKey(nUser,on_delete=models.SET_NULL,null=True)


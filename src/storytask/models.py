from django.db import models
from profileEmp.models import profile

# Create your models here.
class Story_task(models.Model):
    id_st=models.BigAutoField(primary_key=True)
    title=models.CharField(max_length=100)
    desc=models.TextField()
    type=models.CharField(max_length=3,choices=(('St','Story'),('T','Task'),('Ot','other')))
    phase=models.CharField(max_length=5,choices=(('In','Intial'),('D','Dev'),('T','Test'),('Do','Documentation'),('Pr','Production'),('m','maintenance'),('Ot','other')))
    State=models.CharField(max_length=3,choices=(('C','created'),('A','affected'),('Inp','In progress'),('D','Done'),('Ca','Canceled')))
    nv=models.IntegerField(default=1)
    start_before=models.DateField(null=True,blank=True)
    end_before=models.DateField(null=True,blank=True)
    create_date=models.DateField(auto_now_add=True,null=True)
    start=models.DateTimeField(null=True,blank=True)
    end=models.DateTimeField(null=True,blank=True)
    progress=models.PositiveIntegerField(default=0)
    emp=models.ForeignKey(profile,on_delete=models.SET_NULL,null=True,blank=True)
    strat_after_tasks=models.ManyToManyField("self",blank=True,symmetrical=False)
    duration=models.BigIntegerField(blank=True,null=True,help_text="UnixTime")
    project=models.ForeignKey("project.Project",to_field='id_pj',on_delete=models.CASCADE)

class Rapport(models.Model):
    id_r=models.BigAutoField(primary_key=True)
    rapport=models.TextField()
    date_add=models.DateField(auto_now_add=True)
    State=models.CharField(max_length=3,choices=(('D','Done'),('Ca','Canceled')))
    emp=models.ForeignKey(profile,on_delete=models.SET_NULL,null=True)
    story_task=models.ForeignKey(Story_task,to_field='id_st', on_delete=models.CASCADE)

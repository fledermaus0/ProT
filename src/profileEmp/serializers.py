from User.models import nUser
from rest_framework import serializers
from .models import achievment, profile
from User.serializers import UserBrefSerializer, UserCreateSerializer,UserSimpleSerializer
from storytask.models import Story_task

class profilesTasks(serializers.ModelSerializer):    
    class Meta:
        model=Story_task
        fields=('id_st','title','desc','type','phase','nv','start_before','end_before','project','emp','State','progress')

class achievmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=achievment
        fields=('Story1000','Task1000','project50','NoCancel','I300xp','D300xp','T300xp','Do300xp','Pr300xp','m300xp') 

class profileMainSerializer(serializers.ModelSerializer):
    account=serializers.SerializerMethodField()
    def get_account(self,obj):
        p= obj.emp
        return UserCreateSerializer(p).data
    admin=serializers.SerializerMethodField()

    def get_admin(self,obj):
        admin=  obj.emp.admin
        admin =nUser.objects.get(username=admin)
        return UserBrefSerializer(admin).data
    achievment=serializers.SerializerMethodField()
    
    def get_achievment(self,obj):
        ach= obj.ach
        return achievmentSerializer(ach).data

    tasks=serializers.SerializerMethodField()
    def get_tasks(self,obj):
        tasks=Story_task.objects.filter(emp=obj.id_p)
        return profilesTasks(tasks,many=True).data

    class Meta:
        model=profile
        fields='__all__'
    

class profileBrefSerializer(serializers.ModelSerializer):
    account=serializers.SerializerMethodField()
    def get_account(self,obj):
        p= obj.emp
        return UserBrefSerializer(p).data
    
    class Meta:
        model=profile
        fields=('id_p','domaine','XP','account','image')        

class profileSimpleSerializer(serializers.ModelSerializer):
    account=serializers.SerializerMethodField()
    def get_account(self,obj):
        p= obj.emp
        return UserSimpleSerializer(p).data
    class Meta:
        model=profile
        fields=('id_p','XP','account','image')        

class profileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=profile
        fields=('image','CV','domaine','XP','sal') 



from rest_framework import serializers
from .models import Project
from User.serializers import UserSimpleSerializer
from storytask.serializers import story_taskSimpleSerializer

from django.db.models import Q

class projectCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Project
        fields=('title','desc','type','secteur','Device','budget','start_date','date_limit','admin')

class projectMainSerializer(serializers.ModelSerializer):
    count_all_tasks=serializers.SerializerMethodField()
    count_created_tasks=serializers.SerializerMethodField()
    count_affected_tasks=serializers.SerializerMethodField()
    count_Inprogress_tasks=serializers.SerializerMethodField()
    count_Done_tasks=serializers.SerializerMethodField()
    count_Canceled_tasks=serializers.SerializerMethodField()
    admin=UserSimpleSerializer()
    backlogItems=serializers.SerializerMethodField()
    inProgressItems=serializers.SerializerMethodField()
    doneItems=serializers.SerializerMethodField()
    canceldItems =serializers.SerializerMethodField()
    
    def get_count_all_tasks(self,obj):
        return obj.story_task_set.count()
    def get_count_created_tasks(self,obj):
        return obj.story_task_set.filter(State='C').count()
    def get_count_affected_tasks(self,obj):
        return obj.story_task_set.filter(State='A').count()
    def get_count_Inprogress_tasks(self,obj):
        return obj.story_task_set.filter(State='Inp').count()
    def get_count_Done_tasks(self,obj):
        return obj.story_task_set.filter(State='D').count()
    def get_count_Canceled_tasks(self,obj):
        return obj.story_task_set.filter(State='Ca').count()
    

    def get_backlogItems(self,obj):
        s= obj.story_task_set.filter(Q(State='C')|Q(State='A'))
        ser=story_taskSimpleSerializer(s,many=True)
        return ser.data

    def get_inProgressItems(self,obj):
        s= obj.story_task_set.filter(State='Inp')
        ser=story_taskSimpleSerializer(s,many=True)
        return ser.data    
    def get_doneItems(self,obj):
        s= obj.story_task_set.filter(State='D')
        ser=story_taskSimpleSerializer(s,many=True)
        return ser.data  
    def get_canceldItems(self,obj):
        s= obj.story_task_set.filter(State='Ca')
        ser=story_taskSimpleSerializer(s,many=True)
        return ser.data  
    class Meta:
        model=Project
        fields='__all__'
    
    
   

class projectBrefSerializer(serializers.ModelSerializer):
    count_all_tasks=serializers.SerializerMethodField()
    count_created_tasks=serializers.SerializerMethodField()
    count_affected_tasks=serializers.SerializerMethodField()
    count_Inprogress_tasks=serializers.SerializerMethodField()
    count_Done_tasks=serializers.SerializerMethodField()
    count_Canceled_tasks=serializers.SerializerMethodField()
    admin=UserSimpleSerializer()
    
    def get_count_all_tasks(self,obj):
        return obj.story_task_set.count()
    def get_count_created_tasks(self,obj):
        return obj.story_task_set.filter(State='C').count()
    def get_count_affected_tasks(self,obj):
        return obj.story_task_set.filter(State='A').count()
    def get_count_Inprogress_tasks(self,obj):
        return obj.story_task_set.filter(State='Inp').count()
    def get_count_Done_tasks(self,obj):
        return obj.story_task_set.filter(State='D').count()
    def get_count_Canceled_tasks(self,obj):
        return obj.story_task_set.filter(State='Ca').count()
    class Meta:
        model = Project
        fields=('id_pj','title','start_date','date_limit','count_all_tasks','count_created_tasks','count_affected_tasks','count_Inprogress_tasks','count_Done_tasks','count_Canceled_tasks','archieve','admin')


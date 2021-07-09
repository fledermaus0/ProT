from datetime import datetime
from project.models import Project
from profileEmp.serializers import profileSimpleSerializer,UserSimpleSerializer
from rest_framework import serializers
from .models import Story_task,Rapport

class projectBrefSerializer(serializers.ModelSerializer):
    #temp avoid import conflit import circly
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
        fields=('id_pj','title','start_date','date_limit','count_all_tasks','count_created_tasks','count_affected_tasks','count_Inprogress_tasks','count_Done_tasks','count_Canceled_tasks','admin')

class story_taskSimpleSerializer(serializers.ModelSerializer):
    emp=profileSimpleSerializer()
    class Meta:
        model=Story_task
        fields=('id_st','title','State','type','emp','progress')


class rapportMainSerializer(serializers.ModelSerializer):
    emp=profileSimpleSerializer()
    class Meta:
        model=Rapport
        fields='__all__'

class story_taskMainSerializer(serializers.ModelSerializer):
    
    emp=profileSimpleSerializer()
    project=projectBrefSerializer()
    strat_after_tasks=story_taskSimpleSerializer(many=True)
    rapports=serializers.SerializerMethodField()
    def get_rapports(self,obj):
        rapports=obj.rapport_set.all()
        return rapportMainSerializer(rapports,many=True).data
    class Meta:
        model=Story_task
        fields='__all__'        

class story_taskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Story_task
        fields=('pk','title','desc','type','phase','nv','start_before','end_before','strat_after_tasks','project','emp','State')
    def create(self, validated_data):
        tasks = validated_data.pop('strat_after_tasks')
        task = Story_task.objects.create(**validated_data)
        for t in tasks:
            task.strat_after_tasks.add(t)
        task.project.update_date=datetime.now()
        task.project.save()   
        return task

class rapportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Rapport
        fields=('rapport','State','emp','story_task')
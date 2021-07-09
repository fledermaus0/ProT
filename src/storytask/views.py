
from django.views.decorators.csrf import csrf_exempt
from profileEmp.models import profile
from .models import Rapport, Story_task
from .serializers import rapportCreateSerializer, story_taskCreateSerializer, story_taskMainSerializer
from datetime import datetime
from django.db.models import Q,Sum,Count

from django.http.response import HttpResponseBadRequest, HttpResponseServerError, JsonResponse,HttpResponseForbidden,HttpResponseNotFound
from rest_framework.parsers import JSONParser

class AchevAuto:
    def achStory1000(id):
        try:
           p=profile.objects.get(id_p=id)
           s=Story_task.objects.filter(emp=p.id_p,State='D',type="St").count()
           
           if not p.ach.Story1000 and s>=1000:
               p.ach.Story1000=True
               p.ach.save()
               return True
           else:
                return False   
        except:
            return HttpResponseServerError("Oops, Something Went Wrong") 

    def achTask1000(id):
        try:
           p=profile.objects.get(id_p=id)
           s=Story_task.objects.filter(emp=p.id_p,State='D',type="T").count()
           
           if not p.ach.Task1000 and s>=1000:
               p.ach.Task1000=True
               p.ach.save()
               return True
           else:
                return False   
        except:
            return HttpResponseServerError("Oops, Something Went Wrong")       
    
    def achI300xp(id):
        try:
           p=profile.objects.get(id_p=id)
           s=Story_task.objects.filter(emp=p.id_p,State='D',phase="In").aggregate(s=Sum('nv'))['s']
           
           if s and not p.ach.I300xp and s>=300:
               p.ach.I300xp=True
               p.ach.save()
               return True
           else:
                return False   
        except:
            return HttpResponseServerError("Oops, Something Went Wrong")
    
    def achD300xp(id):
        try:
           p=profile.objects.get(id_p=id)
           s=Story_task.objects.filter(emp=p.id_p,State='D',phase="D").aggregate(s=Sum('nv'))['s']
           
           if s and not p.ach.D300xp and s>=300:
               p.ach.D300xp=True
               p.ach.save()
               return True
           else:
                return False   
        except:
            return HttpResponseServerError("Oops, Something Went Wrong")        

    
    def achT300xp(id):
        try:
           p=profile.objects.get(id_p=id)
           s=Story_task.objects.filter(emp=p.id_p,State='D',phase="T").aggregate(s=Sum('nv'))['s']
           
           if s and  not p.ach.T300xp and s>=300:
               p.ach.T300xp=True
               p.ach.save()
               return True
           else:
                return False   
        except Exception as e:
            print(str(e))
            return HttpResponseServerError("Oops, Something Went Wrong")        

    def achDo300xp(id):
        try:
           p=profile.objects.get(id_p=id)
           s=Story_task.objects.filter(emp=p.id_p,State='D',phase="Do").aggregate(s=Sum('nv'))['s']
           
           if s and not p.ach.Do300xp and s>=300:
               p.ach.Do300xp=True
               p.ach.save()
               return True
           else:
                return False   
        except :
            return HttpResponseServerError("Oops, Something Went Wrong")        

    def achPr300xp(id):
        try:
           p=profile.objects.get(id_p=id)
           s=Story_task.objects.filter(emp=p.id_p,State='D',phase="Pr").aggregate(s=Sum('nv'))['s']
           if s and not p.ach.Pr300xp and s>=300:
               p.ach.Pr300xp=True
               p.ach.save()
               return True
           else:
                return False   
        except:
            return HttpResponseServerError("Oops, Something Went Wrong")  

    def achm300xp(id):
        try:
           p=profile.objects.get(id_p=id)
           s=Story_task.objects.filter(emp=p.id_p,State='D',phase="m").aggregate(s=Sum('nv'))['s']
           
           if s and not p.ach.m300xp and s>=300:
               p.ach.m300xp=True
               p.ach.save()
               return True
           else:
                return False   
        except:
            return HttpResponseServerError("Oops, Something Went Wrong")  

    def achProject50(id):
        try:
           p=profile.objects.get(id_p=id)
           s=len(Story_task.objects.filter(emp=p.id_p).values('project').annotate(n=Count('project')))
           if not p.ach.Project50 and s>=50:
               p.ach.project50=True
               p.ach.save()
               return True
           else:
                return False   
        except:
            return HttpResponseServerError("Oops, Something Went Wrong") 

    def achNoCancel(id):
        try:
           p=profile.objects.get(id_p=id)
           s=Rapport.objects.filter(emp=p.id_p,State='Ca').count()
           
           if  s>0:
               p.ach.NoCancel=False
               p.ach.save()
               return True
           else:
                return False   
        except:
            return HttpResponseServerError("Oops, Something Went Wrong")

    def newdataFromcsv(r):
        pa=profile.objects.all()
        for p in pa:
            AchevAuto.achTask1000(p.id_p)
            AchevAuto.achStory1000(p.id_p)
            AchevAuto.achD300xp(p.id_p)
            AchevAuto.achDo300xp(p.id_p)
            AchevAuto.achI300xp(p.id_p)
            AchevAuto.achPr300xp(p.id_p)
            AchevAuto.achT300xp(p.id_p)
            AchevAuto.achm300xp(p.id_p)
            AchevAuto.achNoCancel(p.id_p)
            AchevAuto.achProject50(p.id_p)

class task_rapportsApi():
    @csrf_exempt 
    def getTaskById(request,id):
        if request.method=="GET":
            try:
                task=Story_task.objects.get(id_st=id)  
            except Story_task.DoesNotExist:
                return HttpResponseNotFound("task not found") 
            task_serialized=story_taskMainSerializer(task,many=False)
            return JsonResponse(task_serialized.data,safe=False)
        else:
            return HttpResponseBadRequest("bad Request")     
    
    @csrf_exempt 
    def addNewTask(request):
        if request.method=="POST":
            task=JSONParser().parse(request)
            if task['emp']==None:
                task['State']='C'
            else:
                task['State']='A'   
            task_serialized=story_taskCreateSerializer(data=task)
            if task_serialized.is_valid():
                try:
                    taskdata=task_serialized.save()
                except:
                    return HttpResponseServerError("Oops, Something Went Wrong")    
                return JsonResponse(story_taskCreateSerializer(taskdata).data,safe=False)
            else:                          
                return HttpResponseServerError("Failed to add task") 
        else:
            return HttpResponseBadRequest("bad Request")                
    @csrf_exempt
    def startTask(request,id):
        if request.method=="PUT":
            try:
                task=Story_task.objects.get(id_st=id)
                if Story_task.objects.filter(Q(emp=task.emp)& Q(State='Inp')).count()!=0:
                    return HttpResponseForbidden("finish the task in progress first ")
                if task.strat_after_tasks.filter(~Q(State='D')&~Q(State='Ca')).count()!=0:
                    return HttpResponseForbidden("impossible to start the task(it is linked to the unfinished tasks)")    
                task.State='Inp'
                task.start=datetime.now()
                task.save()
                task.project.update_date=datetime.now()
                task.project.save()
            except:
                return HttpResponseServerError("Oops, Something Went Wrong")    
            return JsonResponse("task started",safe=False)    
        else:
            return HttpResponseBadRequest("bad Request")     
    @csrf_exempt
    def endTask(request,id):
        if request.method=="POST":
            try:
                de=datetime.now()
                rapport=JSONParser().parse(request)
                task=Story_task.objects.get(id_st=id)
                task.State=rapport['State']
                task.project.update_date=datetime.now()
                task.end=de
                ds=task.start
                if task.State=='D':
                    task.emp.XP+=task.nv
                else :
                    task.emp.XP-=task.nv    
                task.duration=int(de.timestamp()- ds.timestamp())
                rapport['story_task']=id
                rapport_serialized=rapportCreateSerializer(data=rapport,many=False)
                if rapport_serialized.is_valid():
                    rapport_serialized.save()
                task.emp.save()    
                task.project.save()
                task.save() 
                AchevAuto.achTask1000(task.emp)
                AchevAuto.achStory1000(task.emp)
                AchevAuto.achD300xp(task.emp)
                AchevAuto.achDo300xp(task.emp)
                AchevAuto.achI300xp(task.emp)
                AchevAuto.achPr300xp(task.emp)
                AchevAuto.achT300xp(task.emp)
                AchevAuto.achm300xp(task.emp)
                AchevAuto.achNoCancel(task.emp)
                AchevAuto.achProject50(task.emp)
            except:
                return HttpResponseServerError("Oops, Something Went Wrong")    
            return JsonResponse("task ended successfully",safe=False)
        else:
            return HttpResponseBadRequest("bad Request")     
    @csrf_exempt
    def deleteTask(request,id):
        if request.method=="DELETE":
            try:
                task=Story_task.objects.get(id_st=id)
                task.project.update_date=datetime.now()
                task.project.save()
                task.delete()
            except: 
                return HttpResponseServerError("Oops, Something Went Wrong")    
            return JsonResponse("delete task successfully",safe=False)
        else:
            return HttpResponseBadRequest("bad Request")     
    
    @csrf_exempt
    def progressTask(request,id):
        if request.method=="PUT":
            try:
                progress=JSONParser().parse(request)['progress']
                task=Story_task.objects.get(id_st=id)    
                task.progress=progress
                task.save()
                task.project.update_date=datetime.now()
                task.project.save()
            except:
                return HttpResponseServerError("Oops, Something Went Wrong")    
            return JsonResponse("task progress updated",safe=False)  
        else:
            return HttpResponseBadRequest("bad Request") 

    @csrf_exempt
    def affectEmpToTask(request,id,id2):
        if request.method=="PUT":
            try:
                task=Story_task.objects.get(id_st=id)    
                if(task.State == 'C' or task.State == 'A'): 
                    try:
                        if id2!=0:
                            emp=profile.objects.get(id_p=id2)
                            task.State='A'
                            task.emp=emp
                        else:
                            emp=None    
                            task.State='C'
                    except :
                        return HttpResponseNotFound("profile not founded")
   
                    task.save()
                    task.project.update_date=datetime.now()
                    task.project.save()
                else:
                    return HttpResponseBadRequest("can't change this task")            
            except:
                return HttpResponseServerError("Oops, Something Went Wrong")    
            return JsonResponse("task emp  updated",safe=False)  
        else:
            return HttpResponseBadRequest("bad Request")            


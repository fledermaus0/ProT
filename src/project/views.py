
from User.models import nUser
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

from .models import Project
from .serializers import projectBrefSerializer,projectMainSerializer,projectCreateSerializer
from storytask.serializers import story_taskSimpleSerializer

from django.db.models.functions import TruncMonth,TruncDay
from django.db.models import Q,Count,Sum

from rest_framework.parsers import JSONParser
from django.http.response import  HttpResponseBadRequest, HttpResponseForbidden, HttpResponseServerError, JsonResponse,HttpResponseNotFound




class homeProjectView:
    @csrf_exempt
    def projectSimpleApi(request): 
        if request.method=="GET":
            num_projects=Project.objects.all().count()
            if(num_projects==0):
                return JsonResponse("0 projects",safe=False)
            if(num_projects<3):
                projects=Project.objects.all().order_by('-update_date')[0:num_projects]
                project_serialized=projectBrefSerializer(projects,many=True)
                return JsonResponse(project_serialized.data,safe=False)
            if(num_projects>=3):
                projects=Project.objects.all().order_by('-update_date')[0:3]
                project_serialized=projectBrefSerializer(projects,many=True)
                return JsonResponse(project_serialized.data,safe=False)    
        else:
            return HttpResponseBadRequest("bad Request") 
    @csrf_exempt
    def projectByIdApi(request,id=0):
        if request.method=="GET":
            try:
                project=Project.objects.get(id_pj=id)  
            except Project.DoesNotExist:
                return HttpResponseNotFound("project not found") 
               
            project_serialized=projectMainSerializer(project)
            return JsonResponse(project_serialized.data,safe=False)
        else:
            return HttpResponseBadRequest("bad Request")     
    
    @csrf_exempt
    def projectBySearchApi(request):
        if request.method=="GET"  :
            projects=[]
            orderby='update_date'
            archive=False
            if 'order-by' in request.GET:
                orderby=request.GET['order-by']
            if 'archive' in request.GET:
                archive=request.GET['archive']   
            if 'search' in request.GET:
                search=request.GET['search']
                projects.append(Project.objects.filter(title__icontains=search))
                
            if 'type' in request.GET:
                t=request.GET['type']
                projects.append(Project.objects.filter(type=t))
                    
            if 'secteur' in request.GET:
                s=request.GET['secteur']
                projects.append(Project.objects.filter(secteur=s))

            if 'Device' in request.GET:
                d=request.GET['Device']
                projects.append(Project.objects.filter(Device=d))

            if len(projects)>0:       
                data=projects[0]
                for i in  range(1,len(projects)) :
                    data =data &  projects[i]

                data=data.filter(archieve=archive).order_by(orderby)             
                projects_serialized=projectBrefSerializer(data,many=True)
                return JsonResponse(projects_serialized.data,safe=False)
            else:
                return JsonResponse("No project found",safe=False)        
        else:
            return HttpResponseBadRequest("bad Request")         
    
    @csrf_exempt
    def projectBySearchApi2(request):
        if request.method=="GET"  :
            projects=[]
            
            if 'search' in request.GET:
                search=request.GET['search']
                projects.append(Project.objects.filter(title__icontains=search))
                
           
            if len(projects)>0:       
                data=projects[0]
                for i in  range(1,len(projects)) :
                    data =data &  projects[i]         
                projects_serialized=projectBrefSerializer(data,many=True)
                return JsonResponse(projects_serialized.data,safe=False)
            else:
                return JsonResponse("No project found",safe=False)        
        else:
            return HttpResponseBadRequest("bad Request")
    @csrf_exempt
    def projectGetAll(request):
        if request.method=="GET":
           projects=Project.objects.all()
           projects_serialized=projectBrefSerializer(projects,many=True)
           return JsonResponse(projects_serialized.data,safe=False)  
        else:
            return HttpResponseBadRequest("bad Request")      
    @csrf_exempt
    def addNewProject(request):
        if request.method=="POST":
            project=JSONParser().parse(request)
            project_serialized=projectCreateSerializer(data=project)
            if project_serialized.is_valid():
                try:
                    project_serialized.save()
                except Exception as e:
                    return HttpResponseServerError(str(e))    
                return JsonResponse("add New project By admin : "+str(project['admin']),safe=False)
            else:                          
                return HttpResponseServerError("Failed to add New project By admin : "+str(project['admin']),safe=False)   
        else:
            return HttpResponseBadRequest("bad Request") 
    @csrf_exempt
    def deleteProject(request,id):
        if request.method=="DELETE":
            try:
                try:
                    project=Project.objects.get(id_pj=id)  
                except Project.DoesNotExist:
                    return HttpResponseNotFound("project not found") 
                
                project.delete()
            except: 
                return HttpResponseServerError("Oops, Something Went Wrong")    
            return JsonResponse("delete project successfully",safe=False)
        else:
            return HttpResponseBadRequest("bad Request") 
    @csrf_exempt
    def archiveProject(request,id):
        if request.method=="PUT":   
            try:
                try:
                    project=Project.objects.get(id_pj=id)  
                except Project.DoesNotExist:
                    return HttpResponseNotFound("project not found") 
                if project.story_task_set.filter(Q(State='D')&Q(State='Ca')).count()!=project.story_task_set.all().count():
                    return HttpResponseForbidden("impossible (it is linked to the unfinished tasks)")    
                project.archieve= not project.archieve
                project.update_date=datetime.now()
                project.save()
                if project.archieve:
                    return JsonResponse("archive project successfully",safe=False)    
                else:
                    return JsonResponse("unarchive project successfully",safe=False)
            except :
                return HttpResponseServerError("Oops, Something Went Wrong")
        else:
            return HttpResponseBadRequest("bad Request") 
    @csrf_exempt
    def getProjectTasks(request,id):
        if request.method=="GET":   
            try:
                try:
                    project=Project.objects.get(id_pj=id)  
                except Project.DoesNotExist:
                    return HttpResponseNotFound("project not found") 
                tasks=project.story_task_set.all()
                tasksSerialized=story_taskSimpleSerializer(tasks,many=True)
                return JsonResponse(tasksSerialized.data,safe=False)
            except :
                return HttpResponseServerError("Oops, Something Went Wrong")                    
        else:
            return HttpResponseBadRequest("bad Request")     

class projectBI:
    def projectsActiv(request):
        if request.method=="GET":
            data={
                    "categories":["archive","active"],
                    "series":[{'name':'',
                                'data':[
                        Project.objects.filter(archieve=True).count(),
                    Project.objects.filter(archieve=False).count()]}]
                }
            return JsonResponse(data=data,safe=True)
        else:
            return HttpResponseBadRequest("bad Request")      

    def projectsTypes(request):
               
        if request.method=="GET":    
            p=Project.objects.all().values('type').annotate(num=Count('type')).order_by('-type')
            labels=[]
            series=[]
            for i in range(0,len(p)):
                if p[i]['type']=='I':
                    labels.append('Interne')
                if p[i]['type']=='E':
                    labels.append('Externe')
                if p[i]['type']=='Ed':
                    labels.append('Educatif')
                if p[i]['type']=='Ot':
                    labels.append('other')
                series.append(p[i]['num']) 
            data={
                        "labels":labels,
                        "series":[{'name':'Projects',
                                'data':series}]
                    }
            return JsonResponse(data=data,safe=True)
        else:
            return HttpResponseBadRequest("bad Request")    

    def projectsBySecteur(request):       
        if request.method=="GET":    
            p=Project.objects.all().values('secteur').annotate(num=Count('secteur')).order_by('-secteur')
            labels=[]
            series=[]
            for i in range(0,len(p)):
                if p[i]['secteur']=='RS':
                    labels.append('reseausociale')
                if p[i]['secteur']=='Blog':
                    labels.append('Blog')
                if p[i]['secteur']=='E-com':
                    labels.append('e-commerce')
                if p[i]['secteur']=='VG':
                    labels.append('Video-games')
                if p[i]['secteur']=='AI':
                    labels.append('Artificial intelligence')    
                if p[i]['secteur']=='onS':
                    labels.append('online-services')
                if p[i]['secteur']=='dig':
                    labels.append('digitalisation')
                if p[i]['secteur']=='Ot':
                    labels.append('other')
                series.append(p[i]['num']) 
            data={
                        "labels":labels,
                        "series":[{'name':'Projects',
                                'data':series}]
                    }
            return JsonResponse(data=data,safe=True)
        else:
            return HttpResponseBadRequest("bad Request")              
    
    def projectsByDevice(request):       
        if request.method=="GET":    
            p=Project.objects.all().values('Device').annotate(num=Count('Device')).order_by('-Device')
            labels=[]
            series=[]
            for i in range(0,len(p)):
                if p[i]['Device']=='Mo':
                    labels.append('Mobile')
                if p[i]['Device']=='Web':
                    labels.append('Web')
                if p[i]['Device']=='De':
                    labels.append('desktop')
                if p[i]['Device']=='Se':
                    labels.append('serveur')
                if p[i]['Device']=='Em':
                    labels.append('Embedded system')    
                if p[i]['Device']=='Ot':
                    labels.append('other')
                series.append(p[i]['num']) 
            data={
                        "labels":labels,
                        "series":[{'name':'Projects',
                                'data':series}]
                            
                    }
            return JsonResponse(data=data,safe=True)
        else:
            return HttpResponseBadRequest("bad Request")  

    def projectByAdmin(request):
        if request.method=="GET":    
            p=Project.objects.all().values('admin').annotate(num=Count('admin'))
            labels=[]
            series=[]
            for i in range(0,len(p)):
                labels.append(nUser.objects.get(id=p[i]['admin']).username)
                series.append(p[i]['num']) 
            data={
                        "labels":labels,
                        "series":[{'name':'',
                                'data':series}]    
                    }
            return JsonResponse(data=data,safe=True)
        else:
            return HttpResponseBadRequest("bad Request")   
            
    def projectsTime(request):
        if request.method=="GET":    
            p=Project.objects.annotate(month=TruncMonth('create_date')).values('month').annotate(num=Count('id_pj')).values('month','num')
            p2=Project.objects.filter(type='E').annotate(month=TruncMonth('create_date')).values('month').annotate(num=Count('id_pj')).values('month','num')
            p3=Project.objects.filter(type='I').annotate(month=TruncMonth('create_date')).values('month').annotate(num=Count('id_pj')).values('month','num')
            categories=[]
            series=[];seriesE=[];seriesI=[]
    
            j=0;k=0
            for i in range(0,len(p)):
                categories.append(p[i]['month'])
                if i==0:
                    series.append(p[i]['num'])
                else:
                    series.append(p[i]['num']+series[i-1])    
                if j<len(p2):
                    if j==0:
                        if p2[j]['month']==p[i]['month']:
                            seriesE.append(p2[j]['num'])
                            j+=1
                        else:
                            seriesE.append(0)
                    else:
                        if p2[j]['month']==p[i]['month']:
                            seriesE.append(p2[j]['num']+seriesE[i-1])
                            j+=1
                        else:
                            seriesE.append(seriesE[i-1])        
                else :
                    seriesE.append(seriesE[i-1])
                if k<len(p3):
                    if k==0:    
                        if p3[k]['month']==p[i]['month']:
                            seriesI.append(p3[k]['num'])
                            k+=1
                        else:
                            seriesI.append(0)
                    else:
                        if p3[k]['month']==p[i]['month']:
                            seriesI.append(p3[k]['num']+seriesI[i-1])
                            k+=1
                        else:
                            seriesI.append(seriesI[i-1])
                else:
                    seriesI.append(seriesI[i-1])            
                                                       
            data={
                        "categories":categories,
                        "series":[{'name':'Projects',
                                'data':series},
                                {'name':'Projects Externe',
                                'data':seriesE},
                                {'name':'Projects Interne',
                                'data':seriesI}]    
                    }
            return JsonResponse(data=data,safe=True)
        else:
            return HttpResponseBadRequest("bad Request")  

    def projectsInDanger(request):
        if request.method=="GET":    
            p=Project.objects.filter(Q(archieve=False)&~Q(date_limit=None)).order_by("-date_limit")
            notInDanger=[]
            for i in p:
                if i.story_task_set.count()==0 or i.story_task_set.count() < i.story_task_set.filter(State='D').count()+i.story_task_set.filter(State='Ca').count() and datetime.now().date() < i.date_limit:
                    notInDanger.append(i.id_pj)
            p=p.exclude(id_pj__in =notInDanger)        
            project_serialized=projectBrefSerializer(p,many=True)
            return JsonResponse(project_serialized.data,safe=False)
        else:
            return HttpResponseBadRequest("bad Request")  

    def projectByTitleTaskPhaseState(request,title):
        if request.method=="GET":    
            try:
                p=Project.objects.get(title=title)  
            except Project.DoesNotExist:
                return HttpResponseNotFound("project not found") 
            categories=['D','Do','In','m','Ot','Pr','T']
            seriesC=[];seriesA=[];seriesInp=[];seriesD=[];seriesCa=[]
            s=p.story_task_set.filter(State='C').values('phase').annotate(num=Count('id_st')).values('phase','num').order_by('phase')
            s2=p.story_task_set.filter(State='A').values('phase').annotate(num=Count('id_st')).values('phase','num').order_by('phase')
            s3=p.story_task_set.filter(State='Inp').values('phase').annotate(num=Count('id_st')).values('phase','num').order_by('phase')
            s4=p.story_task_set.filter(State='D').values('phase').annotate(num=Count('id_st')).values('phase','num').order_by('phase')
            s5=p.story_task_set.filter(State='Ca').values('phase').annotate(num=Count('id_st')).values('phase','num').order_by('phase')
            j=k=l=m=n=0
            for i in range(0,len(categories)):

                if len(s)!=0 and j<len(s) and s[j]['phase']==categories[i]:    
                    seriesC.append(s[j]['num']);j+=1
                else:
                    seriesC.append(0)
                if len(s2)!=0 and k<len(s2) and s2[k]['phase']==categories[i]:
                    seriesA.append(s2[k]['num']);k+=1
                else:
                    seriesA.append(0)
                if len(s3)!=0 and m<len(s3) and s3[m]['phase']==categories[i]:
                    seriesInp.append(s3[m]['num']);m+=1
                else:
                    seriesInp.append(0)
                if len(s4)!=0 and l<len(s4) and s4[l]['phase']==categories[i]:
                    seriesD.append(s4[l]['num']);l+=1
                else:
                    seriesD.append(0)
                if len(s5)!=0 and n<len(s5) and s5[n]['phase']==categories[i]:
                    seriesCa.append(s5[n]['num']);n+=1
                else:
                    seriesCa.append(0)                

                
            categories=['Dev','Documentation','Intial','maintenance','other','Production','Test']
            data={
                        "categories":categories,
                        "series":[{'name':'Created',
                                'data':seriesC},
                                {'name':'Affected',
                                'data':seriesA},
                                {'name':'In progress',
                                'data':seriesInp},
                                {'name':'Done',
                                'data':seriesD},
                                {'name':'Canceled',
                                'data':seriesCa}]    
                    }
            return JsonResponse(data=data,safe=True)
        else:
            return HttpResponseBadRequest("bad Request")

    def projectByTitleTaskPhaseType(request,title):
        if request.method=="GET":    
            try:
                p=Project.objects.get(title=title)  
            except Project.DoesNotExist:
                return HttpResponseNotFound("project not found") 
            categories=['D','Do','In','m','Ot','Pr','T']
            seriesS=[];seriesT=[]
            s=p.story_task_set.filter(type='St').values('phase').annotate(num=Count('id_st')).values('phase','num').order_by('phase')
            s2=p.story_task_set.filter(type='T').values('phase').annotate(num=Count('id_st')).values('phase','num').order_by('phase')
            j=k=0
            for i in range(0,len(categories)):
                if len(s)!=0 and j<len(s) and s[j]['phase']==categories[i]: 
                    seriesS.append(s[j]['num']);j+=1
                else:
                    seriesS.append(0)
                if len(s2)!=0 and k<len(s2) and s2[k]['phase']==categories[i]:
                    seriesT.append(s2[k]['num']);k+=1
                else:
                    seriesT.append(0)               

                
            categories=['Dev','Documentation','Intial','maintenance','Production','other','Test']
            data={
                        "categories":categories,
                        "series":[{'name':'Story',
                                'data':seriesS},
                                {'name':'Task',
                                'data':seriesT},
                                ]    
                    }
            return JsonResponse(data=data,safe=True)
        else:
            return HttpResponseBadRequest("bad Request")        

    def projectBurndownChart(request,title):
        if request.method=="GET":    
            try:
                p=Project.objects.get(title=title)  
            except Project.DoesNotExist:
                return HttpResponseNotFound("project not found")
            s=p.story_task_set.annotate(day=TruncDay('create_date')).values('day').annotate(num=Count('id_st')).values('day','num')
            s2=p.story_task_set.filter(State='D').annotate(day=TruncDay('end')).values('day').annotate(num=Count('id_st')).values('day','num')
            
            sl=[];s2l=[]
            for j in range(0,len(s)):
                sl.append(s[j]['day'])
            for j in range(0,len(s2)):
                s2l.append(s2[j]['day'].date())     

            categories=sorted(set(sl+s2l))
            series=[]
            j=k=0
            b=False;b2=False
            for i in range(0,len(categories)):
                if j<len(s):
                    b=True
                else:
                    b=False
                if k<len(s2):
                    b2=True
                else:
                    b2=False        
                if i==0:  
                    
                    if b and b2 and categories[i]==s[j]['day'] and categories[i]==s2[k]['day'].date():
                        series.append(s[j]['num']-s2[k]['num']);j+=1;k+=1
                    elif b and categories[i]==s[j]['day'] :
                        series.append(s[j]['num']);j+=1
                    else:
                        series.append(-s2[k]['num']);k+=1
                else:
                    
                    if b and b2 and categories[i]==s[j]['day'] and categories[i]==s2[k]['day'].date():
                        series.append(series[i-1]+s[j]['num']-s2[k]['num']);j+=1;k+=1
                    elif b and categories[i]==s[j]['day'] :
                        series.append(series[i-1]+s[j]['num']);j+=1
                    else:
                        series.append(series[i-1]-s2[k]['num']);k+=1
            data={
                        "categories":categories,
                        "series":[{'name':'StoryandTasks',
                                'data':series}]    
                    }
            return JsonResponse(data=data,safe=True)
        else:
            return HttpResponseBadRequest("bad Request")         

    def projectBestEmployes(request,title):
        if request.method=="GET":    
            try:
                p=Project.objects.get(title=title)  
            except Project.DoesNotExist:
                return HttpResponseNotFound("project not found") 
            s=p.story_task_set.filter(State='D').values('emp').annotate(XP=Sum('nv')).values('emp','XP')
            categories=[];series=[]
            for i in s:
                categories.append(nUser.objects.get(profile=i['emp']).username)
                series.append(i['XP'])
            data={
                        "categories":categories,
                        "series":[{'name':'XP',
                                'data':series},
                                ]    
                    }
            return JsonResponse(data=data,safe=True)
        else:
            return HttpResponseBadRequest("bad Request")                
    

from django.db.models.fields import DateField
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from User.models import nUser
from storytask.models import Story_task
from .models import achievment, profile
from .serializers import  profileBrefSerializer, profileSimpleSerializer,profileMainSerializer,profileCreateSerializer
import pandas 
from django.db.models import DateField
from django.db.models import Q,Count,Sum
from django.db.models.functions import TruncMonth,TruncWeek

from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse,HttpResponseNotFound,HttpResponseServerError,HttpResponseBadRequest

class adminProfileView(): 
    @csrf_exempt
    def getEmpByUsername(request,username):
        if request.method=="GET":
            try:
                profilee=nUser.objects.get(username=username).profile
            except:
                return HttpResponseNotFound("Object not founded")
            profile_serialized=profileMainSerializer(profilee,many=False)
            return JsonResponse(profile_serialized.data,safe=False)
        else:
            return HttpResponseBadRequest("bad Request")    
    @csrf_exempt
    def getallEmp(request):
        if request.method=="GET":
            profiles=profile.objects.all()
            emp_serialized=profileSimpleSerializer(profiles,many=True)
            return JsonResponse(emp_serialized.data,safe=False) 
        else:
            return HttpResponseBadRequest("bad Request")    

    @csrf_exempt
    def getAllEmp(request):
        if request.method=="GET":
            profiles=profile.objects.all()
            emp_serialized=profileBrefSerializer(profiles,many=True)
            return JsonResponse(emp_serialized.data,safe=False)
        else:
            return HttpResponseBadRequest("bad Request")

    @csrf_exempt
    def getallEmpByAdmin(request,admin):
        if request.method=="GET":
            users=nUser.objects.get(id=admin).nuser_set.all()
            profiles=[]
            for user in users:
                profiles.append(user.profile)
            emp_serialized=profileSimpleSerializer(profiles,many=True)
            return JsonResponse(emp_serialized.data,safe=False) 
        else:
            return HttpResponseBadRequest("bad Request") 
    @csrf_exempt
    def getAllEmpByAdmin(request,admin):
        if request.method=="GET":
            try:
                users=nUser.objects.get(id=admin).nuser_set.all()
            except:
                return HttpResponseNotFound("Object not founded")
            profiles=[]
            for user in users:
                profiles.append(user.profile)
            emp_serialized=profileBrefSerializer(profiles,many=True)
            return JsonResponse(emp_serialized.data,safe=False)   
        else:
            return HttpResponseBadRequest("bad Request")       

    @csrf_exempt
    def addNewProfile(request,username):
        if request.method=="POST":
            try:
                user=nUser.objects.get(username=username)
            except:
                return HttpResponseNotFound("Object not founded")
            pro=JSONParser().parse(request)
            pro_serialized=profileCreateSerializer(data=pro)
            if pro_serialized.is_valid():
                try:
                    #improve using create and push 
                    user.profile=pro_serialized.save()
                    user.profile.save()
                    achievment(profile=user.profile).save()
                    user.save()
                except:
                    return HttpResponseServerError("Oops, Something Went Wrong")    
                return JsonResponse("add profile to "+username,safe=False)
            else:                          
                return HttpResponseServerError("Failed to add profile to"+username)   
        else:
            return HttpResponseBadRequest("bad Request") 
    @csrf_exempt
    def deleteProfile(request,username):
        if request.method=="DELETE":
            try:
                profile=nUser.objects.get(username=username).profile
                profile.delete()
            except:
                return HttpResponseServerError("Oops, Something Went Wrong")    
            return JsonResponse("delete profile successfully",safe=False)
        else:
            return HttpResponseBadRequest("bad Request")     

    @csrf_exempt
    def profileBySearchApi(request):
        if request.method=="GET"  :
            
            if 'search' in request.GET:
                search=request.GET['search']
                users =nUser.objects.filter(username__icontains=search)
                profiles=[]
                for u in users:
                    profiles.append(u.profile)           
                profiles_serialized=profileBrefSerializer(profiles,many=True)
                return JsonResponse(profiles_serialized.data,safe=False)
            else:
                return JsonResponse("No objects  found",safe=False)        
        else:
            return HttpResponseBadRequest("bad Request")        


class profileBI:
    def adminEmployees(request):
        if request.method=="GET":
            admins=nUser.objects.filter(is_admin=False).values('admin').annotate(num=Count('id')).values('admin','num')
            categories=[];serie=[] 
            for i in range(0,len(admins)):
                categories.append(nUser.objects.get(id=admins[i]['admin']).username)
                serie.append(admins[i]['num'])
            data={
                    "categories":categories,
                    "series":[{'name':'Profiles',
                                'data':serie}]
                }
            return JsonResponse(data=data,safe=True)
        else:
            return HttpResponseBadRequest("bad Request") 

    def employeesTime(request):
        if request.method=="GET":
            users=nUser.objects.filter(is_admin=False).annotate(month=TruncMonth('date_joined', output_field=DateField())).values('month').annotate(num=Count('id')).values('month','num')
            categories=[];serie=[] 
            for i in range(0,len(users)):
                categories.append(users[i]['month'])
                serie.append(users[i]['num'])
            data={
                    "categories":categories,
                    "series":[{'name':'Profiles',
                                'data':serie}]
                }
            return JsonResponse(data=data,safe=True)
        else:
            return HttpResponseBadRequest("bad Request")      

    def employeeTasksPhase(request,username):
        if request.method=="GET":
            pro=nUser.objects.get(username=username).profile.id_p
            task=Story_task.objects.filter(emp=pro,State='D').values('phase').annotate(num=Sum('nv')).values('phase','num')
            dicC={'D':'Dev','Do':'Documentation','In':'Intial','m':'maintenance','Ot':'other','Pr':'Production','T':'Test'}
            categories=[];serie=[];j=0 
            for i in list(dicC.keys()):
                if j<len(task):
                    if i==task[j]['phase']:
                        categories.append(dicC[i])
                        serie.append(task[j]['num']);j+=1
                    else:
                        categories.append(dicC[i])
                        serie.append(0)
                else:
                        categories.append(dicC[i])
                        serie.append(0)    
            data={
                    "categories":categories,
                    "series":[{'name':'the sum of points gained in each phase',
                                'data':serie}]
                }
            return JsonResponse(data=data,safe=True)
        else:
            return HttpResponseBadRequest("bad Request")  

    def employeeStoryTaskType(request,username):
        if request.method=="GET":
            pro=nUser.objects.get(username=username).profile.id_p
            task=Story_task.objects.filter(emp=pro,State='D').values('type').annotate(num=Count('id_st')).values('type','num')
            dicC={'St':'Story','T':'Task','Ot':'other'}
            categories=[];serie=[];j=0 
            for i in list(dicC.keys()):
                if j<len(task):
                    if i==task[j]['type']:
                        categories.append(dicC[i])
                        serie.append(task[j]['num']);j+=1
                    else:
                        categories.append(dicC[i])
                        serie.append(0)
                else:
                        categories.append(dicC[i])
                        serie.append(0)    
            data={
                    "categories":categories,
                    "series":[{'name':'Story_Task Type',
                                'data':serie}]
                }
            return JsonResponse(data=data,safe=True)
        else:
            return HttpResponseBadRequest("bad Request")        

    def employeeProjectsSecteur(request,username):
        if request.method=="GET":
            pro=nUser.objects.get(username=username).profile.id_p
            tasks=[]
            categories=['reseausociale','Bolg','e-commerce','Video-games','Artificial intelligence','online-services','digitalisation']
            task1=Story_task.objects.filter(emp=pro,State='D',project__secteur='RS').annotate(num=Sum('nv')).values('num').aggregate(s=Sum('num'))
            if task1['s']==None:
                tasks.append(0)
            else :
                tasks.append(task1['s'])    
            task1=Story_task.objects.filter(emp=pro,State='D',project__secteur='Blog').annotate(num=Sum('nv')).values('num').aggregate(s=Sum('num'))
            if task1['s']==None:               
                tasks.append(0)
            else :
                tasks.append(task1['s'])
            task1=Story_task.objects.filter(emp=pro,State='D',project__secteur='E-com').annotate(num=Sum('nv')).values('num').aggregate(s=Sum('num'))
            if task1['s']==None:
                tasks.append(0)
            else :
                tasks.append(task1['s'])
            task1=Story_task.objects.filter(emp=pro,State='D',project__secteur='VG').annotate(num=Sum('nv')).values('num').aggregate(s=Sum('num'))
            if task1['s']==None:
                tasks.append(0)
            else :
                tasks.append(task1['s'])
            task1=Story_task.objects.filter(emp=pro,State='D',project__secteur='AI').annotate(num=Sum('nv')).values('num').aggregate(s=Sum('num'))
            if task1['s']==None:
                tasks.append(0)
            else :
                tasks.append(task1['s'])
            task1=Story_task.objects.filter(emp=pro,State='D',project__secteur='onS').annotate(num=Sum('nv')).values('num').aggregate(s=Sum('num'))
            if task1['s']==None:
                tasks.append(0)
            else :
                tasks.append(task1['s'])
            task1=Story_task.objects.filter(emp=pro,State='D',project__secteur='dig').annotate(num=Sum('nv')).values('num').aggregate(s=Sum('num'))
            if task1['s']==None:
                tasks.append(0)
            else :
                tasks.append(task1['s'])
            data={
                    "categories":categories,
                    "series":[{'name':'the sum of points gained in each Secteur',
                                'data':tasks}]
                }
            return JsonResponse(data=data,safe=True)
        else:
            return HttpResponseBadRequest("bad Request")     

    def employeeProjectsDevice(request,username):
        if request.method=="GET":
            pro=nUser.objects.get(username=username).profile.id_p
            tasks=[]
            categories=['Mobile','Web','desktop','serveur','Embedded system']
            task1=Story_task.objects.filter(emp=pro,State='D',project__Device='Mo').annotate(num=Sum('nv')).values('num').aggregate(s=Sum('num'))
            if task1['s']==None:
                tasks.append(0)
            else :
                tasks.append(task1['s'])    
            task1=Story_task.objects.filter(emp=pro,State='D',project__Device='Web').annotate(num=Sum('nv')).values('num').aggregate(s=Sum('num'))
            if task1['s']==None:               
                tasks.append(0)
            else :
                tasks.append(task1['s'])
            task1=Story_task.objects.filter(emp=pro,State='D',project__Device='De').annotate(num=Sum('nv')).values('num').aggregate(s=Sum('num'))
            if task1['s']==None:
                tasks.append(0)
            else :
                tasks.append(task1['s'])
            task1=Story_task.objects.filter(emp=pro,State='D',project__Device='Se').annotate(num=Sum('nv')).values('num').aggregate(s=Sum('num'))
            if task1['s']==None:
                tasks.append(0)
            else :
                tasks.append(task1['s'])
            task1=Story_task.objects.filter(emp=pro,State='D',project__Device='Em').annotate(num=Sum('nv')).values('num').aggregate(s=Sum('num'))
            if task1['s']==None:
                tasks.append(0)
            else :
                tasks.append(task1['s'])
            data={
                    "categories":categories,
                    "series":[{'name':'the sum of points gained in each Device',
                                'data':tasks}]
                }
            return JsonResponse(data=data,safe=True)
        else:
            return HttpResponseBadRequest("bad Request")   

    def employeeProjectsType(request,username):
        if request.method=="GET":
            pro=nUser.objects.get(username=username).profile.id_p
            tasks=[]
            categories=['Interne','Externe','Educatif']
            task1=Story_task.objects.filter(emp=pro,State='D',project__type='I').annotate(num=Count('project')).aggregate(s=Sum('num'))
            if task1['s']==None:
                tasks.append(0)
            else :
                tasks.append(task1['s'])    
            task1=Story_task.objects.filter(emp=pro,State='D',project__type='E').annotate(num=Count('project')).aggregate(s=Sum('num'))
            if task1['s']==None:               
                tasks.append(0)
            else :
                tasks.append(task1['s'])
            task1=Story_task.objects.filter(emp=pro,State='D',project__type='Ed').annotate(num=Count('project')).aggregate(s=Sum('num'))
            if task1['s']==None:
                tasks.append(0)
            else :
                tasks.append(task1['s'])
            
            data={
                    "categories":categories,
                    "series":[{'name':'the sum of tasks in each project Type',
                                'data':tasks}]
                }
            return JsonResponse(data=data,safe=True)
        else:
            return HttpResponseBadRequest("bad Request")  

    def employeeXpByWeeks(request,username):
        if request.method=="GET":
            pro=nUser.objects.get(username=username).profile
            serie=[]
            categories=[]
            categories.append((pro.emp.date_joined).date())
            serie.append(pro.XP-Story_task.objects.filter(emp=pro.id_p,State='D').aggregate(s=Sum('nv'))['s'])
            nvs=Story_task.objects.filter(emp=pro.id_p,State='D').annotate(date=TruncWeek('end')).values('date').annotate(s=Sum('nv')).values('date','s')
            
            for i in range(0,len(nvs)):
                serie.append(nvs[i]['s']+serie[i])
                categories.append(nvs[i]['date'].date())         
            data={
                    "categories":categories,
                    "series":[{'name':'Xp evolutiion by weeks',
                                'data':serie}]
                }
            return JsonResponse(data=data,safe=True)
        else:
            return HttpResponseBadRequest("bad Request")   

    def profilesSalarySummary(request):
        if request.method=="GET":
            o=list(profile.objects.all().values('sal'))
            
            df=pandas.DataFrame(o).describe()
            serie=[]  
            serie.append(df['sal'][3])
            serie.append(df['sal'][4])
            serie.append(df['sal'][5])
            serie.append(df['sal'][6])
            serie.append(df['sal'][7])       
            data={
                    "x":"salary",
                    "y":serie
                }
            return JsonResponse(data=data,safe=True)
        else:
            return HttpResponseBadRequest("bad Request")


    def profilesAgeSummary(request):
        if request.method=="GET":
            o=profile.objects.all()
            Year=datetime.now().year
            x=[]
            for i in o:
                x.append(Year-i.emp.birthdate.year)
            
            df=pandas.DataFrame(x).describe()
            serie=[]  
            serie.append(df[0][3])
            serie.append(df[0][4])
            serie.append(df[0][5])
            serie.append(df[0][6])
            serie.append(df[0][7])       
            data={
                    "x":"Age",
                    "y":serie
                }
            return JsonResponse(data=data,safe=True)
        else:
            return HttpResponseBadRequest("bad Request")

    def profilesXPSummary(request):  
        if request.method=="GET":
            o=list(profile.objects.all().values('XP'))
            
            
            df=pandas.DataFrame(o).describe()
            serie=[]  
            serie.append(df['XP'][3])
            serie.append(df['XP'][4])
            serie.append(df['XP'][5])
            serie.append(df['XP'][6])
            serie.append(df['XP'][7])       
            data={
                    "x":"xp",
                    "y":serie
                }
            return JsonResponse(data=data,safe=True)
        else:
            return HttpResponseBadRequest("bad Request")

                                                   


                    

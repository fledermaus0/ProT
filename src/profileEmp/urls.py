from django.urls import path
from .views import adminProfileView,profileBI

urlpatterns = [
    path('<str:username>/',adminProfileView.getEmpByUsername),
    path('all',adminProfileView.getallEmp),
    path('All',adminProfileView.getAllEmp),
    path('<int:admin>/all',adminProfileView.getallEmpByAdmin),
    path('<int:admin>/All',adminProfileView.getAllEmpByAdmin),
    path('<str:username>/add-profile',adminProfileView.addNewProfile),
    path('',adminProfileView.profileBySearchApi),
    path('<str:username>/delete-profile',adminProfileView.deleteProfile),
    path('BI/admin-profile',profileBI.adminEmployees),
    path('BI/profile-time',profileBI.employeesTime),
    path('BI/profiles-salary-summary',profileBI.profilesSalarySummary),
    path('BI/profiles-xp-summary',profileBI.profilesXPSummary),
    path('BI/profiles-age-summary',profileBI.profilesAgeSummary),
    path('BI/<str:username>/profile-tasks-phase',profileBI.employeeTasksPhase),
    path('BI/<str:username>/profile-tasks-type',profileBI.employeeStoryTaskType),
    path('BI/<str:username>/profile-project-secteur',profileBI.employeeProjectsSecteur),
    path('BI/<str:username>/profile-project-device',profileBI.employeeProjectsDevice),
    path('BI/<str:username>/profile-project-type',profileBI.employeeProjectsType),    
    path('BI/<str:username>/profile-xp-by-weeks',profileBI.employeeXpByWeeks),    

]

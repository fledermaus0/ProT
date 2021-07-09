from django.urls import path
from .views import task_rapportsApi,AchevAuto

urlpatterns = [
    path('add-new-task',task_rapportsApi.addNewTask),
    path('<int:id>/',task_rapportsApi.getTaskById),
    path('<int:id>/start-task',task_rapportsApi.startTask),
    path('<int:id>/end-task',task_rapportsApi.endTask),
    path('<int:id>/delete-task',task_rapportsApi.deleteTask),
    path('<int:id>/to-emp/<int:id2>',task_rapportsApi.affectEmpToTask),
    path('<int:id>/progress',task_rapportsApi.progressTask),
    path('',AchevAuto.newdataFromcsv)    
]

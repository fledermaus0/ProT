from django.urls import path
from .views import homeProjectView,projectBI

urlpatterns = [
    path('home/',homeProjectView.projectSimpleApi),
    path('<int:id>/',homeProjectView.projectByIdApi),
    path('',homeProjectView.projectBySearchApi),
    path('lol/',homeProjectView.projectBySearchApi2),
    path('all',homeProjectView.projectGetAll),
    path('add-new-project',homeProjectView.addNewProject),
    path('<int:id>/archive-project',homeProjectView.archiveProject),
    path('<int:id>/delete-project',homeProjectView.deleteProject),
    path('<int:id>/all-tasks',homeProjectView.getProjectTasks),
    path('BI/archive-active-project',projectBI.projectsActiv),
    path('BI/project-by-types',projectBI.projectsTypes),
    path('BI/project-by-secteur',projectBI.projectsBySecteur),
    path('BI/project-by-device',projectBI.projectsByDevice),
    path('BI/project-by-Admin',projectBI.projectByAdmin),
    path('BI/project-time',projectBI.projectsTime),
    path('BI/project-in-danger',projectBI.projectsInDanger),
    path('BI/<str:title>/project-by-title-tasks-phase-state',projectBI.projectByTitleTaskPhaseState),
    path('BI/<str:title>/project-by-title-tasks-phase-type',projectBI.projectByTitleTaskPhaseType),
    path('BI/<str:title>/burndown-chart',projectBI.projectBurndownChart),
    path('BI/<str:title>/project-best-employess',projectBI.projectBestEmployes),
]

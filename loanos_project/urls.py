"""
URL configuration for loanos_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import job_master_view, question_master_view,task_master_view,state_master_view,siac_master_view
from core.views import JobMasterAPI,QuestionMasterAPI,TaskMasterAPI,StateMasterAPI, SiacMasterAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('api/job/', JobMasterAPI.as_view()),
    path('api/job/<int:pk>/', JobMasterAPI.as_view()),
    path('api/question/', QuestionMasterAPI.as_view()),
    path('api/question/<int:pk>/', QuestionMasterAPI.as_view()),
    path('api/task/', TaskMasterAPI.as_view()),
    path('api/task/<int:pk>/', TaskMasterAPI.as_view()),
    path('api/state/',StateMasterAPI.as_view()),
    path('api/state/<int:pk>/',StateMasterAPI.as_view()),
    path('api/siac/',SiacMasterAPI.as_view()),
    path('api/siac/<int:pk>/',SiacMasterAPI.as_view()),
]
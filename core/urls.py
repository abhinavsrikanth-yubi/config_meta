from django.urls import path, register_converter
from django.contrib import admin
from .views import job_master_view, question_master_view,task_master_view,state_master_view,siac_master_view, index, get_master_results, job_list_view, job_detail_view , debug_view, task_list_view, task_detail_view, state_list_view, state_detail_view, siac_list_view, siac_detail_view, question_list_view, question_detail_view, config_list_view, config_detail_view, config_redirect_view, question_search_api
from .views import config_list_view, config_create_view, config_update_view, config_detail_view, index, account_info, test_view, finalize_changelog
from django.contrib.auth import views as auth_views

from . import viewpage

# Custom path converter for config_id
class ConfigIDConverter:
    regex = r'[-0-9#]+'

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return str(value)

# Custom path converter for signed integers (allow negative and positive)
class SignedIntConverter:
    regex = r'-?\d+'
    def to_python(self, value):
        return int(value)
    def to_url(self, value):
        return str(value)

# Register the custom converters
register_converter(ConfigIDConverter, 'config_id')
register_converter(SignedIntConverter, 'signedint')

urlpatterns = [
    #login
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/info/', account_info, name='account_info'),
    path('', index, name='index'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    # Job URLs
    path('job/', job_master_view, name='job_master'),
    path('job/view/', viewpage.job_view, name='job_list'),
    path('job/create/', job_master_view, name='job_create'),
    path('job/update/<signedint:pk>/', job_master_view, name='job_update'),
    path('job/search/', viewpage.job_search, name='job_search'),
    path('job/<signedint:pk>/', job_detail_view, name='job_detail'),
    # Task URLs
    path('task/view/', task_list_view, name='task_list'),
    path('task/create/', task_master_view, name='task_create'),
    path('task/update/<signedint:pk>/', task_master_view, name='task_update'),
    path('task/<signedint:pk>/', task_detail_view, name='task_detail'),
    # State URLs
    path('state/view/', state_list_view, name='state_list'),
    path('state/create/', state_master_view, name='state_create'),
    path('state/update/<signedint:pk>/', state_master_view, name='state_update'),
    path('state/<signedint:pk>/', state_detail_view, name='state_detail'),
    # SIAC URLs
    path('siac/view/', siac_list_view, name='siac_list'),
    path('siac/create/', siac_master_view, name='siac_create'),
    path('siac/update/<signedint:pk>/', siac_master_view, name='siac_update'),
    path('siac/<signedint:pk>/', siac_detail_view, name='siac_detail'),
    # Question URLs
    path('question/search/', question_search_api, name='question_search_api'),
    path('question/view/', question_list_view, name='question_list'),
    path('question/create/', question_master_view, name='question_create'),
    path('question/update/<signedint:pk>/', question_master_view, name='question_update'),
    path('question/<signedint:pk>/', question_detail_view, name='question_detail'),
    # path('config/',config_data_view,name='config_meta'),
    path('config/', config_redirect_view),  # <-- This must come BEFORE more specific config routes!
    path('config/view/', config_list_view, name='config_list'),
    path('config/create/', config_create_view, name='config_create'),
    path('config/update/<config_id:pk>/', config_update_view, name='config_update'),
    path('config/<config_id:pk>/', config_detail_view, name='config_detail'),
    path('config/search/', viewpage.config_search, name='config_search'),
    # Debug
    path('debug/', debug_view, name='debug'),
    path('get/', get_master_results, name='get_results'),
    path('question/search/', viewpage.question_search, name='question_search'),
    path('question/<int:pk>/', viewpage.question_detail, name='question_detail'),
    path('job/search/', viewpage.job_search, name='job_search'),
    # path('job/<int:pk>/', viewpage.job_detail, name='job_detail'),
    path('task/search/', viewpage.task_search, name='task_search'),
    path('task/<int:pk>/', viewpage.task_detail, name='task_detail'),
    path('state/search/', viewpage.state_search, name='state_search'),
    path('state/<int:pk>/', viewpage.state_detail, name='state_detail'),
    path('siac/search/', viewpage.siac_search, name='siac_search'),
    path('siac/<int:pk>/', viewpage.siac_detail, name='siac_detail'),
    path('job/view/', viewpage.job_view, name='job_view'),
    path('question/view/', viewpage.question_view, name='question_view'),
    path('task/view/', viewpage.task_view, name='task_view'),
    path('state/view/', viewpage.state_view, name='state_view'),
    path('siac/view/', viewpage.siac_view, name='siac_view'),
    # path('config/view/', viewpage.config_view, name='config_view'),
    path('config/view/', config_list_view, name='config_list'),
    path('config/search/', viewpage.config_search, name='config_search'),
    path('config/<config_id:pk>/', viewpage.config_detail, name='config_detail'),
    path('config/<config_id:pk>/', config_detail_view, name='config_detail'),
    path('finalize-changelog/', finalize_changelog, name='finalize_changelog'),
    path('test-changelog/', test_view, name='test_changelog'),
]
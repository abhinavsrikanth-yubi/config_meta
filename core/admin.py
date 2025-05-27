from django.contrib import admin
from .models import JobMaster, QuestionMaster, TaskMaster, StateMaster, SiacMaster, ConfigMetas

@admin.register(JobMaster)
class JobMasterAdmin(admin.ModelAdmin):
    list_display = ('job_id', 'job_name', 'order_id')
    search_fields = ('job_id', 'job_name')

@admin.register(QuestionMaster)
class QuestionMasterAdmin(admin.ModelAdmin):
    list_display = ('question_id', 'question_name', 'is_active', 'is_master', 'source_category')
    search_fields = ('question_id', 'question_name')
    list_filter = ('is_active', 'is_master')

@admin.register(TaskMaster)
class TaskMasterAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'task_name', 'task_type', 'mandatory', 'order_id')
    search_fields = ('task_id', 'task_name')
    list_filter = ('mandatory',)

@admin.register(StateMaster)
class StateMasterAdmin(admin.ModelAdmin):
    list_display = ('state_id', 'state_name', 'description')
    search_fields = ('state_id', 'state_name')

@admin.register(SiacMaster)
class SiacMasterAdmin(admin.ModelAdmin):
    list_display = ('siac_id', 'description', 'scheme', 'sector')
    search_fields = ('siac_id', 'description')

@admin.register(ConfigMetas)
class ConfigMetasAdmin(admin.ModelAdmin):
    list_display = ('id', 'state_id', 'question_id', 'siac_id', 'task_id', 'job_id', 'entity_type')
    search_fields = ('id', 'state_id', 'question_id', 'siac_id')
    list_filter = ('entity_type', 'is_active')

    # def has_change_permission(self, request, obj=None):
    #     # Allow 'product' group to update, 'developer' group only to view
    #     if request.user.groups.filter(name='product').exists():
    #         return True
    #     elif request.user.groups.filter(name='developer').exists():
    #         # Only allow view, not update
    #         if request.method in ['GET', 'HEAD', 'OPTIONS']:
    #             return True
    #         return False
    #     return super().has_change_permission(request, obj)

    # def has_view_permission(self, request, obj=None):
    #     # Both groups can view
    #     if request.user.groups.filter(name__in=['product', 'developer']).exists():
    #         return True
    #     return super().has_view_permission(request, obj)

    # def has_add_permission(self, request):
    #     # Only product group can add
    #     return request.user.groups.filter(name='product').exists()

    # def has_delete_permission(self, request, obj=None):
    #     # Only product group can delete
    #     return request.user.groups.filter(name='product').exists()

# admin.site.register(ConfigMetas, ConfigMetasAdmin)
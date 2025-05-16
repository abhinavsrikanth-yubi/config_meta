# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone
from datetime import datetime
import pytz

INDIA_TZ = pytz.timezone('Asia/Kolkata')

# class ConfigMetas(models.Model):
#     id = models.CharField(max_length=100, primary_key=True)
#     config_id = models.CharField(max_length=100, null=True)
#     parent_question_operator = models.CharField(max_length=255, null=True)
#     siac_id = models.CharField(max_length=255, null=True)
#     default_option = models.JSONField(null=True)
#     parent_response_condition = models.JSONField(null=True)
#     possible_options = models.CharField(null=True)
#     enable_task_response = models.JSONField(null=True)
#     entity_type = models.CharField(max_length=255, null=True)
#     parent_option_condition = models.JSONField(null=True)
#     question_type = models.CharField(max_length=255, null=True)
#     attributes = models.JSONField(null=True)
#     state_id = models.IntegerField(null=True)
#     question_id = models.IntegerField(null=True)
#     job_id = models.IntegerField(null=True)
#     task_id = models.IntegerField(null=True)
#     category = models.CharField(max_length=255, null=True)
#     is_active = models.BooleanField(null=True)
#     created_at = models.DateTimeField(null=True)
#     updated_at = models.DateTimeField(null=True)
    # job_id_fk = models.IntegerField(null=True)
    # task_id_fk = models.IntegerField(null=True)
    # question_id_fk = models.IntegerField(null=True)
    # siac_id_fk = models.IntegerField(null=True)

    # def save(self, *args, **kwargs):
    #     # Generate ID: question_id#state_id#task_id#job_id
    #     self.id = f"{self.question_id}#{self.state_id}#{self.task_id}#{self.job_id}"
    #     print(self.id)
    #     # Generate config_id: id-first_char_of_siac_id
    #     if self.siac_id:
    #         print(self.siac_id)
    #         self.config_id = f"{self.id}-{str(self.siac_id)}"
    #         self.config_id = self.config_id.replace('##-1#', '#')  # Remove ##-1#
    #         self.config_id = self.config_id.replace('###-', '#')  # Remove ###-
        
    #     now_utc = timezone.now()
    #     now_india = now_utc.astimezone(INDIA_TZ)
    #     if not self.created_at:
    #         self.created_at = now_india
    #     self.updated_at = now_india
        
    #     super().save(*args, **kwargs)

    # class Meta:
    #     managed = False
    #     db_table = 'config_metas'

class JobMaster(models.Model):
    job_id = models.IntegerField(primary_key=True)
    conditions = models.JSONField(null=True)
    created_at = models.DateTimeField(null=True)
    job_name = models.CharField(max_length=255, null=True)
    order_id = models.IntegerField(null=True)
    system_identifier = models.CharField(max_length=255, null=True)
    updated_at = models.DateTimeField(null=True)
    
    def __str__(self):
        return f"{self.job_id} - {self.job_name}"

    def save(self, *args, **kwargs):
        now_utc = timezone.now()
        now_india = now_utc.astimezone(INDIA_TZ)
        if not self.created_at:
            self.created_at = now_india
        self.updated_at = now_india
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'job_master'


class ConfigMetas(models.Model):
    id = models.CharField(max_length=100)
    config_id = models.CharField(max_length=100,  primary_key=True)
    parent_question_operator = models.CharField(max_length=255, null=True)
    siac_id = models.CharField(max_length=255, null=True)
    default_option = models.JSONField(blank=True, null=True)
    parent_response_condition = models.JSONField(null=True)
    possible_options = models.JSONField(blank=True, null=True)
    enable_task_response = models.JSONField(blank=True, null=True)
    entity_type = models.CharField(max_length=255, null=True)
    parent_option_condition = models.JSONField(null=True)
    question_type = models.CharField(max_length=255, null=True)
    attributes = models.JSONField(null=True)
    state_id = models.IntegerField(null=True)
    question_id = models.IntegerField(null=True)
    job_id = models.IntegerField(null=True)
    task_id = models.IntegerField(null=True)
    category = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    skip_trigger = models.BooleanField(default=False)
    # job_id_fk = models.IntegerField(null=True)
    # task_id_fk = models.IntegerField(null=True)
    # question_id_fk = models.IntegerField(null=True)
    # siac_id_fk = models.IntegerField(null=True)

    # def save(self, *args, **kwargs):
    #     update_fields = kwargs.get('update_fields', None)

    #     # Only set id/config_id if not a partial update or those fields are being updated
    #     if not update_fields or 'id' in update_fields or 'config_id' in update_fields:
    #         self.id = f"{self.question_id}#{self.state_id}#{self.task_id}#{self.job_id}"
    #         if self.siac_id:
    #             self.config_id = f"{self.id}-{str(self.siac_id)}"
    #             self.config_id = self.config_id.replace('##-1#', '#')
    #             self.config_id = self.config_id.replace('###-', '#')

    #     now_utc = timezone.now()
    #     now_india = now_utc.astimezone(INDIA_TZ)

    #     # Only set created_at if not a partial update or it's being updated
    #     if (not update_fields or 'created_at' in update_fields) and not self.created_at:
    #         self.created_at = now_india
    #     # Always set updated_at unless it's a partial update and not being updated
    #     if not update_fields or 'updated_at' in update_fields:
    #         self.updated_at = now_india

    #     super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'config_metas'


# class JobMaster(models.Model):
#     job_id = models.IntegerField(primary_key=True)
#     conditions = models.JSONField(blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     job_name = models.CharField(max_length=255, blank=True, null=True)
#     order_id = models.IntegerField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     system_identifier = models.CharField(max_length=255, blank=True, null=True)

#     def __str__(self):
#         return f"{self.job_id} - {self.job_name}"
    
#     def save(self, *args, **kwargs):
#         now_utc = timezone.now()
#         now_india = now_utc.astimezone(INDIA_TZ)
#         if not self.created_at:
#             self.created_at = now_india
#         self.updated_at = now_india
#         if self.job_name:
#             self.system_identifier = self.job_name.upper().replace(' ', '_')
#         super().save(*args, **kwargs)

    # class Meta:
    #     managed = False
    #     db_table = 'job_master'


class QuestionMaster(models.Model):
    question_id = models.IntegerField(primary_key=True)
    question_name = models.CharField(max_length=255, blank=True, null=True)
    identifier = models.CharField(max_length=255, blank=True, null=True)
    ui_element_type = models.CharField(max_length=255, blank=True, null=True)
    possible_options = models.JSONField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    is_multi_select = models.BooleanField(blank=True, null=True)
    default_option = models.CharField(max_length=255, blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    source_category = models.CharField(max_length=255, blank=True, null=True)
    attributes = models.JSONField(blank=True, null=True)
    is_master = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.question_id} - {self.question_name}"

    def save(self, *args, **kwargs):
        now_utc = timezone.now()
        now_india = now_utc.astimezone(INDIA_TZ)
        if not self.created_at:
            self.created_at = now_india
        self.updated_at = now_india
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'question_master'


class SiacMaster(models.Model):
    siac_id = models.CharField(primary_key=True, max_length=255)
    conditions = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    scheme = models.CharField(max_length=255, blank=True, null=True)
    sector = models.CharField(max_length=255, blank=True, null=True)
    siac_uuid = models.UUIDField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'siac_master'

    def save(self, *args, **kwargs):
        now_utc = timezone.now()
        now_india = now_utc.astimezone(INDIA_TZ)
        print(now_utc,now_india)
        if not self.created_at:
            self.created_at = now_india
        self.updated_at = now_india
        super().save(*args, **kwargs)


class StateMaster(models.Model):
    state_id = models.IntegerField(primary_key=True)
    condition = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    state_name = models.CharField(max_length=255, blank=True, null=True)
    system_identifier = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.state_id} - {self.state_name}"


    def save(self, *args, **kwargs):
        now_utc = timezone.now()
        now_india = now_utc.astimezone(INDIA_TZ)
        if not self.created_at:
            self.created_at = now_india
        self.updated_at = now_india
        if self.state_name:
            self.system_identifier = self.state_name.upper().replace(' ', '_')
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'state_master'


class TaskMaster(models.Model):
    task_id = models.IntegerField(primary_key=True)
    conditions = models.JSONField(blank=True, null=True)
    mandatory = models.BooleanField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    task_name = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    system_identifier = models.CharField(max_length=255, blank=True, null=True)
    task_type = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.task_id} - {self.task_name}"
        

    def save(self, *args, **kwargs):
        now_utc = timezone.now()
        now_india = now_utc.astimezone(INDIA_TZ)
        print(now_india,now_utc)
        if not self.created_at:
            self.created_at = now_india
        self.updated_at = now_india
        if self.task_name:
            self.system_identifier = self.task_name.upper().replace(' ', '_')
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'task_master'

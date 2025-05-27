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
from liquibase_checks_python import liquibase_changesets
import sys
import pytz

INDIA_TZ = pytz.timezone('Asia/Kolkata')


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
        db_table = 'config_data"."job_master'


class ConfigMetas(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    parent_question_operator = models.CharField(max_length=255, null=True)
    siac_id = models.CharField(max_length=255, null=True)
    default_option = models.JSONField(blank=True, null=True)
    parent_response_condition = models.JSONField(null=True)
    possible_options = models.JSONField(blank=True, null=True)
    enable_task_response = models.CharField(max_length=255, null=True)
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
    # job_id_fk = models.IntegerField(null=True)
    # task_id_fk = models.IntegerField(null=True)
    # question_id_fk = models.IntegerField(null=True)
    # siac_id_fk = models.IntegerField(null=True)
    def save(self, *args, **kwargs):
        if self.question_type:
            self.question_type = self.question_type.upper()
        if self.entity_type:
            self.entity_type = self.entity_type.upper()
        super().save(*args, **kwargs)
    
    class Meta:
        managed = False
        db_table = 'config_data"."config_metas'


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
        db_table = 'config_data"."question_master'


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
        db_table = 'config_data"."siac_master'

    def save(self, *args, **kwargs):
        now_utc = timezone.now()
        now_india = now_utc.astimezone(INDIA_TZ)
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
        db_table = 'config_data"."state_master'


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
        if not self.created_at:
            self.created_at = now_india
        self.updated_at = now_india
        if self.task_name:
            self.system_identifier = self.task_name.upper().replace(' ', '_')
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'config_data"."task_master'

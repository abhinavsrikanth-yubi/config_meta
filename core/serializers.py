from rest_framework import serializers
from .models import JobMaster,QuestionMaster,TaskMaster,StateMaster, SiacMaster,ConfigMetas
import pytz

IST_TZ = pytz.timezone('Asia/Kolkata')

class ISTDateTimeSerializerMixin:
    created_at_ist = serializers.SerializerMethodField()
    updated_at_ist = serializers.SerializerMethodField()

    def get_created_at_ist(self, obj):
        if hasattr(obj, 'created_at') and obj.created_at:
            return obj.created_at.astimezone(IST_TZ).strftime('%Y-%m-%d %H:%M:%S')
        return None

    def get_updated_at_ist(self, obj):
        if hasattr(obj, 'updated_at') and obj.updated_at:
            return obj.updated_at.astimezone(IST_TZ).strftime('%Y-%m-%d %H:%M:%S')
        return None

class QuestionMasterSerializer(ISTDateTimeSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model=QuestionMaster
        fields='__all__'

class JobMasterSerializer(ISTDateTimeSerializerMixin, serializers.ModelSerializer):
    system_identifier=serializers.CharField(read_only=True)

    class Meta:
        model = JobMaster
        fields = '__all__'

class TaskMasterSerializer(ISTDateTimeSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model=TaskMaster
        fields='__all__'

class StateMasterSerializer(ISTDateTimeSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model=StateMaster
        fields='__all__'

class SiacMasterSerializer(ISTDateTimeSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model=SiacMaster
        fields='__all__'

class ConfigMetaSerializer(ISTDateTimeSerializerMixin, serializers.ModelSerializer):
    parent_option_condition = serializers.CharField(required=False)
    parent_response_condition = serializers.CharField(required=False)

    class Meta:
        model = ConfigMetas
        fields = '__all__'

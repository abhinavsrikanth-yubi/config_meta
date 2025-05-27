from django import forms
from .models import QuestionMaster, JobMaster,TaskMaster,StateMaster,SiacMaster,ConfigMetas
from django.forms import formset_factory
from django.db.models import Max

class QuestionMasterForm(forms.ModelForm):
    possible_options = forms.CharField(
        required=False,
        help_text="Enter comma-separated values (e.g., Option1,Option2,Option3)",
        widget=forms.TextInput()
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and isinstance(self.instance.possible_options, list):
            self.initial['possible_options'] = ', '.join(self.instance.possible_options)
            self.fields['possible_options'].initial = ', '.join(self.instance.possible_options)
            self.fields['question_id'].disabled = True
        else:
            max_id=QuestionMaster.objects.all().aggregate(max_id=Max('question_id'))['max_id'] or 0
            self.fields['question_id'].initial = max_id + 1
            
    UI_ELEMENT_TYPE_CHOICES = [
        ('RADIO_BUTTON', 'RADIO_BUTTON'),
        ('CHECKBOX', 'CHECKBOX'),
        ('DROPDOWN', 'DROPDOWN'),
        ('TEXT', 'TEXT'),   
        ('SINGLE_SELECT', 'SINGLE_SELECT'),
        ('MULTI_SELECT', 'MULTI_SELECT'),
    ]
    IS_ACTIVE_CHOICES = [
        ('YES', 'YES'),
        ('NO', 'NO'),
        ('UNKNOWN', 'UNKNOWN'),
    ]
    is_active = forms.ChoiceField(
        choices=IS_ACTIVE_CHOICES,
        initial='YES',
        required=True,
        label="Is Active"
    )

    ui_element_type=forms.ChoiceField(
        choices=UI_ELEMENT_TYPE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    def clean_possible_options(self):
        data = self.cleaned_data['possible_options']
        if not data:
            return []
        res = []
        for i in data.split(','):
            stripped_item = i.strip()
            if stripped_item:
                res.append(stripped_item)
        return res
    def save(self, commit=True):
        instance = super().save(commit=False)
        question_name = self.cleaned_data.get('question_name')
        if question_name:
            instance.identifier = question_name.upper().replace(' ', '_')
        if commit:
            instance.save()
            self.save_m2m()
        return instance
    class Meta:
        model=QuestionMaster
        fields=[
            'question_id',
            'question_name',
            'is_master',
            'is_active', 'is_multi_select', 'default_option', 'identifier',
            'ui_element_type', 'possible_options',
            'attributes', 
        ]

class JobMasterForm(forms.ModelForm):
    conditions = forms.CharField(
        required=False,
        help_text='Enter CSV',
        widget=forms.TextInput()
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if self.instance and self.instance.pk:
        #     value = self.instance.conditions
        #     if isinstance(value, list):
        #         self.fields['conditions'].initial = ', '.join(value)
        if self.instance and self.instance.pk and isinstance(self.instance.conditions, list):
            self.initial['conditions'] = ', '.join(self.instance.conditions)
            self.fields['conditions'].initial = ', '.join(self.instance.conditions)
            # Make job_id read-only on update
            self.fields['job_id'].disabled = True
        else:
            max_id=JobMaster.objects.all().aggregate(max_id=Max('job_id'))['max_id'] or 0
            self.fields['job_id'].initial = max_id + 1
    def clean_conditions(self):
        data = self.cleaned_data['conditions']
        if not data:
            return []
        res = []
        for i in data.split(','):
            stripped_item = i.strip()
            if stripped_item:
                res.append(stripped_item)
        return res

    def save(self, commit=True):
        instance = super().save(commit=False)
        job_name = self.cleaned_data.get('job_name')
        if job_name:
            # Set system_identifier as UPPERCASE and underscores
            instance.system_identifier = job_name.upper().replace(' ', '_')
        if commit:
            instance.save()
            self.save_m2m()
        return instance

    class Meta:
        model=JobMaster
        fields=[
            'job_id',
            'job_name',
            'conditions',
            'order_id',
            # 'created_at',  # Excluded from UI
            # 'updated_at',  # Excluded from UI
        ]

class TaskMasterForm(forms.ModelForm):
    conditions = forms.CharField(
        required=False,
        help_text='Enter CSV',
        widget=forms.TextInput()
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and isinstance(self.instance.conditions, list):
            self.initial['conditions'] = ', '.join(self.instance.conditions)
            self.fields['conditions'].initial = ', '.join(self.instance.conditions)
            self.fields['task_id'].disabled = True
        else:
            max_id=TaskMaster.objects.all().aggregate(max_id=Max('task_id'))['max_id'] or 0
            self.fields['task_id'].initial = max_id + 1
    def clean_conditions(self):
        data = self.cleaned_data['conditions']
        if not data:
            return []
        res = []
        for i in data.split(','):
            stripped_item = i.strip()
            if stripped_item:
                res.append(stripped_item)
        return res
    def save(self, commit=True):
        instance = super().save(commit=False)
        task_name = self.cleaned_data.get('task_name')
        if task_name:
            instance.system_identifier = task_name.upper().replace(' ', '_')
        if commit:
            instance.save()
            self.save_m2m()
        return instance
    class Meta:
        model = TaskMaster
        fields = [
            'task_id', 'conditions', 'mandatory', 'order_id', 'task_name', 'task_type'
        ]
    def clean_mandatory(self):
        value = self.cleaned_data.get('mandatory')
        if value is None:
            raise forms.ValidationError("Mandatory cannot be null or unknown. Please select Yes or No.")
        return value


class StateMasterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['state_id'].disabled = True
        else:
            max_id=StateMaster.objects.all().aggregate(max_id=Max('state_id'))['max_id'] or 0
            self.fields['state_id'].initial = max_id + 1
    def save(self, commit=True):
        instance = super().save(commit=False)
        state_name = self.cleaned_data.get('state_name')
        if state_name:
            instance.system_identifier = state_name.upper().replace(' ', '_')
        if commit:
            instance.save()
            self.save_m2m()
        return instance
    class Meta:
        model=StateMaster
        fields=[
            'state_id',
            'state_name',
            'description',
            #system_identifier
            #created_at
            #updated_at
        ]

class SiacMasterForm(forms.ModelForm):
    conditions = forms.CharField(
        required=False,
        help_text='Enter CSV',
        widget=forms.TextInput()
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and isinstance(self.instance.conditions, list):
            self.initial['conditions'] = ', '.join(self.instance.conditions)
            self.fields['conditions'].initial = ', '.join(self.instance.conditions)
            self.fields['siac_id'].disabled = True
        else:
            max_id=SiacMaster.objects.all().aggregate(max_id=Max('siac_id'))['max_id']
            if max_id is None:
                next_id = 1
            else:
                next_id = int(max_id) + 1
            self.fields['siac_id'].initial = next_id
                
    def clean_conditions(self):
        data = self.cleaned_data['conditions']
        if not data:
            return []
        res = []
        for i in data.split(','):
            stripped_item = i.strip()
            if stripped_item:
                res.append(stripped_item)
        return res
    def save(self, commit=True):
        instance = super().save(commit=False)
        description = self.cleaned_data.get('description')
        if description:
            instance.system_identifier = description.upper().replace(' ', '_')
        if commit:
            instance.save()
            self.save_m2m()
        return instance
    class Meta:
        model=SiacMaster
        fields=[
            'siac_id', 'conditions', 'description', 'scheme', 'sector', 'siac_uuid'
        ]

class ParentResponseForm(forms.Form):
    question = forms.ModelChoiceField(
        queryset=QuestionMaster.objects.all(),
        label='Question',
        required=True,
        empty_label='Select a Question'
    )
    answer = forms.CharField(
        label='Answer',
        required=True
    )
ParentResponseFormSet = formset_factory(ParentResponseForm, extra=3, can_delete=True)
CATEGORY_CHOICES = [
    ('ASSET CATEGORY', 'ASSET CATEGORY'),
    ('PROGRAM', 'PROGRAM'),
    ('','NONE')
]
ENTITY_TYPE_CHOICES = [
    ('CUSTOMER', 'CUSTOMER'),
    ('INVESTOR', 'INVESTOR'),
    ('','NONE')
]
QUESTION_TYPE_CHOICES = [
    ('STATIC', 'STATIC'),
    ('DYNAMIC', 'DYNAMIC'),
    ('','NONE')
]
TASK_RESPONSE_CHOICES= [
    ('YUBI','YUBI'),
    ('NO WILL RELY ON YUBI','NO WILL RELY ON YUBI'),
    ('','NONE')
]
class ConfigMetaForm(forms.ModelForm):
    default_option = forms.CharField(
        label='Default Option',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    is_active = forms.TypedChoiceField(
        label='Is active',
        choices=[(True, 'Yes'), (False, 'No')],
        coerce=lambda x: x == 'True',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    enable_task_response = forms.ChoiceField(
        choices=TASK_RESPONSE_CHOICES,
        required=False,
        label='Enable Task Response',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        required=True,
        initial='ASSET CATEGORY',
        label='Category',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    entity_type = forms.ChoiceField(
        choices=ENTITY_TYPE_CHOICES,
        required=True,
        initial='INVESTOR',
        label='Entity Type',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    question_type = forms.ChoiceField(
        choices=QUESTION_TYPE_CHOICES,
        required=True,
        initial='STATIC',
        label='Question Type',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    id = forms.CharField(
        label='Config ID',
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
# {{ ... }}
    question_id = forms.ChoiceField(
        # queryset=QuestionMaster.objects.all(),
        choices=[('-1', '-1 - None')] + [(str(q.question_id), f"{q.question_id} - {q.question_name}") for q in QuestionMaster.objects.all()],
        label='Question',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    state_id = forms.ChoiceField(
        # queryset=StateMaster.objects.all(),
        choices=[('-1', '-1 - None')] + [(str(s.state_id), f"{s.state_id} - {s.state_name}") for s in StateMaster.objects.all()],
        label='State',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    job_id = forms.ChoiceField(
        # queryset=JobMaster.objects.all(),
        choices=[('-1', '-1 - None')] + [(str(j.job_id), f"{j.job_id} - {j.job_name}") for j in JobMaster.objects.all()],
        label='Job',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    task_id = forms.ChoiceField(
        # queryset=TaskMaster.objects.all(),
        choices=[('-1', '-1 - None')] + [(str(t.task_id), f"{t.task_id} - {t.task_name}") for t in TaskMaster.objects.all()],
        label='Task',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate choices for all dropdowns
        self.fields['siac_id'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['question_id'].choices = [('-1', '-1 - None')] + [
            (str(q.question_id), f"{q.question_id} - {q.question_name}") for q in QuestionMaster.objects.all()
        ]
        self.fields['state_id'].choices = [('-1', '-1 - None')] + [
            (str(s.state_id), f"{s.state_id} - {s.state_name}") for s in StateMaster.objects.all()
        ]
        self.fields['job_id'].choices = [('-1', '-1 - None')] + [
            (str(j.job_id), f"{j.job_id} - {j.job_name}") for j in JobMaster.objects.all()
        ]
        self.fields['task_id'].choices = [('-1', '-1 - None')] + [
            (str(t.task_id), f"{t.task_id} - {t.task_name}") for t in TaskMaster.objects.all()
        ]
        # Render possible_options as CSV string for UI
        if self.instance and self.instance.pk and isinstance(self.instance.possible_options, list):
            self.initial['possible_options'] = ', '.join(self.instance.possible_options)
            self.fields['possible_options'].initial = ', '.join(self.instance.possible_options)
        # Render siac_id as CSV string for UI
        if self.instance and self.instance.pk and isinstance(self.instance.siac_id, list):
            self.initial['siac_id'] = str(self.instance.siac_id)
            self.fields['siac_id'].initial = str(self.instance.siac_id)
        if self.instance and self.instance.pk:
            self.fields['id'].initial = self.instance.id
            self.fields['id'].disabled = True
            self.fields['question_id'].initial = self.instance.question_id
            self.fields['state_id'].initial = self.instance.state_id
            self.fields['job_id'].initial = self.instance.job_id
            self.fields['task_id'].initial = self.instance.task_id

            if isinstance(self.instance.possible_options, list):
                self.fields['possible_options'].initial = ', '.join(self.instance.possible_options)
    
    def clean_possible_options(self):
        data = self.cleaned_data.get('possible_options', '')
        if not data:
            return []
        # Accept both CSV string and list (for update)
        if isinstance(data, list):
            return [str(i).strip() for i in data if str(i).strip()]
        # Remove quotes and brackets if user pasted a list-like string
        data = data.replace('[','').replace(']','').replace("'",'').replace('"','')
        return [i.strip() for i in data.split(',') if i.strip()]

    siac_id = forms.CharField(
        label='SIAC IDs',
        help_text='Enter comma-separated SIAC IDs (e.g., 1,2,3,4)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    possible_options = forms.CharField(
        label='Possible Options',
        help_text='Enter comma-separated values',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    parent_option_condition = forms.CharField(
        label='Parent Option Condition',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    parent_question_operator = forms.CharField(
        label='Parent Question Operator',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    attributes = forms.CharField(
        label='Attributes',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )


    def clean_possible_options_for_rendering(self):
        data = self.cleaned_data['possible_options']
        # Convert "yes, no, additional" -> ['Yes', 'No', 'additional']
        if isinstance(data, str):
            options = [opt.strip().capitalize() for opt in data.split(',') if opt.strip()]
            return options
        return data

    def initial_possible_options(self):
        # For initial display: convert list to CSV string
        val = self.instance.possible_options
        if isinstance(val, list):
            return ', '.join(val)
        elif isinstance(val, str):
            # If it's a string in DB, just show as is
            return val
        return ''

    def clean_siac_id(self):
        data = self.cleaned_data['siac_id']
        # Optionally, validate CSV format or strip whitespace
        return data.strip() if data else ''


    # def clean_siac_id(self):
    #     data = self.cleaned_data.get('siac_id', '')
    #     # If it's already a list, clean each item
    #     if isinstance(data, list):
    #         return [str(s).strip() for s in data if s]
    #     # If it's a string, split by commas and clean each item
    #     if isinstance(data, str):
    #         # Clean any brackets or quotes
    #         clean_data = str(data).replace('[', '').replace(']', '').replace('"', '').strip()
    #         if clean_data:
    #             return [str(s).strip() for s in clean_data.split(',') if s.strip()]
    #         return []
    #     return []

    def clean_parent_response_condition(self):
        data = self.cleaned_data.get('parent_response_condition', '')
        if not data:
            return {}
        res = {}
        for item in data.split(','):
            stripped_item = item.strip()
            if stripped_item:
                try:
                    number, response = stripped_item.split(':')
                    number = int(number.strip())
                    response = response.strip()
                    res[number] = response
                except ValueError:
                    continue
        return res

    def clean_parent_option_condition(self):
        data = self.cleaned_data.get('parent_option_condition', '')
        if not data:
            return {}
        condition_dict = {}
        for item in data.split(','):
            item = item.strip()
            if item:
                try:
                    key, value = item.split(':')
                    key = key.strip()
                    value = value.strip()
                    condition_dict[key] = value
                except ValueError:
                    continue
        return condition_dict

    def clean_attributes(self):
        data = self.cleaned_data.get('attributes', '')
        if not data:
            return {}
        attr_dict = {}
        for item in data.split(','):
            item = item.strip()
            if item:
                try:
                    key, value = item.split(':')
                    key = key.strip()
                    value = value.strip()
                    attr_dict[key] = value
                except ValueError:
                    continue
        return attr_dict

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Always store possible_options as a list
        if isinstance(self.cleaned_data.get('possible_options'), list):
            instance.possible_options = self.cleaned_data['possible_options']
        # Always store siac_id as a list of ints
        if isinstance(self.cleaned_data.get('siac_id'), list):
            instance.siac_id = self.cleaned_data['siac_id']
        if commit:
            instance.save()
            self.save_m2m()
        return instance

    def clean_question_id(self):
        value = self.cleaned_data['question_id']
        if hasattr(value, 'pk'):
            return value.pk
        return int(value) if value else None


    def clean_task_id(self):
        value = self.cleaned_data['task_id']
        if hasattr(value, 'pk'):
            return value.pk
        return int(value) if value else None

    def clean_job_id(self):
        value = self.cleaned_data['job_id']
        if hasattr(value, 'pk'):
            return value.pk
        return int(value) if value else None

    def clean_state_id(self):
        value = self.cleaned_data['state_id']
        if hasattr(value, 'pk'):
            return value.pk
        return int(value) if value else None


    class Meta:
        model = ConfigMetas
        fields = [
            'id', 'question_id', 'task_id', 'job_id', 'state_id',
            'siac_id', 'possible_options', 'parent_option_condition',
            'parent_question_operator', 'category', 'enable_task_response',
            'entity_type', 'question_type', 'attributes', 'is_active'
        ]
        widgets = {
            'parent_option_condition': forms.Textarea(attrs={'class': 'form-control', 'required': False}),
            'parent_question_operator': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'entity_type': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'question_type': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'attributes': forms.Textarea(attrs={'class': 'form-control', 'required': False}),
        }
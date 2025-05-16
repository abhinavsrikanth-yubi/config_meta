from django import forms
from .models import QuestionMaster, JobMaster,TaskMaster,StateMaster,SiacMaster,ConfigMetas
from django.forms import formset_factory

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
            'is_active', 'is_multi_select', 'default_option', 'identifier',
            'question_name', 'ui_element_type', 'possible_options', 'order_id',
            'source_category', 'attributes', 'question_id', 'is_master'
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
        print('Initial conditions:', self.fields['conditions'].initial)
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


class StateMasterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['state_id'].disabled = True
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
class ConfigMetaForm(forms.ModelForm):
    enable_task_response = forms.TypedChoiceField(
        label='Enable Task Response',
        choices=[(True, 'Yes'), (False, 'No')],
        coerce=lambda x: x == 'True',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    is_active = forms.TypedChoiceField(
        label='Is active',
        choices=[(True, 'Yes'), (False, 'No')],
        coerce=lambda x: x == 'True',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    skip_trigger = forms.TypedChoiceField(
        label='Skip Trigger',
        choices=[(True, 'Yes'), (False, 'No')],
        coerce=lambda x: x == 'True',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    config_id = forms.CharField(
        label='Config ID',
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
# {{ ... }}
    question_id = forms.ModelChoiceField(
        queryset=QuestionMaster.objects.all(),
        label='Question',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    state_id = forms.ModelChoiceField(
        queryset=StateMaster.objects.all(),
        label='State',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    job_id = forms.ModelChoiceField(
        queryset=JobMaster.objects.all(),
        label='Job',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    task_id = forms.ModelChoiceField(
        queryset=TaskMaster.objects.all(),
        label='Task',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate choices for all dropdowns
        self.fields['question_id'].choices = [
            (q.question_id, f"{q.question_id} - {q.question_name}") for q in QuestionMaster.objects.all()
        ]
        self.fields['state_id'].choices = [
            (s.state_id, f"{s.state_id} - {s.state_name}") for s in StateMaster.objects.all()
        ]
        self.fields['job_id'].choices = [
            (j.job_id, f"{j.job_id} - {j.job_name}") for j in JobMaster.objects.all()
        ]
        self.fields['task_id'].choices = [
            (t.task_id, f"{t.task_id} - {t.task_name}") for t in TaskMaster.objects.all()
        ]
        # Render possible_options as CSV string for UI
        if self.instance and self.instance.pk and isinstance(self.instance.possible_options, list):
            self.initial['possible_options'] = ', '.join(self.instance.possible_options)
            self.fields['possible_options'].initial = ', '.join(self.instance.possible_options)
        # Render siac_id as CSV string for UI
        if self.instance and self.instance.pk and isinstance(self.instance.siac_id, list):
            self.initial['siac_id'] = ', '.join(str(i) for i in self.instance.siac_id)
            self.fields['siac_id'].initial = ', '.join(str(i) for i in self.instance.siac_id)
        if self.instance and self.instance.pk:
            self.fields['config_id'].initial = self.instance.config_id
            self.fields['config_id'].disabled = True
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

    def clean_siac_id(self):
        data = self.cleaned_data.get('siac_id', '')
        if isinstance(data, list):
            return [int(i) for i in data if str(i).strip()]
        if not data:
            return []
        # Remove brackets if user pasted a list-like string
        data = data.replace('[','').replace(']','')
        return [int(i.strip()) for i in data.split(',') if i.strip().isdigit()]
    
    #     self.fields['question_id'].label_from_instance = lambda obj: f"{obj.question_id} - {obj.question_name}"
    #     self.fields['state_id'].label_from_instance = lambda obj: f"{obj.state_id} - {obj.state_name}"
    #     self.fields['job_id'].label_from_instance = lambda obj: f"{obj.job_id} - {obj.job_name}"
    #     self.fields['task_id'].label_from_instance = lambda obj: f"{obj.task_id} - {obj.task_name}"
    #     if self.instance and self.instance.pk:
    #         self.fields['config_id'].initial = self.instance.config_id
    #         self.fields['config_id'].disabled = True
    #         # Set initial to the PK for integer fields, or the related object for FKs
    #         self.fields['question_id'].initial = self.instance.question_id.pk if hasattr(self.instance.question_id, 'pk') else self.instance.question_id
    #         self.fields['state_id'].initial = self.instance.state_id.pk if hasattr(self.instance.state_id, 'pk') else self.instance.state_id
    #         self.fields['job_id'].initial = self.instance.job_id.pk if hasattr(self.instance.job_id, 'pk') else self.instance.job_id
    #         self.fields['task_id'].initial = self.instance.task_id.pk if hasattr(self.instance.task_id, 'pk') else self.instance.task_id
    #         if isinstance(self.instance.siac_id, list):
    #             self.fields['siac_id'].initial = ', '.join(map(str, self.instance.siac_id))
    #         if isinstance(self.instance.possible_options, list):
    #             self.fields['possible_options'].initial = ', '.join(self.instance.possible_options)

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
    question_type = forms.CharField(
        label='Question Type',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    attributes = forms.CharField(
        label='Attributes',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.instance and self.instance.pk:
    #         self.fields['config_id'].initial = self.instance.config_id
    #         self.fields['config_id'].disabled = True
    #         if isinstance(self.instance.siac_id, list):
    #             self.fields['siac_id'].initial = ', '.join(map(str, self.instance.siac_id))
    #         if isinstance(self.instance.possible_options, list):
    #             self.fields['possible_options'].initial = ', '.join(self.instance.possible_options)

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
        data = self.cleaned_data.get('siac_id', '')
        # If it's already a list, clean each item
        if isinstance(data, list):
            return [str(s).strip() for s in data if s]
        # If it's a string, split by commas and clean each item
        if isinstance(data, str):
            # Clean any brackets or quotes
            clean_data = str(data).replace('[', '').replace(']', '').replace('"', '').strip()
            if clean_data:
                return [str(s).strip() for s in clean_data.split(',') if s.strip()]
            return []
        return []

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
            'config_id', 'question_id', 'task_id', 'job_id', 'state_id',
            'siac_id', 'possible_options', 'parent_option_condition',
            'parent_question_operator', 'category', 'enable_task_response',
            'entity_type', 'question_type', 'attributes', 'is_active', 'skip_trigger'
        ]
        widgets = {
            
            'parent_option_condition': forms.Textarea(attrs={'class': 'form-control', 'required': False}),
            'parent_question_operator': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'entity_type': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'question_type': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'attributes': forms.Textarea(attrs={'class': 'form-control', 'required': False}),
        }
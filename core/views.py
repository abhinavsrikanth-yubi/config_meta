from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import QuestionMasterForm, JobMasterForm,TaskMasterForm,StateMasterForm,SiacMasterForm,ConfigMetaForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import JobMaster, TaskMaster, StateMaster,SiacMaster, ConfigMetas, QuestionMaster
from .serializers import JobMasterSerializer, QuestionMasterSerializer, TaskMasterSerializer, StateMasterSerializer,SiacMasterSerializer, ConfigMetaSerializer
from django.db import IntegrityError
from .forms import ConfigMetaForm, ParentResponseFormSet
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from core.utils.liquibase_changelog import LiquibaseChangelogMixin
import os
from django.conf import settings
from threading import Lock
from core.utils.liquibase_changelog import CHANGELOG_DIR
import shutil


@login_required
def index(request):
    return render(request, 'index.html')

def is_product(user):
    return user.groups.filter(name='Product').exists()


def get_master_results(request):
    """Display results for existing masters"""
    # Fetch all master records
    masters = {
        'Job Masters': JobMaster.objects.all(),
        'Question Masters': QuestionMaster.objects.all(),
        'State Masters': StateMaster.objects.all(),
        'Task Masters': TaskMaster.objects.all(),
        'SIAC Masters': SiacMaster.objects.all(),
        'Config Metas': ConfigMetas.objects.all()
    }
    
    return render(request, 'get_results.html', {'masters': masters})


def handle_master_form(form_class, template_name, request):
    """Common handler for all master forms"""
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            # Check if the ID already exists
            model = form_class.Meta.model
            pk_field = form_class.Meta.fields[0]  # First field is always the PK
            pk_value = form.cleaned_data[pk_field]
            
            if model.objects.filter(**{pk_field: pk_value}).exists():
                # Redirect to get page
                return redirect('get_results')
            
            form.save()
            messages.success(request, f'Successfully saved {model.__name__} with ID {pk_value}')
            return redirect('index')
    else:
        form = form_class()
    
    return render(request, template_name, {'form': form})

def question_master_view(request):
    if request.method == 'POST':
        form = QuestionMasterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question Master entry created/updated successfully!')
            return redirect('question_master')
    else:
        form = QuestionMasterForm()
    return render(request, 'createpages/question.html', {'form': form})
    if not request.user.groups.filter(name='product').exists():
        return HttpResponseForbidden("You do not have permission to create configs.")

# List view for all jobs
# from django.shortcuts import get_object_or_404
@login_required
def job_list_view(request):
    jobs = JobMaster.objects.all()
    return render(request, 'viewpages/job_view.html', {'jobs': jobs})

# Read-only detail view
@login_required
def job_detail_view(request, pk):
    job = get_object_or_404(JobMaster, job_id=pk)
    return render(request, 'detailing/job_detail.html', {'job': job})

# Unified create/update view
@user_passes_test(is_product)
@login_required
def job_master_view(request, pk=None):
    if pk:
        job = get_object_or_404(JobMaster, job_id=pk)
        is_update = True
    else:
        job = None
        is_update = False
    if request.method == 'POST':
        form = JobMasterForm(request.POST, instance=job)
        if form.is_valid():
            mixin = LiquibaseChangelogMixin()
            # Check for changes if updating
            if pk:
                #update
                has_changed = False
                changed_fields = []
                for field in form.changed_data:
                    # Exclude job_id since it's disabled
                    if field != 'job_id':
                        has_changed = True
                        changed_fields.append(field)
                        break
                if not has_changed:
                    messages.info(request, 'No edits made.')
                else:
                    job_obj = form.save()
                    username = request.user.username if request.user.is_authenticated else 'frontend'
                    mixin.append_liquibase_changeset('update', job_obj, changed_fields, username=username, request=request)
                    messages.success(request, 'Job Master entry updated successfully!')
                form = JobMasterForm(instance=job)
            else:
                job_obj = form.save()
                username = request.user.username if request.user.is_authenticated else 'frontend'
                mixin.append_liquibase_changeset('insert', job_obj, username=username, request=request)
                messages.success(request, 'Job Master entry created successfully!')
                form = JobMasterForm()  # blank form after create
    else:
        form = JobMasterForm(instance=job)
    return render(request, 'createpages/job.html', {'form': form, 'job': job, 'is_update': is_update})
    if not request.user.groups.filter(name='product').exists():
        return HttpResponseForbidden("You do not have permission to create configs.")


from django.shortcuts import get_object_or_404

# --- Task Master ---
@login_required
def task_list_view(request):
    tasks = TaskMaster.objects.all()
    return render(request, 'viewpages/task_view.html', {'tasks': tasks})
@login_required
def task_detail_view(request, pk):
    task = get_object_or_404(TaskMaster, task_id=pk)
    return render(request, 'detailing/task_detail.html', {'task': task})

@user_passes_test(is_product)
@login_required
def task_master_view(request, pk=None):
    if pk:
        task = get_object_or_404(TaskMaster, task_id=pk)
        is_update = True
    else:
        task = None
        is_update = False

    if request.method == 'POST':
        form = TaskMasterForm(request.POST, instance=task)
        if form.is_valid():
            mixin = LiquibaseChangelogMixin()
            if pk:
                # update
                has_changed = False
                changed_fields = []
                for field in form.changed_data:
                    if field != 'task_id':
                        has_changed = True
                        changed_fields.append(field)
                if not has_changed:
                    messages.info(request, 'No edits made.')
                else:
                    task_obj = form.save()
                    username = request.user.username if request.user.is_authenticated else 'frontend'
                    mixin.append_liquibase_changeset('update', task_obj, changed_fields, username=username, request=request)
                    messages.success(request, 'Task Master entry updated successfully!')
                form = TaskMasterForm(instance=task)
            else:
                # create
                task_obj = form.save()
                username = request.user.username if request.user.is_authenticated else 'frontend'
                mixin.append_liquibase_changeset('insert', task_obj, username=username, request=request)
                messages.success(request, 'Task Master entry created successfully!')
                form = TaskMasterForm()  # blank form after create
    else:
        form = TaskMasterForm(instance=task)
    return render(request, 'createpages/task.html', {'form': form, 'task': task, 'is_update': is_update})   
# --- State Master ---
@login_required
def state_list_view(request):
    states = StateMaster.objects.all()
    return render(request, 'viewpages/state_view.html', {'states': states})

@login_required
def state_detail_view(request, pk):
    state = get_object_or_404(StateMaster, state_id=pk)
    return render(request, 'detailing/state_detail.html', {'state': state})

@user_passes_test(is_product)
@login_required
def state_master_view(request, pk=None):
    if pk:
        state = get_object_or_404(StateMaster, state_id=pk)
        is_update = True
    else:
        state = None
        is_update = False
    if request.method == 'POST':
        form = StateMasterForm(request.POST, instance=state)
        if form.is_valid():
            mixin = LiquibaseChangelogMixin()
            if pk:
                #update
                has_changed = False
                changed_fields = []
                for field in form.changed_data:
                    if field != 'state_id':
                        has_changed = True
                        changed_fields.append(field)
                        break
                if not has_changed:
                    messages.info(request, 'No edits made.')
                else:
                    state_obj = form.save()
                    username = request.user.username if request.user.is_authenticated else 'frontend'
                    mixin.append_liquibase_changeset('update', state_obj, changed_fields, username=username, request=request)
                    messages.success(request, 'State Master entry updated successfully!')
                form = StateMasterForm(instance=state)
            else:
                #create
                state_obj = form.save()
                username = request.user.username if request.user.is_authenticated else 'frontend'
                mixin.append_liquibase_changeset('insert', state_obj, username=username, request=request)
                messages.success(request, 'State Master entry created successfully!')
                form = StateMasterForm()  # blank form after create
    else:
        form = StateMasterForm(instance=state)
    return render(request, 'createpages/state.html', {'form': form, 'state': state, 'is_update': is_update})
    if not request.user.groups.filter(name='product').exists():
        return HttpResponseForbidden("You do not have permission to create configs.")

# --- SIAC Master ---
@login_required
def siac_list_view(request):
    siacs = SiacMaster.objects.all()
    return render(request, 'viewpages/siac_view.html', {'siacs': siacs})
@login_required
def siac_detail_view(request, pk):
    siac = get_object_or_404(SiacMaster, siac_id=pk)
    return render(request, 'detailing/siac_detail.html', {'siac': siac})

@user_passes_test(is_product)
@login_required
def siac_master_view(request, pk=None):
    if pk:
        siac = get_object_or_404(SiacMaster, siac_id=pk)
        is_update = True
    else:
        siac = None
        is_update = False
    if request.method == 'POST':
        form = SiacMasterForm(request.POST, instance=siac)
        if form.is_valid():
            mixin = LiquibaseChangelogMixin()
            if pk:
                #update
                has_changed = False
                changed_fields = []
                for field in form.changed_data:
                    if field != 'siac_id':
                        has_changed = True
                        changed_fields.append(field)
                        break
                if not has_changed:
                    messages.info(request, 'No edits made.')
                else:
                    siac_obj = form.save()
                    username = request.user.username if request.user.is_authenticated else 'frontend'
                    mixin.append_liquibase_changeset('update', siac_obj, changed_fields, username=username, request=request)
                    messages.success(request, 'SIAC Master entry updated successfully!')
                form = SiacMasterForm(instance=siac)
            else:
                #create
                siac_obj = form.save()
                username = request.user.username if request.user.is_authenticated else 'frontend'
                mixin.append_liquibase_changeset('insert', siac_obj, username=username, request=request)
                messages.success(request, 'SIAC Master entry created successfully!')
                form = SiacMasterForm()  # blank form after create
    else:
        form = SiacMasterForm(instance=siac)
    return render(request, 'createpages/siac.html', {'form': form, 'siac': siac, 'is_update': is_update})
    if not request.user.groups.filter(name='product').exists():
        return HttpResponseForbidden("You do not have permission to create configs.")

# --- Question Master ---
def question_list_view(request):
    questions = QuestionMaster.objects.all()
    return render(request, 'viewpages/question_view.html', {'questions': questions})

def question_detail_view(request, pk):
    question = get_object_or_404(QuestionMaster, question_id=pk)
    return render(request, 'detailing/question_detail.html', {'question': question})

@user_passes_test(is_product)
@login_required
def question_master_view(request, pk=None):
    if pk:
        question = get_object_or_404(QuestionMaster, question_id=pk)
        is_update = True
    else:
        question = None
        is_update = False
    if request.method == 'POST':
        form = QuestionMasterForm(request.POST, instance=question)
        if form.is_valid():
            mixin = LiquibaseChangelogMixin()
            if pk:
                #update
                has_changed = False
                changed_fields = []
                for field in form.changed_data:
                    if field != 'question_id':
                        has_changed = True
                        changed_fields.append(field)
                        break
                if not has_changed:
                    messages.info(request, 'No edits made.')
                else:
                    question_obj = form.save()
                    username = request.user.username if request.user.is_authenticated else 'frontend'
                    mixin.append_liquibase_changeset('update', question_obj, changed_fields, username=username, request=request)
                    messages.success(request, 'Question Master entry updated successfully!')
                form = QuestionMasterForm(instance=question)
            else:
                #create
                question_obj = form.save()
                username = request.user.username if request.user.is_authenticated else 'frontend'
                mixin.append_liquibase_changeset('insert', question_obj, username=username, request=request)
                messages.success(request, 'Question Master entry created successfully!')
                form = QuestionMasterForm()  # blank form after create
    else:
        form = QuestionMasterForm(instance=question)
    return render(request, 'createpages/question.html', {'form': form, 'question': question, 'is_update': is_update})
    if not request.user.groups.filter(name='product').exists():
        return HttpResponseForbidden("You do not have permission to create configs.")


# --- Config Master ---
@login_required
def config_redirect_view(request):
    return redirect('config_list')
@login_required
def config_list_view(request):
    # (Unchanged main view for initial load)
    siac = request.GET.get('siac', '').strip()
    state = request.GET.get('state', '').strip()
    id = request.GET.get('id', '').strip()
    question_id = request.GET.get('question_id', '').strip()
    task_id = request.GET.get('task_id', '').strip()
    job_id = request.GET.get('job_id', '').strip()

    configs = ConfigMetas.objects.all()
    if siac:
        configs = configs.filter(siac_id__icontains=siac)
    if state:
        configs = configs.filter(state_id__icontains=state)
    if id:
        configs = configs.filter(id__icontains=id)
    if question_id:
        configs = configs.filter(question_id__icontains=question_id)
    if task_id:
        configs = configs.filter(task_id__icontains=task_id)
    if job_id:
        configs = configs.filter(job_id__icontains=job_id)

    configs = configs.exclude(id__contains='None').exclude(id__isnull=True).exclude(id='')
    configs = configs.order_by('id')
    paginator = Paginator(configs, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'viewpages/config_view.html', {
        'configs': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'search': {
            'siac': siac,
            'state': state,
            'id': id,
            'question_id': question_id,
            'task_id': task_id,
            'job_id': job_id,
        }
    })

# AJAX endpoint for config search and pagination
from django.forms.models import model_to_dict
from django.db.models.functions import Cast
from django.db.models import CharField, Q

#question_search

def question_search_api(request):
    q = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))
    per_page = 10

    questions = QuestionMaster.objects.all()
    if q:
        questions = questions.filter(
            Q(question_id__icontains=q) | Q(question_name__icontains=q)
        )

    total = questions.count()
    start = (page - 1) * per_page
    end = start + per_page
    results = [
        {
            "id": q.question_id,
            "label": f"{q.question_id} - {q.question_name}",
        }
        for q in questions[start:end]
    ]
    num_pages = (total + per_page - 1) // per_page

    return JsonResponse({
        "results": results,
        "current_page": page,
        "num_pages": num_pages,
        "total": total,
    })


#config_search
def config_search_api(request):
    siac = request.GET.get('siac', '').strip()
    state = request.GET.get('state', '').strip()
    question_id = request.GET.get('question_id', '').strip()
    task_id = request.GET.get('task_id', '').strip()
    job_id = request.GET.get('job_id', '').strip()
    id = request.GET.get('id', '').strip()
    page = int(request.GET.get('page', 1))

    configs = ConfigMetas.objects.all()
    # SIAC: id only
    if siac:
        configs = configs.filter(siac_id=siac)
    # State: id only
    if state:
        configs = configs.filter(state_id=int(state_id))
    # Question: id only
    if question_id:
        configs = configs.filter(question_id=int(question_id))
    # Task: id only
    if task_id:
        configs = configs.filter(task_id=int(task_id))
    # Job: id only
    if job_id:
        configs = configs.filter(job_id=int(job_id))
    # Config ID: string match
    if id:
        configs = configs.filter(id__icontains=id)
    configs = configs.exclude(id__contains='None').exclude(id__isnull=True).exclude(id='')
    configs = configs.order_by('id')
    paginator = Paginator(configs, 10)
    page_obj = paginator.get_page(page)

    results = []
    for config in page_obj:
        siac_val = config.siac_id
        if isinstance(siac_val, list):
            siac_val = ", ".join(map(str, siac_val))
        id_val = getattr(config, 'id', None)
        if id_val and isinstance(id_val, str) and id_val.strip():
            results.append({
                "id": id_val,
                "state_id": config.state_id,
                "siac_id": siac_val,
                "question_id": config.question_id,
                "task_id": config.task_id,
                "job_id": config.job_id,
            })
    return JsonResponse({
        "results": results,
        "current_page": page_obj.number,
        "num_pages": paginator.num_pages,
    })
    if not request.user.groups.filter(name='product').exists():
        return HttpResponseForbidden("You do not have permission to create configs.")
@login_required
def config_detail_view(request, pk):
    config = get_object_or_404(ConfigMetas, id=pk)
    return render(request, 'detailing/config_detail.html', {'config': config})

@user_passes_test(is_product)
@login_required
def config_create_view(request):
    from .models import QuestionMaster
    questions = QuestionMaster.objects.all()
    if request.method == 'POST':
        form = ConfigMetaForm(request.POST)
        parent_questions = request.POST.getlist('parent_question')
        parent_responses = request.POST.getlist('parent_response')
        parent_response_dict = {}
        for q, r in zip(parent_questions, parent_responses):
            if q and r:
                parent_response_dict.setdefault(q, []).append(r)
        possible_options_raw = request.POST.get('possible_options', '')
        possible_options_list = [opt.strip() for opt in possible_options_raw.split(',') if opt.strip()]
        default_option_raw = request.POST.get('default_option', '')
        default_option_list = [opt.strip() for opt in default_option_raw.split(',') if opt.strip()]
        siac_ids_raw = request.POST.get('siac_id', '')
        siac_ids = [sid.strip() for sid in siac_ids_raw.split(',') if sid.strip()]
        if form.is_valid():
            mixin = LiquibaseChangelogMixin()
            created_configs = []
            duplicate_configs = []
            question_id = form.cleaned_data.get('question_id')
            state_id = form.cleaned_data.get('state_id')
            if state_id is not None:
                state_id = int(state_id)
            task_id = form.cleaned_data.get('task_id')
            job_id = form.cleaned_data.get('job_id')
            generated_id = f"{question_id}#{state_id}#{task_id}#{job_id}"
            now = timezone.now()
            for siac_id in siac_ids:
                config_id_str = f"{generated_id}-{siac_id}"
                if ConfigMetas.objects.filter(id=config_id_str).exists():
                    duplicate_configs.append(config_id_str)
                    continue
                config=ConfigMetas.objects.create(
                    id=config_id_str,
                    siac_id=siac_id,  # store as string
                    state_id=state_id,
                    question_id=question_id,
                    job_id=job_id,
                    task_id=task_id,
                    possible_options=possible_options_list,
                    default_option=default_option_list,
                    parent_option_condition=form.cleaned_data.get('parent_option_condition'),
                    parent_response_condition=parent_response_dict,
                    parent_question_operator=form.cleaned_data.get('parent_question_operator'),
                    category=form.cleaned_data.get('category'),
                    enable_task_response=form.cleaned_data.get('enable_task_response'),
                    entity_type=form.cleaned_data.get('entity_type'),
                    question_type=form.cleaned_data.get('question_type'),
                    attributes=form.cleaned_data.get('attributes'),
                    is_active=form.cleaned_data.get('is_active'),
                    created_at=now,
                    updated_at=now,
                )
                created_configs.append(config_id_str)
                username = request.user.username if request.user.is_authenticated else 'frontend'
                mixin.append_liquibase_changeset('insert', config, username=username, request=request)
            if created_configs:
                messages.success(request, f"Created configs: {', '.join(created_configs)}")
            if duplicate_configs:
                messages.error(request, f"Duplicate config_id(s) not created: {', '.join(duplicate_configs)}")
            if created_configs:
                return redirect('config_update', pk=created_configs[0])
        else:
            messages.error(request, "Form validation failed")
        # Normalize siac_id and possible_options for re-rendering
        initial = {}
        if siac_ids:
            initial['siac_id'] = ', '.join(str(x) for x in siac_ids)
        if possible_options_list:
            initial['possible_options'] = ', '.join(possible_options_list)
        form = ConfigMetaForm(request.POST, initial=initial)
        return render(request, 'createpages/config.html', {
            'form': form,
            'is_update': False,
            'parent_response_items': parent_response_dict,
            'questions': questions,
        })
    else:
        form = ConfigMetaForm()
        return render(request, 'createpages/config.html', {
            'form': form,
            'is_update': False,
            'parent_response_items': {},
            'questions': questions,
        })

@user_passes_test(is_product)
@login_required
def config_update_view(request, pk):
    questions = QuestionMaster.objects.all()
    config = get_object_or_404(ConfigMetas, id=pk)
    parent_response_items={}
    if config.parent_response_condition:
        for qid, responses in config.parent_response_condition.items():
            if str(qid) == "-1":
                question_name = "None"
            else:
                try:
                    question = QuestionMaster.objects.get(question_id=qid)
                    question_name = question.question_name
                except QuestionMaster.DoesNotExist:
                    question_name = "Unknown"
            parent_response_items[qid] = {
                "question_name": question_name,
                "responses": responses
            }

    if request.method == 'POST':
        form = ConfigMetaForm(request.POST, instance=config)
        existing_dict = config.parent_response_condition.copy() if config.parent_response_condition else {}
        parent_questions = request.POST.getlist('parent_question')
        parent_responses = request.POST.getlist('parent_response')
        parent_response_dict = {}
        for q, r in zip(parent_questions, parent_responses):
            if q and r:
                parent_response_dict.setdefault(q, []).append(r)
        for q, responses in parent_response_dict.items():
            if existing_dict.get(q) != responses:
                existing_dict[q] = responses
        default_option_raw = request.POST.get('default_option', '')
        default_option_list = [opt.strip() for opt in default_option_raw.split(',') if opt.strip()]
        possible_options_raw = request.POST.get('possible_options', '')
        possible_options_list = [opt.strip() for opt in possible_options_raw.split(',') if opt.strip()]
        siac_ids_raw = request.POST.get('siac_id', '')
        siac_ids = [sid.strip() for sid in siac_ids_raw.split(',') if sid.strip()]
        question_id = form.data.get('question_id') or form.initial.get('question_id')
        state_id = form.data.get('state_id') or form.initial.get('state_id')
        task_id = form.data.get('task_id') or form.initial.get('task_id')
        job_id = form.data.get('job_id') or form.initial.get('job_id')
        generated_id = f"{question_id}#{state_id}#{task_id}#{job_id}"
        now = timezone.now()
        if form.is_valid():
            mixin = LiquibaseChangelogMixin()
            updated_configs = []
            created_configs = []
            # Find all existing configs for this base config (excluding siac_id)
            base_configs_qs = ConfigMetas.objects.filter(id=generated_id)
            # Track SIAC IDs that should remain
            updated_siac_ids = set()
            for siac_id in siac_ids:
                config_id_str = f"{generated_id}-{siac_id}"
                obj, created = ConfigMetas.objects.update_or_create(
                    id=config_id_str,
                    defaults={
                        'id': generated_id,
                        'siac_id': siac_id,
                        'state_id': state_id,
                        'question_id': question_id,
                        'job_id': job_id,
                        'task_id': task_id,
                        'possible_options': possible_options_list,
                        'default_option': default_option_list,
                        'parent_option_condition': form.cleaned_data.get('parent_option_condition'),
                        'parent_response_condition': existing_dict,
                        'parent_question_operator': form.cleaned_data.get('parent_question_operator'),
                        'category': form.cleaned_data.get('category'),
                        'enable_task_response': form.cleaned_data.get('enable_task_response'),
                        'entity_type': form.cleaned_data.get('entity_type'),
                        'question_type': form.cleaned_data.get('question_type'),
                        'attributes': form.cleaned_data.get('attributes'),
                        'is_active': form.cleaned_data.get('is_active'),
                        'updated_at': now,
                    }
                )
                updated_siac_ids.add(siac_id)
                if created:
                    obj.created_at = now
                    obj.save()
                    created_configs.append(config_id_str)
                    username = request.user.username if request.user.is_authenticated else 'frontend'
                    mixin.append_liquibase_changeset('insert', obj, username=username, request=request)
                else:
                    changed_fields = []
                    for field in form.changed_data:
                        # Only include fields that are actually in the model and not ignored
                        if hasattr(obj, field):
                            changed_fields.append(field)
                    updated_configs.append(config_id_str)
                    username = request.user.username if request.user.is_authenticated else 'frontend'
                    mixin.append_liquibase_changeset('update', obj, changed_fields, username=username, request=request)
                    # print("Session after changelog append:", request.session.items())
            # Remove configs for SIAC IDs not in the new list
            for old_config in base_configs_qs:
                if old_config.siac_id not in updated_siac_ids:
                    old_config.delete()
            # Show messages
            if created_configs:
                messages.success(request, f"Created configs: {', '.join(created_configs)}")
            if updated_configs:
                messages.success(request, f"Updated configs: {', '.join(updated_configs)}")
            return redirect('config_update', pk=f"{generated_id}-{siac_ids[0]}")
        else:
            messages.error(request, "Form validation failed")
            initial = {}
            if siac_ids:
                initial['siac_id'] = ', '.join(str(x) for x in siac_ids)
            if possible_options_list:
                initial['possible_options'] = ', '.join(possible_options_list)
            form = ConfigMetaForm(request.POST, instance=config, initial=initial)
            parent_response_items = existing_dict
            return render(request, 'createpages/config.html', {
                'form': form,
                'config': config,
                'is_update': True,
                'parent_response_items': parent_response_items,
                'questions': questions,
            })
    else:
        initial = {}
        if isinstance(config.siac_id, list):
            initial['siac_id'] = ', '.join(str(x) for x in config.siac_id)
        elif isinstance(config.siac_id, str):
            initial['siac_id'] = config.siac_id
        else:
            initial['siac_id'] = config.siac_id or ''
        form = ConfigMetaForm(instance=config, initial=initial)
        parent_response_items = config.parent_response_condition or {}
    return render(request, 'createpages/config.html', {
        'form': form,
        'config': config,
        'is_update': True,
        'parent_response_items': parent_response_items,
        'questions': questions,
    })


def finalize_changelog(request):
    filename = request.session.get('changelog_filename')
    epoch = request.session.get('changelog_epoch')
    print("Epoch:", epoch)
    if filename and epoch:
        old_path = os.path.join(CHANGELOG_DIR, filename)
        new_path = os.path.join(CHANGELOG_DIR, f"changelog-{epoch}.sql")
        print("Old path:", old_path)
        if old_path == new_path:
            messages.warning(request, "Changelog is already finalized.")
            return redirect('config_list')
        try:
            shutil.copyfile(old_path, new_path)
            os.remove(old_path)
            messages.success(request, "Changelog file created successfully!")
        except Exception as e:
            messages.error(request, f"Failed to rename changelog file: {e}")
            print("Rename exception:", e)
        for key in ['changelog_filename', 'changelog_epoch', 'changelog_counter']:
            if key in request.session:
                del request.session[key]
    else:
        messages.warning(request, "No changelog file found in session!")
    next_url=request.META.get('HTTP_REFERER')
    return redirect(next_url)


def debug_view(request):
    """Debug view to check database contents"""
    configs = ConfigMetas.objects.all()
    for config in configs:
        siac_id=str(siac_id),
        state_id=state_id,
        question_id=question_id,
        job_id=job_id,
        task_id=task_id,
        id=config_id  # Store the generated config ID
    messages.success(request, 'Configurations created successfully for the given input!')
    return redirect('config_data_view')
    

class QuestionMasterAPI(APIView):
    def get(self, request, pk=None):
        if pk:
            question = get_object_or_404(QuestionMaster, pk=pk)
            serializer = QuestionMasterSerializer(question)
            return Response(serializer.data)
        questions = QuestionMaster.objects.all()
        serializer = QuestionMasterSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QuestionMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        question = get_object_or_404(QuestionMaster, pk=pk)
        serializer = QuestionMasterSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        question = get_object_or_404(QuestionMaster, pk=pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # Create your views here.



class JobMasterAPI(APIView):
    def get(self, request, pk=None):
        if pk:
            job = get_object_or_404(JobMaster, pk=pk)
            serializer = JobMasterSerializer(job)
            return Response(serializer.data)
        jobs = JobMaster.objects.all()
        serializer = JobMasterSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JobMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        job = get_object_or_404(JobMaster, pk=pk)
        serializer = JobMasterSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        job = get_object_or_404(JobMaster, pk=pk)
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class TaskMasterAPI(APIView):
    def get(self,request,pk=None):
        if pk:
            task=get_object_or_404(TaskMaster,pk=pk)
            serializer=TaskMasterSerializer(task)
            return Response(serializer.data)
        tasks=TaskMaster.objects.all()
        serializer=TaskMasterSerializer(tasks,many=True)
        return Response(serializer.data)
    
    def post (self,request):
        serializer=TaskMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,pk):
        job=get_object_or_404(TaskMaster,pk=pk)
        serializer=TaskMasterSerializer(job,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        task=get_object_or_404(TaskMaster,pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
            
class StateMasterAPI(APIView):
    def get(self,request,pk=None):
        if pk:
            state=get_object_or_404(StateMaster,pk=pk)
            serializer=StateMasterSerializer(state)
            return Response(serializer.data)
        states=StateMaster.objects.all()
        serializer=StateMasterSerializer(states,many=True)
        return Response(serializer.data)


    def put(self,request,pk):
        state=get_object_or_404(StateMaster,pk=pk)
        serializer=StateMasterSerializer(state,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    def post(self,request):
        serializer=StateMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        state=get_object_or_404(StateMaster,pk=pk)
        state.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class SiacMasterAPI(APIView):
    def get(self,request,pk=None):
        if pk:
            siac=get_object_or_404(SiacMaster,pk=pk)
            serializer=SiacMasterSerializer(siac)
            return Response(serializer.data)
        siacs=SiacMaster.objects.all()
        serializer=SiacMasterSerializer(siacs,many=True)
        return Response(serializer.data)

    def put(self,request,pk):
        siac=get_object_or_404(SiacMaster,pk=pk)
        serializer=SiacMasterSerializer(siac,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def post(self,request):
        serializer=SiacMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(request.data)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        siac=get_object_or_404(SiacMaster,pk=pk)
        siac.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConfigMetaAPI(APIView):
    def get(self,request,pk=None):
        if pk:
            config=get_object_or_404(ConfigMetas,pk=pk)
            serializer=ConfigMetasSerializer(config)
            return Response(serializer.data)
        configs=ConfigMetas.objects.all()
        serializer=ConfigMetasSerializer(configs,many=True)
        return Response(serializer.data)
    
    def put(self,request,pk):
        config=get_object_or_404(ConfigMetas,pk=pk)
        serializer=ConfigMetasSerializer(config,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        config=get_object_or_404(ConfigMetas,pk=pk)
        config.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self,request):
        serializer=ConfigMetasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



    

from django.core.mail import send_mail
from django.conf import settings

@login_required
def account_info(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        changed = False
        password_changed = False
        # Only allow username change
        if username and username != user.username:
            user.username = username
            changed = True
        # Handle password update with confirmation
        if password or password2:
            if password != password2:
                messages.error(request, "Passwords do not match.")
                return redirect('index')
            if password:
                user.set_password(password)
                password_changed = True
                changed = True
        user.save()
        # Prepare updated info for email
        group_names = ", ".join([g.name for g in user.groups.all()])
        if changed:
            # Send email notification
            send_mail(
                subject="Your Account Info Was Updated",
                message=f"Hello {user.username},\n\nYour account information has been updated.\n\nUsername: {user.username}\nEmail: {user.email}\nUser Groups: {group_names}\n",
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com'),
                recipient_list=[user.email],
                fail_silently=True,
            )
            if password_changed:
                messages.success(request, "Password updated successfully. A confirmation email has been sent.")
            else:
                messages.success(request, "Account info updated! A confirmation email has been sent.")
        else:
            messages.info(request, "No changes made.")
        return redirect('index')
    return redirect('index')



from django.http import HttpResponse
from core.utils.liquibase_changelog import liquibase_changelog

@liquibase_changelog('update')
def test_view(request):
    from core.models import TaskMaster
    obj = TaskMaster.objects.first()
    request.liquibase_instance = obj
    request.liquibase_changed_fields = ['task_name']
    return HttpResponse("Test")
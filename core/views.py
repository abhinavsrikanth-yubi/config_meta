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
            print("Form errors:", form.errors)
    else:
        form = QuestionMasterForm()
    return render(request, 'createpages/question.html', {'form': form})
    if not request.user.groups.filter(name='product').exists():
        return HttpResponseForbidden("You do not have permission to create configs.")

# List view for all jobs
# from django.shortcuts import get_object_or_404

def job_list_view(request):
    jobs = JobMaster.objects.all()
    return render(request, 'viewpages/job_view.html', {'jobs': jobs})

# Read-only detail view

def job_detail_view(request, pk):
    job = get_object_or_404(JobMaster, job_id=pk)
    return render(request, 'detailing/job_detail.html', {'job': job})

# Unified create/update view
@user_passes_test(is_product)
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
            # Check for changes if updating
            if pk:
                has_changed = False
                for field in form.changed_data:
                    # Exclude job_id since it's disabled
                    if field != 'job_id':
                        has_changed = True
                        break
                if not has_changed:
                    messages.info(request, 'No edits made.')
                else:
                    job_obj = form.save()
                    messages.success(request, 'Job Master entry created/updated successfully!')
                form = JobMasterForm(instance=job)
            else:
                job_obj = form.save()
                messages.success(request, 'Job Master entry created/updated successfully!')
                form = JobMasterForm()  # blank form after create
        else:
            print("Form errors:", form.errors)
    else:
        form = JobMasterForm(instance=job)
    return render(request, 'createpages/job.html', {'form': form, 'job': job, 'is_update': is_update})
    if not request.user.groups.filter(name='product').exists():
        return HttpResponseForbidden("You do not have permission to create configs.")


from django.shortcuts import get_object_or_404

# --- Task Master ---
def task_list_view(request):
    tasks = TaskMaster.objects.all()
    return render(request, 'viewpages/task_view.html', {'tasks': tasks})

def task_detail_view(request, pk):
    task = get_object_or_404(TaskMaster, task_id=pk)
    return render(request, 'detailing/task_detail.html', {'task': task})

@user_passes_test(is_product)
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
            if pk:
                has_changed = False
                for field in form.changed_data:
                    if field != 'task_id':
                        has_changed = True
                        break
                if not has_changed:
                    messages.info(request, 'No edits made.')
                else:
                    task_obj = form.save()
                    messages.success(request, 'Task Master entry created/updated successfully!')
                form = TaskMasterForm(instance=task)
            else:
                task_obj = form.save()
                messages.success(request, 'Task Master entry created/updated successfully!')
                form = TaskMasterForm()  # blank form after create
        else:
            print("Form errors:", form.errors)
    else:
        form = TaskMasterForm(instance=task)
    return render(request, 'createpages/task.html', {'form': form, 'task': task, 'is_update': is_update})
    if not request.user.groups.filter(name='product').exists():
        return HttpResponseForbidden("You do not have permission to create configs.")

    
# --- State Master ---
def state_list_view(request):
    states = StateMaster.objects.all()
    return render(request, 'viewpages/state_view.html', {'states': states})

def state_detail_view(request, pk):
    state = get_object_or_404(StateMaster, state_id=pk)
    return render(request, 'detailing/state_detail.html', {'state': state})

@user_passes_test(is_product)
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
            if pk:
                has_changed = False
                for field in form.changed_data:
                    if field != 'state_id':
                        has_changed = True
                        break
                if not has_changed:
                    messages.info(request, 'No edits made.')
                else:
                    state_obj = form.save()
                    messages.success(request, 'State Master entry created/updated successfully!')
                form = StateMasterForm(instance=state)
            else:
                state_obj = form.save()
                messages.success(request, 'State Master entry created/updated successfully!')
                form = StateMasterForm()  # blank form after create
        else:
            print("Form errors:", form.errors)
    else:
        form = StateMasterForm(instance=state)
    return render(request, 'createpages/state.html', {'form': form, 'state': state, 'is_update': is_update})
    if not request.user.groups.filter(name='product').exists():
        return HttpResponseForbidden("You do not have permission to create configs.")

# --- SIAC Master ---
def siac_list_view(request):
    siacs = SiacMaster.objects.all()
    return render(request, 'viewpages/siac_view.html', {'siacs': siacs})

def siac_detail_view(request, pk):
    siac = get_object_or_404(SiacMaster, siac_id=pk)
    return render(request, 'detailing/siac_detail.html', {'siac': siac})

@user_passes_test(is_product)
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
            if pk:
                has_changed = False
                for field in form.changed_data:
                    if field != 'siac_id':
                        has_changed = True
                        break
                if not has_changed:
                    messages.info(request, 'No edits made.')
                else:
                    siac_obj = form.save()
                    messages.success(request, 'SIAC Master entry created/updated successfully!')
                form = SiacMasterForm(instance=siac)
            else:
                siac_obj = form.save()
                messages.success(request, 'SIAC Master entry created/updated successfully!')
                form = SiacMasterForm()  # blank form after create
        else:
            print("Form errors:", form.errors)
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
            if pk:
                has_changed = False
                for field in form.changed_data:
                    if field != 'question_id':
                        has_changed = True
                        break
                if not has_changed:
                    messages.info(request, 'No edits made.')
                else:
                    question_obj = form.save()
                    messages.success(request, 'Question Master entry created/updated successfully!')
                form = QuestionMasterForm(instance=question)
            else:
                question_obj = form.save()
                messages.success(request, 'Question Master entry created/updated successfully!')
                form = QuestionMasterForm()  # blank form after create
        else:
            print("Form errors:", form.errors)
    else:
        form = QuestionMasterForm(instance=question)
    return render(request, 'createpages/question.html', {'form': form, 'question': question, 'is_update': is_update})
    if not request.user.groups.filter(name='product').exists():
        return HttpResponseForbidden("You do not have permission to create configs.")


# --- Config Master ---

def config_redirect_view(request):
    return redirect('config_list')

def config_list_view(request):
    # (Unchanged main view for initial load)
    siac = request.GET.get('siac', '').strip()
    state = request.GET.get('state', '').strip()
    config_id = request.GET.get('config_id', '').strip()
    question_id = request.GET.get('question_id', '').strip()
    task_id = request.GET.get('task_id', '').strip()
    job_id = request.GET.get('job_id', '').strip()

    configs = ConfigMetas.objects.all()
    if siac:
        configs = configs.filter(siac_id__icontains=siac)
    if state:
        configs = configs.filter(state_id__icontains=state)
    if config_id:
        configs = configs.filter(config_id__icontains=config_id)
    if question_id:
        configs = configs.filter(question_id__icontains=question_id)
    if task_id:
        configs = configs.filter(task_id__icontains=task_id)
    if job_id:
        configs = configs.filter(job_id__icontains=job_id)

    configs = configs.exclude(config_id__contains='None').exclude(config_id__isnull=True).exclude(config_id='')
    configs = configs.order_by('config_id')
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
            'config_id': config_id,
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
    config_id = request.GET.get('config_id', '').strip()
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
    if config_id:
        configs = configs.filter(config_id=config_id)
    configs = configs.exclude(config_id__contains='None').exclude(config_id__isnull=True).exclude(config_id='')
    configs = configs.order_by('config_id')
    paginator = Paginator(configs, 10)
    page_obj = paginator.get_page(page)

    results = []
    for config in page_obj:
        print('DEBUG config object:', config.__dict__)
        siac_val = config.siac_id
        if isinstance(siac_val, list):
            siac_val = ", ".join(map(str, siac_val))
        config_id_val = getattr(config, 'config_id', None)
        if config_id_val and isinstance(config_id_val, str) and config_id_val.strip():
            results.append({
                "config_id": config_id_val,
                "state_id": config.state_id,
                "siac_id": siac_val,
                "question_id": config.question_id,
                "task_id": config.task_id,
                "job_id": config.job_id,
            })
    print(f"DEBUG: Final results list = {results}")
    return JsonResponse({
        "results": results,
        "current_page": page_obj.number,
        "num_pages": paginator.num_pages,
    })
    if not request.user.groups.filter(name='product').exists():
        return HttpResponseForbidden("You do not have permission to create configs.")

def config_detail_view(request, pk):
    config = get_object_or_404(ConfigMetas, config_id=pk)
    return render(request, 'detailing/config_detail.html', {'config': config})

@user_passes_test(is_product)
def config_create_view(request):
    print("CREATE VIEW CALLED", request.method)
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
        siac_id_raw = request.POST.get('siac_id', '')
        siac_ids = [s.strip() for s in siac_id_raw.split(',') if s.strip()]
        if form.is_valid():
            created_configs = []
            duplicate_configs = []
            for siac_id in siac_ids:
                siac_id_str = str(int(siac_id))
                siac_id_list = [int(siac_id)]
                question_id = form.cleaned_data.get('question_id')
                state_id = form.cleaned_data.get('state_id')
                task_id = form.cleaned_data.get('task_id')
                job_id = form.cleaned_data.get('job_id')
                generated_id = f"{question_id}#{state_id}#{task_id}#{job_id}"
                config_id_str = f"{generated_id}-{siac_id_str}"
                now = timezone.now()
                # Check duplicate
                if ConfigMetas.objects.filter(config_id=config_id_str).exists():
                    duplicate_configs.append(config_id_str)
                    continue
                ConfigMetas.objects.create(
                    config_id=config_id_str,
                    id=generated_id,
                    siac_id=siac_id_list,
                    state_id=state_id,
                    question_id=question_id,
                    job_id=job_id,
                    task_id=task_id,
                    possible_options=possible_options_list,
                    parent_option_condition=form.cleaned_data.get('parent_option_condition'),
                    parent_response_condition=parent_response_dict,
                    parent_question_operator=form.cleaned_data.get('parent_question_operator'),
                    category=form.cleaned_data.get('category'),
                    enable_task_response=form.cleaned_data.get('enable_task_response'),
                    entity_type=form.cleaned_data.get('entity_type'),
                    question_type=form.cleaned_data.get('question_type'),
                    attributes=form.cleaned_data.get('attributes'),
                    is_active=form.cleaned_data.get('is_active'),
                    skip_trigger=form.cleaned_data.get('skip_trigger'),
                    created_at=now,
                    updated_at=now,
                )
                created_configs.append(config_id_str)
                print(created_configs)
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
        # siac_ids: convert to CSV string for display
        if siac_ids:
            initial['siac_id'] = ', '.join(str(x) for x in siac_ids)
        # possible_options: convert to CSV string for display
        if possible_options_list:
            initial['possible_options'] = ', '.join(possible_options_list)
        # Use the initial dict for the form
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
def config_update_view(request, pk):
    from .models import QuestionMaster
    questions = QuestionMaster.objects.all()
    config = get_object_or_404(ConfigMetas, config_id=pk)

    if request.method == 'POST':
        form = ConfigMetaForm(request.POST, instance=config)
        # Load existing parent_response_condition dict
        existing_dict = config.parent_response_condition.copy() if config.parent_response_condition else {}
        parent_questions = request.POST.getlist('parent_question')
        parent_responses = request.POST.getlist('parent_response')
        # Build new responses from POST
        parent_response_dict = {}
        for q, r in zip(parent_questions, parent_responses):
            if q and r:
                parent_response_dict.setdefault(q, []).append(r)
        # Merge: extend or add
        for q, responses in parent_response_dict.items():
            if q in existing_dict:
                existing_dict[q].extend(responses)
            else:
                existing_dict[q] = responses
        possible_options_raw = request.POST.get('possible_options', '')
        possible_options_list = [opt.strip() for opt in possible_options_raw.split(',') if opt.strip()]
        if form.is_valid():
            config_obj = form.save(commit=False)
            config_obj.parent_response_condition = existing_dict
            config_obj.possible_options = possible_options_list
            config_obj.updated_at = timezone.now()
            config_obj.save()
            messages.success(request, f"Config {config_obj.config_id} updated successfully.")
            return redirect('config_update', pk=config_obj.config_id)
        else:
            messages.error(request, "Form validation failed")
        parent_response_items = existing_dict
        # else:
        # # GET: prepare initial data for form
        #     initial = {}
        if isinstance(config.siac_id, list):
            # Handles both ['4'] and [4]
            initial['siac_id'] = ', '.join(str(x) for x in config.siac_id)
        elif isinstance(config.siac_id, str):
            # Try to parse string list
            import ast
            try:
                parsed = ast.literal_eval(config.siac_id)
                if isinstance(parsed, list):
                    initial['siac_id'] = ', '.join(str(x) for x in parsed)
                else:
                    initial['siac_id'] = config.siac_id
            except Exception:
                initial['siac_id'] = config.siac_id
        else:
            initial['siac_id'] = config.siac_id or ''
        form = ConfigMetaForm(instance=config, initial=initial)
        parent_response_items = config.parent_response_condition or {}
        parent_response_items = parent_response_dict
    else:
        initial = {}
        if isinstance(config.siac_id, list):
            # Handles both ['4'] and [4]
            initial['siac_id'] = ', '.join(str(x) for x in config.siac_id)
        elif isinstance(config.siac_id, str):
            # Try to parse string list
            import ast
            try:
                parsed = ast.literal_eval(config.siac_id)
                if isinstance(parsed, list):
                    initial['siac_id'] = ', '.join(str(x) for x in parsed)
                else:
                    initial['siac_id'] = config.siac_id
            except Exception:
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

    # Fetch config if updating, else None
    config = get_object_or_404(ConfigMetas, config_id=pk) if pk else None
    is_update = bool(pk)

    # For GET requests: render the form with instance data
    if request.method == 'GET':
        # Prepare initial data for possible_options and siac_id as CSV
        initial = {}
        if config:
            # possible_options: stored as list or string, show as CSV
            if isinstance(config.possible_options, list):
                initial['possible_options'] = ', '.join(config.possible_options)
            elif isinstance(config.possible_options, str):
                initial['possible_options'] = config.possible_options
            # siac_id: always show as CSV string
            siac_val = config.siac_id
            if isinstance(siac_val, list):
                initial['siac_id'] = ', '.join(str(x) for x in siac_val)
            elif isinstance(siac_val, str):
                # Try to parse a string that looks like a list
                if siac_val.startswith('[') and siac_val.endswith(']'):
                    try:
                        import ast
                        parsed = ast.literal_eval(siac_val)
                        if isinstance(parsed, list):
                            initial['siac_id'] = ', '.join(str(x) for x in parsed)
                        else:
                            initial['siac_id'] = siac_val
                    except Exception:
                        initial['siac_id'] = siac_val
                else:
                    initial['siac_id'] = siac_val
            else:
                initial['siac_id'] = ''
            # Parent response: parse dict for rendering
            parent_response_items = config.parent_response_condition or {}
        else:
            parent_response_items = {}
        from .models import QuestionMaster
        # questions = QuestionMaster.objects.all()
        form = ConfigMetaForm(instance=config, initial=initial)
        return render(request, 'createpages/config.html', {
            'form': form,
            'config': config,
            'is_update': is_update,
            'parent_response_items': parent_response_items,
            'questions': QuestionMaster.objects.all(),
            # 'questions': questions,
        })

    # For POST/PUT: process form submission
    if request.method in ['POST', 'PUT']:
        form = ConfigMetaForm(request.POST, instance=config)
        # Parse parent_response_condition from hidden JSON field
        parent_response_json = request.POST.get('parent_response_condition_json', '{}')
        try:
            parent_response_dict = json.loads(parent_response_json)
        except Exception:
            parent_response_dict = {}

        # Clean possible_options to python list
        possible_options_raw = request.POST.get('possible_options', '')
        possible_options_list = [opt.strip() for opt in possible_options_raw.split(',') if opt.strip()]

        # Clean siac_id to python list of strings
        siac_id_raw = request.POST.get('siac_id', '')
        siac_ids = [s.strip() for s in siac_id_raw.split(',') if s.strip()]


        if form.is_valid():
            created_configs = []
            updated_configs = []

            for siac_id in siac_ids:
                # Build config_id for each SIAC
                siac_id_str = str(int(siac_id))
                siac_id_list=[int(siac_id)]
                question_id = form.cleaned_data.get('question_id')
                state_id = form.cleaned_data.get('state_id')
                task_id = form.cleaned_data.get('task_id')
                job_id = form.cleaned_data.get('job_id')
                new_config_id = f"{question_id}#{state_id}#{task_id}#{job_id}-{siac_id_str}"

                # Use update_or_create to avoid duplicate key errors

                # Generate id and config_id in the view
                generated_id = f"{question_id}#{state_id}#{task_id}#{job_id}"
                config_id_str = f"{generated_id}-{siac_id_str}"
                now = timezone.now()
                obj, created = ConfigMetas.objects.update_or_create(
                    config_id=config_id_str,
                    defaults={
                        'id': generated_id,
                        'siac_id': siac_id_list,
                        'state_id': state_id,
                        'question_id': question_id,
                        'job_id': job_id,
                        'task_id': task_id,
                        'possible_options': possible_options_list,
                        'parent_option_condition': form.cleaned_data.get('parent_option_condition'),
                        'parent_response_condition': parent_response_dict,
                        'parent_question_operator': form.cleaned_data.get('parent_question_operator'),
                        'category': form.cleaned_data.get('category'),
                        'enable_task_response': form.cleaned_data.get('enable_task_response'),
                        'entity_type': form.cleaned_data.get('entity_type'),
                        'question_type': form.cleaned_data.get('question_type'),
                        'attributes': form.cleaned_data.get('attributes'),
                        'is_active': form.cleaned_data.get('is_active'),
                        'skip_trigger': form.cleaned_data.get('skip_trigger'),
                        'id': form.cleaned_data.get('id'),
                        # 'updated_at': now,
                        # 'created_at': now if created else obj.created_at,
                    }
                )
                if created:
                    obj.created_at = now
                    obj.save()
                    created_configs.append(new_config_id)
                else:
                    updated_configs.append(new_config_id)

            # Show messages
            if created_configs:
                messages.success(request, f"Created configs: {', '.join(created_configs)}")
            if updated_configs:
                messages.success(request, f"Updated configs: {', '.join(updated_configs)}")

            # Redirect to update page for the first config
            if created_configs:
                return redirect('config_update', pk=created_configs[0])
            elif updated_configs:
                return redirect('config_update', pk=updated_configs[0])
            else:
                messages.error(request, "No configs created or updated")
                return render(request, 'createpages/config.html', {
                    'form': form,
                    'config': config,
                    'is_update': is_update,
                    'parent_response_items': parent_response_dict,
                })
        else:
            messages.error(request, "Form validation failed")
            # For re-rendering after error, show parent_response_items as entered
            parent_response_items = parent_response_dict

        from .models import QuestionMaster
        questions = QuestionMaster.objects.all()
        if not form.has_changed():
            messages.info(request, "No changes made.")
        return render(request, 'createpages/config.html', {
            'form': form,
            'config': config,
            'is_update': is_update,
            'parent_response_items': parent_response_items,
            'questions': questions,
        })
def debug_view(request):
    """Debug view to check database contents"""
    configs = ConfigMetas.objects.all()
    print("\nDatabase contents:")
    for config in configs:
        print(f"\nConfig ID: {config.id}")
        print(f"SIAC ID: {config.siac_id}")
        print(f"Question ID: {config.question_id}")
        print(f"State ID: {config.state_id}")
        print(f"Job ID: {config.job_id}")
        siac_id=str(siac_id),
        state_id=state_id,
        question_id=question_id,
        job_id=job_id,
        task_id=task_id,
        config_id=config_id  # Store the generated config ID
    messages.success(request, 'Configurations created successfully for the given input!')
    return redirect('config_data_view')
    # else:
    #     print("Form errors:", form.errors)
        # else:
            # form = ConfigMetaForm()
    
    # return render(request, 'config.html', {'form': form})


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

    
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import QuestionMaster, JobMaster, StateMaster, TaskMaster, SiacMaster,ConfigMetas
from django.core.paginator import Paginator

def question_search(request):
    q = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    questions = QuestionMaster.objects.all().order_by('question_id')
    if q:
        questions = questions.filter(
            Q(question_id__icontains=q) | Q(question_name__icontains=q)
        )
    paginator = Paginator(questions, 10)  # 10 per page
    page_obj = paginator.get_page(page)
    results = [
        {
            'id': question.question_id,
            'label': f'{question.question_id} - {question.question_name}',
            'question_name': question.question_name,
        }
        for question in page_obj
    ]
    return JsonResponse({
        'results': results,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
    })

def question_detail(request, pk):
    question = get_object_or_404(QuestionMaster, question_id=pk)
    return render(request, 'detailing/question_detail.html', {'question': question})

def question_view(request):
    questions = QuestionMaster.objects.all().order_by('question_id')
    return render(request, 'viewpages/question_view.html', {'questions': questions})



def job_search(request):
    q = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    jobs = JobMaster.objects.all().order_by('job_id')
    if q:
        jobs = jobs.filter(
            Q(job_id__icontains=q) | Q(job_name__icontains=q)
        )
    paginator = Paginator(jobs, 10)  # 10 per page
    page_obj = paginator.get_page(page)
    results = [
        {
            'id': job.job_id,
            'label': f'{job.job_id} - {job.job_name}',
            'job_name': job.job_name,
        }
        for job in page_obj
    ]
    return JsonResponse({
        'results': results,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
    })


def job_detail(request, pk):
    job = get_object_or_404(JobMaster, job_id=pk)
    return render(request, 'detailing/job_detail.html', {'job': job})

def job_view(request):
    jobs = JobMaster.objects.all().order_by('job_id')
    paginator = Paginator(jobs, 10)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'viewpages/job_view.html', {'jobs': jobs})

def state_search(request):
    q = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    states = StateMaster.objects.all().order_by('state_id')
    if q:
        states = states.filter(
            Q(state_id__icontains=q) | Q(state_name__icontains=q)
        )
    paginator = Paginator(states, 10)  # 10 per page
    page_obj = paginator.get_page(page)
    results = [
        {
            'id': state.state_id,
            'label': f'{state.state_id} - {state.state_name}',
            'state_name': state.state_name,
        }
        for state in page_obj
    ]
    return JsonResponse({
        'results': results,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
    })

def state_detail(request, pk):
    state = get_object_or_404(StateMaster, state_id=pk)
    return render(request, 'detailing/state_detail.html', {'state': state})

def state_view(request):
    states = StateMaster.objects.all().order_by('state_id')
    return render(request, 'viewpages/state_view.html', {'states': states})

def task_search(request):
    q = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    tasks = TaskMaster.objects.all().order_by('task_id')
    if q:
        tasks = tasks.filter(
            Q(task_id__icontains=q) | Q(task_name__icontains=q)
        )
    paginator = Paginator(tasks, 10)
    page_obj = paginator.get_page(page)
    results = [
        {
            'id': t.task_id,
            'label': f'{t.task_id} - {t.task_name}',
            'task_name': t.task_name,
        }
        for t in page_obj
    ]
    return JsonResponse({
        'results': results,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
    })

def task_detail(request, pk):
    task = get_object_or_404(TaskMaster, task_id=pk)
    return render(request, 'detailing/task_detail.html', {'task': task})

def task_view(request):
    tasks = TaskMaster.objects.all().order_by('task_id')
    return render(request, 'viewpages/task_view.html', {'tasks': tasks})

def siac_search(request):
    q = request.GET.get('q', '')
    results = []
    if q:
        qs = SiacMaster.objects.filter(
            Q(siac_id__icontains=q) | Q(scheme__icontains=q) | Q(sector__icontains=q)
        )
    else:
        qs=SiacMaster.objects.all().order_by('siac_id')
    page = int(request.GET.get('page', 1))
    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(page)
    results = [
        {
            'id': obj.siac_id,
            'scheme': obj.scheme,
            'sector': obj.sector,
            'label': f'{obj.siac_id} '
        }
        for obj in page_obj
    ]
    return JsonResponse({'results': results})

def siac_detail(request,pk):
    siac = get_object_or_404(SiacMaster, siac_id=pk)
    return render(request, 'detailing/siac_detail.html', {'siac': siac})
    
def siac_view(request):
    siacs = SiacMaster.objects.all().order_by('siac_id')
    return render(request, 'viewpages/siac_view.html', {'siacs': siacs})

def config_search(request):
    page = int(request.GET.get('page', 1))
    configs = ConfigMetas.objects.all().order_by('id')

    id = request.GET.get('id', '')
    state = request.GET.get('state', '')
    question = request.GET.get('question', '')
    siac = request.GET.get('siac', '')
    task = request.GET.get('task', '')
    job = request.GET.get('job', '')

    # Only search by IDs (not names)
    if id:
        configs = configs.filter(id__icontains=id)
    if state:
        state_ids = list(StateMaster.objects.filter(state_name__icontains=state).values_list('state_id', flat=True))
        configs = configs.filter(Q(state_id__icontains=state) | Q(state_id__in=state_ids))
    if question:
        configs = configs.filter(question_id=int(question))
    if siac:
        configs = configs.filter(siac_id__icontains=siac)
    if task:
        configs = configs.filter(task_id=int(task))
    if job:
        configs = configs.filter(job_id=int(job))

    paginator = Paginator(configs, 10)
    page_obj = paginator.get_page(page)
    results = []
    for config in page_obj:
        # Optionally fetch related names for display (not for searching)
        question = QuestionMaster.objects.filter(question_id=config.question_id).first()
        state = StateMaster.objects.filter(state_id=config.state_id).first()
        task = TaskMaster.objects.filter(task_id=config.task_id).first()
        job = JobMaster.objects.filter(job_id=config.job_id).first()
        siac = SiacMaster.objects.filter(siac_id=config.siac_id).first()

        results.append({
            'id': config.id,
            'question_id': config.question_id,
            'state_id': config.state_id,
            'task_id': config.task_id,
            'job_id': config.job_id,
            'siac_id': config.siac_id,
            # # Display names for UI (optional)
            # 'question_name': question.question_name if question else '',
            # 'state_name': state.state_name if state else '',
            # 'task_name': task.task_name if task else '',
            # 'job_name': job.job_name if job else '',
            # 'siac_description': siac.siac_description if siac else '',
        })

    return JsonResponse({
        "results": results,
        "current_page": page_obj.number,
        "num_pages": paginator.num_pages,
    })


def config_detail(request,pk):
    config = get_object_or_404(ConfigMetas, id=pk)
    return render(request, 'detailing/config_detail.html', {'config': config})

def config_view(request):
    configs = ConfigMetas.objects.all().order_by('id')
    return render(request, 'viewpages/config_view.html', {'configs': configs})
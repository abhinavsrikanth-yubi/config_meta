from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import JobMaster, QuestionMaster, TaskMaster, StateMaster, SiacMaster, ConfigMetas
from django.urls import reverse
import json

# Job update (unchanged)
def job_update(request, pk):
    job = get_object_or_404(JobMaster, job_id=pk)
    updated=False
    message=None
    if request.method in ['POST', 'PUT']:
        old_values={
            'job_name': job.job_name,
            'conditions': job.conditions,
            'order_id': job.order_id,
            'source_category': job.source_category,
            'job_type': job.job_type,

        }
        new_values={
            'job_name': request.POST.get('job_name', job.job_name),
            'conditions': request.POST.get('conditions', job.conditions),
            'order_id': request.POST.get('order_id', job.order_id),
            'source_category': request.POST.get('source_category', job.source_category),
            'job_type': request.POST.get('job_type', job.job_type),
        }
        for field, new_val in new_values.items():
            if str(getattr(job, field)) != str(new_val):
                setattr(job, field, new_val)
                updated = True
        if updated:
            job.save()
            messages.success(request, 'Values updated successfully.')
        else:
            messages.info(request, 'No edits made.')
        return redirect(f'/job/update/{pk}/')
    return render(request, 'updatepages/job_update.html', {'job': job})

# Question update with change detection and messages
def question_update(request, pk):
    question = get_object_or_404(QuestionMaster, question_id=pk)
    updated = False
    message = None
    if request.method in ['POST', 'PUT']:
        # Store old values for comparison
        old_values = {
            'question_name': question.question_name,
            'attributes': question.attributes,
            'default_option': question.default_option,
            'is_active': question.is_active,
            'is_multi_select': question.is_multi_select,
            'is_master': question.is_master,
            'source_category': question.source_category,
            'ui_element_type': question.ui_element_type,
        }
        # Get new values from request
        new_values = {
            'question_name': request.POST.get('question_name', question.question_name),
            'attributes': request.POST.get('attributes', question.attributes),
            'default_option': request.POST.get('default_option', question.default_option),
            'is_active': request.POST.get('is_active', question.is_active),
            'is_multi_select': request.POST.get('is_multi_select', question.is_multi_select),
            'is_master': request.POST.get('is_master', question.is_master),
            'source_category': request.POST.get('source_category', question.source_category),
            'ui_element_type': request.POST.get('ui_element_type', question.ui_element_type),
        }
        # Compare and update if changed
        for field, new_val in new_values.items():
            if str(getattr(question, field)) != str(new_val):
                setattr(question, field, new_val)
                updated = True
        if updated:
            question.save()
            messages.success(request, 'Values updated successfully.')
        else:
            messages.info(request, 'No edits made.')
        return redirect(f'/question/update/{pk}/')
    return render(request, 'updatepages/question_update.html', {'question': question})


# Task update
def task_update(request, pk):
    task = get_object_or_404(TaskMaster, task_id=pk)
    updated=False
    message=None
    if request.method in ['POST', 'PUT']:
        old_values={
            'task_name': task.task_name,
            'conditions': task.conditions,
            'order_id': task.order_id,
            'task_type': task.task_type,
            'mandatory': task.mandatory,
        }
        new_values={
            'task_name': request.POST.get('task_name', task.task_name),
            'conditions': request.POST.get('conditions', task.conditions),
            'order_id': request.POST.get('order_id', task.order_id),
            'task_type': request.POST.get('task_type', task.task_type),
            'mandatory': request.POST.get('mandatory', task.mandatory),
        }
        for field, new_val in new_values.items():
            if str(getattr(task, field)) != str(new_val):
                setattr(task, field, new_val)
                updated = True
        if updated:
            task.save()
            messages.success(request, 'Values updated successfully.')
        else:
            messages.info(request, 'No edits made.')
        return redirect(f'/task/update/{pk}/')
    return render(request, 'updatepages/task_update.html', {'task': task})

# State update
def state_update(request, pk):
    state = get_object_or_404(StateMaster, state_id=pk)
    updated=False
    message=None
    if request.method in ['POST', 'PUT']:
        old_values={
            'state_name': state.state_name,
            'condition': state.condition,
            'description': state.description,
        }
        new_values={
            'state_name': request.POST.get('state_name', state.state_name),
            'condition': request.POST.get('condition', state.condition),
            'description': request.POST.get('description', state.description),
        }
        for field, new_val in new_values.items():
            if str(getattr(state, field)) != str(new_val):
                setattr(state, field, new_val)
                updated = True
        if updated:
            state.save()
            messages.success(request, 'Values updated successfully.')
        else:
            messages.info(request, 'No edits made.')
        return redirect(f'/state/update/{pk}/')
    return render(request, 'updatepages/state_update.html', {'state': state})

# SIAC update
def siac_update(request, pk):
    siac = get_object_or_404(SiacMaster, siac_id=pk)
    updated=False
    message=None
    if request.method in ['POST', 'PUT']:
        old_values={
            'description': siac.description,
            'scheme': siac.scheme,
            'sector': siac.sector,
            'conditions': siac.conditions,
        }
        new_values={
            'description': request.POST.get('description', siac.description),
            'scheme': request.POST.get('scheme', siac.scheme),
            'sector': request.POST.get('sector', siac.sector),
            'conditions': request.POST.get('conditions', siac.conditions),
        }
        for field, new_val in new_values.items():
            if str(getattr(siac, field)) != str(new_val):
                setattr(siac, field, new_val)
                updated = True
        if updated:
            siac.save()
            messages.success(request, 'Values updated successfully.')
        else:
            messages.info(request, 'No edits made.')
        return redirect(f'/siac/update/{pk}/')
    return render(request, 'updatepages/siac_update.html', {'siac': siac})


def config_update(request, pk):
    config = get_object_or_404(ConfigMetas, config_id=pk)
    questions = QuestionMaster.objects.all()
    questions_json = json.dumps([{'id': q.question_id, 'label': q.question_name} for q in questions])
    updated = False
    message = None
    if request.method in ['POST', 'PUT']:
        new_config_id = request.POST.get('config_id')
        # If new config_id exists, update that record
        try:
            config_instance = ConfigMetas.objects.get(config_id=new_config_id)
            existed = True
        except ConfigMetas.DoesNotExist:
            config_instance = None
            existed = False
        form = ConfigMetaForm(request.POST, instance=config_instance)
        formset = ParentResponseFormSet(request.POST, prefix='parent_response')
        parent_response_dict = {}
        if form.is_valid() and formset.is_valid():
            config_obj = form.save(commit=False)
            config_obj.parent_response_condition = parent_response_dict
            config_obj.save()
            for f in formset:
                if f.cleaned_data and not f.cleaned_data.get('DELETE', False):
                    q = f.cleaned_data.get('question')
                    a = f.cleaned_data.get('answer')
                    if q and a:
                        parent_response_dict[str(q.question_id)] = [a.strip()]
            if existed:
                messages.success(request, f"Existing config_id: {config_obj.config_id} is updated")
            else:
                messages.success(request, f"Config ID: {config_obj.config_id} created successfully")
            return redirect('config_update', pk=config_obj.config_id)
            old_values={
            'config_id': config.config_id,
            'question_id': config.question_id,
            'task_id': config.task_id,
            'job_id': config.job_id,
            'state_id': config.state_id,
            'siac_id': config.siac_id,
            'possible_options': config.possible_options,
            'enable_task_response': config.enable_task_response,
            'entity_type': config.entity_type,
            'question_type': config.question_type,
            'attributes': config.attributes,
            'parent_option_condition': config.parent_option_condition,
            'parent_question_operator': config.parent_question_operator,
            'category': config.category,
            'is_active': config.is_active,}
            # 'skip_trigger': config.skip_trigger,
        
        # --- Process parent_response_condition ---
        prc_raw = request.POST.get('parent_response_condition', '[]')
        try:
            if prc_raw == '[]':
                prc_dict = config.parent_response_condition or {}
            else:
                prc_list = json.loads(prc_raw)
                prc_dict = config.parent_response_condition or {}
                if isinstance(prc_list, list):
                    for item in prc_list:
                        qid = str(item.get("question", "")).strip()
                        v = item.get("value", "").strip()
                        if qid and v:
                            if qid in prc_dict:
                                prc_dict[qid].append(v)
                            else:
                                prc_dict[qid] = [v]
            config.parent_response_condition = prc_dict
        except Exception as e:
            print(f"Error processing parent_response_condition: {e}")
            config.parent_response_condition = config.parent_response_condition or {}
        # Deep compare using json.dumps
        if json.dumps(old_values.get('parent_response_condition', {}), sort_keys=True) != json.dumps(config.parent_response_condition, sort_keys=True):
            updated = True
        # --- Update other fields ---
        fields_to_check = [
            'siac_id', 'default_option', 'state_id', 'question_id', 'job_id', 'task_id', 'config_id',
            # 'possible_options',
            'enable_task_response', 'entity_type', 'question_type', 'attributes',
            'parent_option_condition', 'parent_question_operator', 'category',
        ]
        for field in fields_to_check:
            new_val = request.POST.get(field, getattr(config, field))
            if str(getattr(config, field)) != str(new_val):
                setattr(config, field, new_val)
                updated = True
        # Save and redirect
        if updated:
            config.save()
            messages.success(request, 'Values updated successfully.')
        else:
            messages.info(request, 'No edits made.')
        # Use pk for redirect to avoid NoReverseMatch if config_id changes
        return redirect(reverse('config_update', args=[pk]))
    return render(request, 'updatepages/config_update.html', {'config': config, 'questions_json': questions_json})
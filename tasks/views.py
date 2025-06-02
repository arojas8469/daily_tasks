from django.shortcuts import render, redirect
from .models import Task
from django.contrib.auth.decorators import login_required 
from django.shortcuts import get_object_or_404
from django.contrib import messages


@login_required
def task_list(request):
    status_filter = request.GET.get('status')  
    tasks = Task.objects.filter(user=request.user)

    if status_filter:
        tasks = tasks.filter(status=status_filter)

    tasks = tasks.order_by('-created_at')  

    return render(request, 'tasks/tasks.html', {'tasks': tasks})


@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        status = request.POST.get('status', 'todo')  # 👈 Added this line

        if title:
            Task.objects.create(
                title=title,
                description=description,
                status=status,  # 👈 Save status
                user=request.user
            )
            messages.success(request, "Task added successfully!")
            return redirect('task_list')
        else:
            return render(request, 'tasks/add_task.html', {'error': 'Title is required'})
    
    return render(request, 'tasks/add_task.html')

@login_required
def task_list(request):
    status_filter = request.GET.get('status')  
    tasks = Task.objects.filter(user=request.user)

    if status_filter:
        tasks = tasks.filter(status=status_filter)

    tasks = tasks.order_by('-created_at')  

    total_tasks = tasks.count()
    done_tasks = tasks.filter(status='Done').count()
    completion_percentage = int((done_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    return render(request, 'tasks/tasks.html', {
        'tasks': tasks,
        'completion_percentage': completion_percentage,
        'done_tasks': done_tasks,
        'total_tasks': total_tasks
    })


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('task_list')

@login_required
def update_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['todo', 'in_progress', 'Done']:
            task.status = status
            task.save()
    return redirect('task_list')


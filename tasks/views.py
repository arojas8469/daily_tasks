from django.shortcuts import render, redirect
from .models import Task
from django.contrib.auth.decorators import login_required 
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Case, When, Value, IntegerField
from django.core.mail import send_mail
from .forms import ContactForm
from django.conf import settings 


def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    priority = request.GET.get('priority')
    if priority:
        tasks = tasks.filter(priority=priority)

    tasks = tasks.order_by(
        Case(
            When(priority='High', then=Value(1)),
            When(priority='Medium', then=Value(2)),
            When(priority='Low', then=Value(3)),
            output_field=IntegerField()
        )
    )

    return render(request, 'tasks/tasks.html', {'tasks': tasks})



@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        status = request.POST.get('status', 'todo')  # 👈 Added this line
        priority = request.POST.get('priority')

        if title:
            Task.objects.create(
                title=title,
                description=description,
                status=status, 
                priority=priority,
                user=request.user
            )
            messages.success(request, "Task added successfully!")
            return redirect('task_list')
        else:
            return render(request, 'tasks/add_task.html', {'error': 'Title is required'})
    
    return render(request, 'tasks/add_task.html')

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


def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        priority = request.POST.get("priority", "").strip()

        if not title:
            return render(request, "tasks/edit_task.html", {
                "task": task,
                "error": "Title is required."
            })
        if not priority:
            return render(request, "tasks/edit_task.html", {
                "task": task,
                "error": "Priority is required."
            })

        task.title = title
        task.description = description
        task.priority = priority

        task.save()

        return redirect("task_list")

    return render(request, "tasks/edit_task.html", {"task": task})


@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

def contact(request):
    return render(request, 'tasks/contact.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            send_mail(
                subject=f"Message from {name}",
                message=message,
                from_email=email,
                recipient_list=['anthony.rojas099@gmail.com'],
                fail_silently=False
            )
            messages.success(request, "Message sent successfully!")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'tasks/contact.html', {'form': form})

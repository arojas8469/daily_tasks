from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Case, When, Value, IntegerField
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from calendar import Calendar
from datetime import date
from calendar import monthcalendar
from calendar import month_name
from datetime import date
from .forms import TaskForm, ContactForm
from .models import Task
from calendar import monthcalendar
from django.utils.timezone import localdate
from django.utils.timezone import now
from collections import defaultdict
from django.utils import timezone
from datetime   import datetime
@login_required
def task_list(request):
    q = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')

    today = now().date()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    # Calendar setup
    cal = Calendar(firstweekday=6).monthdayscalendar(year, month)

    # Calculate previous and next month/year
    prev_month = 12 if month == 1 else month - 1
    next_month = 1 if month == 12 else month + 1
    prev_year = year - 1 if month == 1 else year
    next_year = year + 1 if month == 12 else year

    # Task filtering
    tasks = Task.objects.filter(user=request.user)
    if q:
        tasks = tasks.filter(title__icontains=q)
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)

    # Task ordering
    tasks = tasks.order_by(
        Case(
            When(priority='High', then=Value(1)),
            When(priority='Medium', then=Value(2)),
            When(priority='Low', then=Value(3)),
            output_field=IntegerField(),
        )
    )

    # Tasks grouped by day
    tasks_by_day = defaultdict(list)
    for t in tasks:
        if t.due_date and t.due_date.year == year and t.due_date.month == month:
            tasks_by_day[t.due_date.day].append(t)

    return render(request, 'tasks/tasks.html', {
        'tasks': tasks,
        'today': today,
        'year': year,
        'month': month,
        'cal': cal,
        'tasks_by_day': dict(tasks_by_day),
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'current_month': datetime(year, month, 1).strftime('%B'),
    })

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task added successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form': form})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/edit_task.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    messages.success(request, 'Task deleted.')
    return redirect('task_list')

@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    state = 'completed' if task.completed else 'marked incomplete'
    messages.success(request, f'Task {state}.')
    return redirect('task_list')

@login_required
def update_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            task.save()
            messages.success(request, 'Status updated.')
    return redirect('task_list')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_mail(
                subject=f'Message from {name}',
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
            )
            messages.success(request, 'Message sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'tasks/contact.html', {'form': form})

@login_required
def calendar_view(request):
    today = date.today()
    cal = calendar.monthcalendar(today.year, today.month)
    tasks = Task.objects.filter(
        user=request.user,
        due_date__year=today.year,
        due_date__month=today.month
    )
    tasks_by_day = {d: [] for week in cal for d in week if d != 0}
    for t in tasks:
        tasks_by_day[t.due_date.day].append(t)
    return render(request, 'tasks/calendar.html', {
        'cal': cal,
        'year': today.year,
        'month': today.month,
        'tasks_by_day': tasks_by_day,
    })

@login_required
def toggle_star(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user in task.stars.all():
        task.stars.remove(request.user)
    else:
        task.stars.add(request.user)
    return redirect('task_list')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def custom_logout_view(request):
    logout(request)
    return redirect('login')

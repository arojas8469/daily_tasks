from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo',        'To Do'),
        ('in_progress', 'In Progress'),
        ('done',        'Done'),
    ]
    PRIORITY_CHOICES = [
        ('High',   'High'),
        ('Medium', 'Medium'),
        ('Low',    'Low'),
    ]
    CATEGORY_CHOICES = [
        ('Work',     'Work'),
        ('Personal', 'Personal'),
        ('Other',    'Other'),
    ]
    FREQUENCY_CHOICES = [
        ('daily',   'Daily'),
        ('weekly',  'Weekly'),
        ('monthly', 'Monthly'),
    ]

    # who created it
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title       = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    status   = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default='todo'
    )
    priority = models.CharField(
        max_length=6,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='Work'
    )

    due_date = models.DateField(
        null=True,
        blank=True,
        help_text="When this task is due"
    )

    # recurrence
    frequency = models.CharField(
        max_length=7,
        choices=FREQUENCY_CHOICES,
        null=True,
        blank=True,
        help_text="Repeat pattern (daily, weekly, monthly)"
    )
    interval = models.PositiveIntegerField(
        default=1,
        help_text="Repeat every N days/weeks/months"
    )

    # starring/favorites
    stars = models.ManyToManyField(
        User,
        related_name="starred_tasks",
        blank=True,
        help_text="Users who have favorited this task"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

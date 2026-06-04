from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = 'todo', 'К выполнению'
        IN_PROGRESS = 'in_progress', 'В процессе'
        DONE = 'done', 'Выполнено'

    class Priority(models.TextChoices):
        LOW = 'low', 'Низкий'
        MEDIUM = 'medium', 'Средний'
        HIGH = 'high', 'Высокий'

    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    status = models.CharField(
        'Статус', max_length=20, choices=Status.choices, default=Status.TODO
    )
    priority = models.CharField(
        'Приоритет', max_length=10, choices=Priority.choices, default=Priority.MEDIUM
    )
    due_date = models.DateField('Срок выполнения', null=True, blank=True)
    created_at = models.DateTimeField('Создана', auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Пользователь',
    )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        if self.due_date and self.status != self.Status.DONE:
            return self.due_date < timezone.now().date()
        return False

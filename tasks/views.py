from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect

from .models import Task
from .forms import TaskForm, RegisterForm


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 12

    def get_queryset(self):
        qs = Task.objects.filter(user=self.request.user)
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        q = self.request.GET.get('q', '').strip()
        if status:
            qs = qs.filter(status=status)
        if priority:
            qs = qs.filter(priority=priority)
        if q:
            qs = qs.filter(title__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status_choices'] = Task.Status.choices
        ctx['priority_choices'] = Task.Priority.choices
        ctx['current_status'] = self.request.GET.get('status', '')
        ctx['current_priority'] = self.request.GET.get('priority', '')
        ctx['current_q'] = self.request.GET.get('q', '')
        return ctx


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Задача создана.')
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task-list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Задача обновлена.')
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:task-list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Задача удалена.')
        return super().delete(request, *args, **kwargs)


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('tasks:task-list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Регистрация успешна! Добро пожаловать.')
        return redirect(self.success_url)

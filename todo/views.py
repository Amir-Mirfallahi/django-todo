from django.views.generic import FormView, ListView, UpdateView, RedirectView
from .forms import TaskForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404


class TodoManageView(LoginRequiredMixin, ListView):
    """
    This view is used to manage the tasks of the user.
    """
    paginate_by = 6
    model = Task
    template_name = 'todo/todo_manage.html'
    context_object_name = 'tasks'
    login_url = reverse_lazy('accounts:login')
    redirect_field_name = 'redirect_to'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context


    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('status', '-priority')


class CreateTaskView(LoginRequiredMixin, FormView):
    """
    This view is used to create a new task.
    """
    template_name = 'todo/task_form.html'
    form_class = TaskForm
    login_url = reverse_lazy('accounts:login')
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('todo:todo_manage')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ایجاد کار'
        return context


class UpdateTaskView(LoginRequiredMixin, UpdateView):
    """
    This view is used to update a task.
    """
    model = Task
    template_name = 'todo/task_form.html'
    form_class = TaskForm
    login_url = reverse_lazy('accounts:login')
    redirect_field_name = 'redirect_to'

    def get_success_url(self):
        return reverse_lazy('todo:todo_manage')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ویرایش کار'
        return context  
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class CompleteTaskView(LoginRequiredMixin, RedirectView):
    """
    This view is used to complete a task.
    """
    login_url = reverse_lazy('accounts:login')
    redirect_field_name = 'redirect_to'
    url = reverse_lazy('todo:todo_manage')

    def get_redirect_url(self, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'], user=self.request.user)
        task.status = not task.status
        task.save()
        return super().get_redirect_url(*args, **kwargs)


class DeleteTaskView(LoginRequiredMixin, RedirectView):
    """
    This view is used to delete a task.
    """
    login_url = reverse_lazy('accounts:login')
    redirect_field_name = 'redirect_to'
    url = reverse_lazy('todo:todo_manage')

    def get_redirect_url(self, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'], user=self.request.user)
        task.delete()
        return super().get_redirect_url(*args, **kwargs)

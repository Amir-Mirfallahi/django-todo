from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.TodoManageView.as_view(), name='todo_manage'),
    path('create/', views.CreateTaskView.as_view(), name='create_task'),
    path('update/<int:pk>/', views.UpdateTaskView.as_view(), name='update_task'),
    path('complete/<int:pk>/', views.CompleteTaskView.as_view(), name='complete_task'),
    path('delete/<int:pk>/', views.DeleteTaskView.as_view(), name='delete_task'),
]

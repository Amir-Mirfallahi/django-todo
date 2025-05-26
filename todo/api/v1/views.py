from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from todo.models import Task
from .serializers import TaskSerializer
from .permissions import IsOwner

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint for tasks management
    """
    serializer_class = TaskSerializer
    
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        """
        Filter tasks to return only those belonging to the current user
        """
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Set the user of the task as the current authenticated user
        """
        serializer.save(user=self.request.user)
        
    @action(detail=True, methods=['get'])
    def toggle_status(self, request, pk=None):
        """
        Toggle the status of a task (complete/incomplete)
        """
        task = self.get_object()
        task.status = not task.status
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

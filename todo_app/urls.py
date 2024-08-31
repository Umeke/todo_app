# todo_app/urls.py
from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet
from django.urls import path

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
urlpatterns = [
    path('api/authenticate/', authenticate_user, name='authenticate_user'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('test/', test_view, name='test'),
    path('task-list/', TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('task/create/', TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('task/<int:pk>/toggle-status/', ToggleTaskStatusView.as_view(), name='toggle_task_status'),

]+ router.urls

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.views import View
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')  # Замените на нужное представление после входа
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('task_list')  # Замените на нужное представление после входа
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Переход на страницу входа после выхода

def test_view(request):
    return render(request, 'registration/test.html')





# Create your views here.
# View for listing tasks
from django.views.generic import ListView
from .models import Task


class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    ordering = ['-created_at']  # Default ordering

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        sort_by = self.request.GET.get('sort_by')

        # Filter by status
        if status:
            if status == 'completed':
                queryset = queryset.filter(status=True)
            elif status == 'incomplete':
                queryset = queryset.filter(status=False)

        # Sort by sort_by parameter
        if sort_by:
            if sort_by == 'date_created':
                queryset = queryset.order_by('created_at')
            elif sort_by == 'status':
                queryset = queryset.order_by('status')

        # Ensure tasks are only visible to the logged-in user
        queryset = queryset.filter(user=self.request.user)

        return queryset


# View for displaying task details
class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'status']
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):

        form.instance.user = self.request.user
        return super().form_valid(form)

# View for updating an existing task
class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'status']

    def get_success_url(self):
        return reverse('task_detail', kwargs={'pk': self.object.pk})

# View for deleting a task
class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')


class ToggleTaskStatusView(View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.status = not task.status
        task.save()
        return redirect('task_list')





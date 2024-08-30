from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task

class AuthViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.task_list_url = reverse('task_list')
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_register_view(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': '123456789@qwe',
            'password2': '123456789@qwe',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.task_list_url)
        self.assertTrue(User.objects.filter(username='newuser').exists())

        # Verify that the email was correctly saved
        new_user = User.objects.get(username='newuser')
        self.assertEqual(new_user.email, 'newuser@example.com')

    def test_login_view(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'password',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.task_list_url)

    def test_logout_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)




class TaskViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.task_list_url = reverse('task_list')
        self.task_create_url = reverse('task_create')
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            status=False,
            user=self.user,
        )
        self.task_detail_url = reverse('task_detail', kwargs={'pk': self.task.pk})
        self.task_update_url = reverse('task_update', kwargs={'pk': self.task.pk})
        self.task_delete_url = reverse('task_delete', kwargs={'pk': self.task.pk})
        self.toggle_status_url = reverse('toggle_task_status', kwargs={'pk': self.task.pk})

    def test_task_list_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')

    def test_task_detail_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.task_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_detail.html')

    def test_task_create_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.task_create_url, {
            'title': 'New Task',
            'description': 'New Description',
            'status': False,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.task_list_url)
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_task_update_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.task_update_url, {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'status': True,
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.description, 'Updated Description')
        self.assertEqual(self.task.status, True)
        # 123

    def test_task_delete_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.task_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.task_list_url)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_toggle_task_status_view(self):
        self.client.login(username='testuser', password='password')
        initial_status = self.task.status
        response = self.client.post(self.toggle_status_url)
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertNotEqual(self.task.status, initial_status)

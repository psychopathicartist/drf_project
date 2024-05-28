from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='testuser@myapp.ru', password='123')
        self.course = Course.objects.create(name='Тестовый курс', description='Нужен для теста')
        self.lesson = Lesson.objects.create(name='Тестовый урок', description='Нужен для теста', course=self.course,
                                            video='https://www.youtube.com/', author=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('materials:lesson-view', args=[self.lesson.pk])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), self.lesson.name)

    def test_lesson_create(self):
        url = reverse('materials:lesson-create')
        data = {'name': 'Тестовый урок 2', 'description': 'Тоже нужен для теста', 'course': '1'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse('materials:lesson-edit', args=[self.lesson.pk])
        data = {'name': 'Тестовый урок 2'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), 'Тестовый урок 2')

    def test_lesson_delete(self):
        url = reverse('materials:lesson-delete', args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse('materials:lesson-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.all().count(), 1)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='testuser@myapp.ru', password='123')
        self.course = Course.objects.create(name='Тестовый курс', description='Нужен для теста')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('materials:subscription')
        self.data = {"course": self.course.id}

    def test_subscription_create(self):
        response = self.client.post(self.url, self.data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('message'), 'Подписка добавлена')

    def test_subscription_delete(self):
        self.client.post(self.url, self.data)
        response = self.client.post(self.url, self.data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('message'), 'Подписка удалена')

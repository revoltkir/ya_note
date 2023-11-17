from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestContent(TestCase):
    HOME_URL = reverse('notes:home')
    LIST_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        Note.objects.bulk_create(
            Note(title=f'Новость {index}', slug=f'Slug{index}', text='Просто текст.', author=cls.author)
            for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
        )

    def test_news_count(self):
        self.client.force_login(self.author)
        response = self.client.get(self.LIST_URL)
        object_list = response.context['object_list']
        news_count = len(object_list)
        # print(news_count)
        self.assertEqual(news_count, settings.NEWS_COUNT_ON_HOME_PAGE)

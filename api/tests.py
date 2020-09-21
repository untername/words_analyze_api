from rest_framework.test import APITestCase
from rest_framework import status
from .models import Analyzer


class TestModel(APITestCase):

    """ Тестирование модели. """

    @classmethod
    def setUpTestData(cls) -> None:
        Analyzer.objects.create(method='antonyms', text='Code without tests is broken as designed.')

    def test_obj(self) -> None:
        obj = Analyzer.objects.get(id=1)
        field: str = obj._meta.get_field('method').verbose_name
        second_field: str = obj._meta.get_field('text').verbose_name

        self.assertEqual(field, 'method')
        self.assertEqual(second_field, 'text')
        self.assertTrue('antonyms' in obj.method)


class ViewTest(APITestCase):

    """ Тестирование view-класса. """

    @classmethod
    def setUpTestData(cls) -> None:
        Analyzer.objects.create(method='tranlate', text='Code without tests is broken as designed')

    def test_view(self) -> None:
        response = self.client.get('/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Analyzer.objects.count(), 1)


class TestRequest(APITestCase):

    """ Тестирование POST-запроса. """

    def test_post(self) -> None:

        response = self.client.post(
            '/', data={"text": "Code without tests is broken as designed", "method": "translate"})

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

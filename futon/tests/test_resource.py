from unittest.mock import patch

from django.test import SimpleTestCase, TestCase
from rest_framework.serializers import ModelSerializer

from ..models import Token, Site
from ..resource import Resource


class MySerializer(ModelSerializer):
    class Meta:
        model = Token


class MyResource(Resource):
    model = Token
    serializer = MySerializer
    endpoint = '/api/blah'
    domain = 'http://domain.com'
    mapping = {
        'site': 'site',
        'token': 'token',
    }


RESULTS = {
    'results': [
        {
            'id': 0,
            'site': '1',
            'token': 'b2',
        },
        {
            'id': 1,
            'site': '1',
            'token': 'a1',
        },
    ],
}


class ResourceTestCase(TestCase):

    def setUp(self):
        Site.objects.get_or_create(domain='http://domain.com', name='test')

    @patch('futon.resource.fetch', return_value=RESULTS)
    def test_resource(self, fetch):
        self.assertEqual(Token.objects.all().count(), 0)
        MyResource.sync()
        self.assertEqual(Token.objects.all().count(), 2)

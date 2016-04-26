# from unittest.mock import patch
# import logging

# from django.test import SimpleTestCase, TestCase
# from django.contrib.sites.models import Site
# from rest_framework import serializers, viewsets
# from rest_framework.exceptions import ValidationError

# from ..models import Token
# from ..tasks import pull_viewset
# from .. import tasks


# logging.disable(logging.CRITICAL)


# class SiteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Site


# class TokenSerializer(serializers.ModelSerializer):
#     site = serializers.SlugRelatedField(queryset=Site.objects.all(), slug_field='name')

#     class Meta:
#         model = Token


# class SiteViewSet(viewsets.ModelViewSet):
#     queryset = Site.objects.all()
#     serializer_class = SiteSerializer


# class TokenViewSet(viewsets.ModelViewSet):
#     queryset = Token.objects.all()
#     serializer_class = TokenSerializer


# class PullViewSetTestCase(SimpleTestCase):

#     def setUp(self):
#         self.site, created = Site.objects.get_or_create(domain='http://localhost', name='test')

#     @patch.object(tasks, 'fetch')
#     def test_basic_model(self, fetch):
#         fetch.return_value = {
#             'results': [{
#                 'id': 10,
#                 'domain': 'http://hello',
#                 'name': 'world',
#             }]
#         }
#         pull_viewset(self.site, SiteViewSet(), '/blah')
#         obj = Site.objects.get(id=10)
#         self.assertEqual(obj.domain, 'http://hello')
#         self.assertEqual(obj.name, 'world')

#     @patch.object(tasks, 'fetch')
#     def test_foreign_key_does_not_exist(self, fetch):
#         fetch.return_value = {
#             'results': [{
#                 'id': 10,
#                 'token': 'hello',
#                 'site': 'second',
#             }]
#         }
#         with self.assertRaises(ValidationError):
#             pull_viewset(self.site, TokenViewSet(), '/blah')

#     @patch.object(tasks, 'fetch')
#     def test_foreign_key_exists(self, fetch):
#         fetch.return_value = {
#             'results': [{
#                 'id': 10,
#                 'token': 'hello',
#                 'site': self.site.name,
#             }]
#         }
#         pull_viewset(self.site, TokenViewSet(), '/blah')
#         obj = Token.objects.get(id=10)
#         self.assertEqual(obj.token, 'hello')
#         self.assertEqual(obj.site.id, self.site.id)
#         self.assertEqual(obj.site.name, self.site.name)
#         self.assertEqual(obj.site.domain, self.site.domain)

#     # def test_many_to_many(self):
#     #     # TODO
#     #     pass

#     @patch.object(tasks, 'fetch')
#     def test_update_model(self, fetch):
#         fetch.return_value = {
#             'results': [{
#                 'id': self.site.id,
#                 'name': 'hello',
#                 'domain': 'http://world',
#             }]
#         }
#         pull_viewset(self.site, SiteViewSet(), '/blah')
#         obj = Site.objects.get(id=self.site.id)
#         self.assertEqual(obj.name, 'hello')
#         self.assertEqual(obj.domain, 'http://world')

#     @patch.object(tasks, 'fetch')
#     def test_deleteion(self, fetch):
#         fetch.return_value = {
#             'results': []
#         }
#         pull_viewset(self.site, SiteViewSet(), '/blah')
#         self.assertEqual(len(Site.objects.all()), 0)

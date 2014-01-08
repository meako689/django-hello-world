from django.test import TestCase
from django.test.client import RequestFactory

from hello.models import User
from watchr.middleware import RequestRecordMiddleware
from watchr.models import RecordedRequest

class MiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@example.com', password='top_secret')
        
    def test_record_request(self):
        """Test that request object is correctly saved into db"""
        r = self.factory.get('/')
        r.user = self.user
        m = RequestRecordMiddleware()
        self.assertEqual(RecordedRequest.objects.count(),0)
        m.process_request(r)
        self.assertEqual(RecordedRequest.objects.count(),1)
        obj = RecordedRequest.objects.all()[0]
        self.assertEqual(obj.user, self.user)
        self.assertEqual(obj.path, '/')

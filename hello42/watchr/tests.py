from django.test import TestCase
from django.test import Client
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser

from hello.models import User
from watchr.middleware import RequestRecordMiddleware
from watchr.models import RecordedRequest

class MiddlewareTestCase(TestCase):
    def setUp(self):
        self.f = RequestFactory()
        self.u = User.objects.create_user(
            username='jacob', email='jacob@example.com', password='top_secret')
        
    def test_record_request(self):
        """Test that request object is correctly saved into db"""
        r = self.f.get('/')
        r.user = self.u
        m = RequestRecordMiddleware()
        self.assertEqual(RecordedRequest.objects.count(),0)
        m.process_request(r)
        self.assertEqual(RecordedRequest.objects.count(),1)
        obj = RecordedRequest.objects.all()[0]
        self.assertEqual(obj.user, self.u)
        self.assertEqual(obj.path, '/')

class TestViews(TestCase):
    def setUp(self):
        self.c = Client()
        self.f = RequestFactory()
        self.u = User.objects.create_user(
            username='jacob', email='jacob@example.com', password='top_secret')
        m = RequestRecordMiddleware()

        for i in xrange(10):
            r = self.f.get('/')
            r.user = self.u if i % 2 else AnonymousUser()
            m.process_request(r)

    def test_show_request_list(self):
        response = self.c.get(reverse('request_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.u.username)
        for req in RecordedRequest.objects.order_by('-id')[:10]:
            self.assertContains(response, req.id)
            self.assertContains(response, req.path)

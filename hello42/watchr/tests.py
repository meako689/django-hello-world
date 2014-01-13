from django.test import TestCase
from django.test import Client
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser

from hello.models import User
from watchr.middleware import RequestRecordMiddleware
from watchr.models import RecordedRequest, ModelChangeRecord

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
        self.assertEqual(RecordedRequest.objects.count(),11)
        for req in RecordedRequest.objects.order_by('time')[:10]:
            self.assertContains(response, req.path)
            self.assertTrue(req in response.context['request_list'])
        unwanted_req = RecordedRequest.objects.latest('id')
        self.assertFalse(unwanted_req in response.context['request_list'])

    def test_ordering_for_request_list(self):
        response = self.c.get(reverse('request_list'), {'order_by':'user'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.u.username)
        self.assertEqual(RecordedRequest.objects.count(),11)
        for req in RecordedRequest.objects.order_by('user')[:10]:
            self.assertContains(response, req.path)
            self.assertTrue(req in response.context['request_list'])
        unwanted_req = RecordedRequest.objects.latest('user')
        self.assertFalse(unwanted_req in response.context['request_list'])

        response = self.c.get(reverse('request_list'), {'order_by':'-user'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.u.username)
        self.assertEqual(RecordedRequest.objects.count(),12)
        for req in RecordedRequest.objects.order_by('-user')[:10]:
            self.assertContains(response, req.path)
            self.assertTrue(req in response.context['request_list'])
        unwanted_req = RecordedRequest.objects.earliest('user')
        self.assertFalse(unwanted_req in response.context['request_list'])

        response = self.c.get(reverse('request_list'), {'order_by':'path'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.u.username)
        self.assertEqual(RecordedRequest.objects.count(),13)
        for req in RecordedRequest.objects.order_by('path')[:10]:
            self.assertContains(response, req.path)
            self.assertTrue(req in response.context['request_list'])
        unwanted_req = RecordedRequest.objects.latest('path')
        self.assertFalse(unwanted_req in response.context['request_list'])

        response = self.c.get(reverse('request_list'), {'order_by':'wat'})
        self.assertEqual(response.status_code, 200)

class TestContextProcessor(TestCase):
    def test_processing_context(self):
        c = Client()
        resp = c.get('/')
        self.assertTrue('settings' in resp.context)

class TestSignalWatcher(TestCase):
    def test_create_uodate_delete(self):
        """everything should be recorded"""
        self.assertEqual(ModelChangeRecord.objects.count(),0)
        self.u = User.objects.create_user(
            username='jacob2', email='jacob@example.com', password='top_secret')
        self.assertEqual(ModelChangeRecord.objects.count(),1)
        rec = ModelChangeRecord.objects.all()[0]
        self.assertEqual(rec.action, 1)
        self.assertEqual(rec.content_object, self.u)
        self.u.first_name="blaaah"
        self.u.save()
        self.assertEqual(ModelChangeRecord.objects.count(),2)
        rec = ModelChangeRecord.objects.all()[1]
        self.assertEqual(rec.action, 2)
        self.assertEqual(rec.content_object, self.u)
        self.u.delete()
        self.assertEqual(ModelChangeRecord.objects.count(),3)
        rec = ModelChangeRecord.objects.all()[2]
        self.assertEqual(rec.action, 3)
        self.assertEqual(rec.shelfed_object[0]['pk'], 1)

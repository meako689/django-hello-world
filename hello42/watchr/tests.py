from django.test import (TestCase,Client)


class TestContextProcessor(TestCase):
    def test_processing_context(self):
        """docstring for test_processing_context"""
        c = Client()
        resp = c.get('/')
        self.assertTrue('settings' in resp.context)

        

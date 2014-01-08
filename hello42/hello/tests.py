from datetime import datetime

from django.core.urlresolvers import reverse
from django.test import (TestCase,Client)

from hello42.hello.models import User

# Create your tests here.

class UserProfileTestCase(TestCase):
    def setUp(self):
        self.u = User(username='testuser',
                first_name='Test',
                last_name='User',
                email='e@example.com',
                date_of_birth=datetime(1981,1,1).date(),
                jabber='j@example.com',
                skype='testuser',
                bio='Born to test',
                other_contacts='call the rail')
        self.u.save()

        self.c = Client()

    def test_show_bio_page(self):
        response = self.c.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.u.email)
        self.assertContains(response, self.u.first_name)
        self.assertContains(response, self.u.last_name)
        self.assertContains(response, self.u.jabber)
        self.assertContains(response, self.u.skype)
        self.assertContains(response, self.u.bio)
        self.assertContains(response, self.u.other_contacts)
        self.assertContains(response, self.u.date_of_birth.strftime("%Y-%m-%d"))





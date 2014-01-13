import os
import datetime
import subprocess

from datetime import datetime

from django.core.urlresolvers import reverse
from django.test import (TestCase,Client)
from django.conf import settings

from hello42.hello.models import User, DEFAULT_DIMENSIONS

# Create your tests here.

class UserProfileTestCase(TestCase):
    def setUp(self):
        self.u = User.objects.create_superuser(username='testuser',
                password='pass',
                first_name='Test',
                last_name='User',
                email='e@example.com',
                date_of_birth=datetime(1981,1,1).date(),
                jabber='j@example.com',
                skype='testuser',
                bio='Born to test',
                other_contacts='call the rail')

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

    def test_edit_page(self):
        url = reverse('user_edit', kwargs={'pk':self.u.pk})
        response = self.c.get(url)
        self.assertEqual(response.status_code, 302)
        self.c.login(username=self.u.username, password='pass')
        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        data = form.initial
        data['last_name'] = 'Wrrroooom'
        data.pop('photo') #otherwise fail
        self.c.post(url, data)
        u = User.objects.get(pk=self.u.pk)
        self.assertEqual(u.last_name, 'Wrrroooom')

    def test_edit_a_photo(self):
        """Upload a photo and check that it will resize"""
        url = reverse('user_edit', kwargs={'pk':self.u.pk})
        self.c.login(username=self.u.username, password='pass')
        response = self.c.get(url)
        form = response.context['form']
        data = form.initial
        f = open(os.path.join(
            os.path.dirname(__file__),
            'testfiles/1024magrittesonofman.jpg')
        )
        data['photo'] = f
        self.c.post(url, data)
        response = self.c.get(url)
        self.assertContains(response, '1024magrittesonofman')
        u = User.objects.get(pk=self.u.pk)
        self.assertTrue(u.photo)
        self.assertEqual((u.photo.width,u.photo.height), DEFAULT_DIMENSIONS)
        os.unlink(u.photo.path)

    def test_admin_edit_link(self):
        self.c.login(username=self.u.username, password='pass')
        response = self.c.get(reverse('home'))
        adminlink='href="/admin/hello/user/{id}/"'.format(id=self.u.id)
        self.assertTrue(adminlink in response.content)
        self.u.is_staff = False
        self.u.save()
        response = self.c.get(reverse('home'))
        self.assertFalse(adminlink in response.content)

    def test_modellist_script(self):
        """test shell script which prints list of models"""
        path_to_script = settings.BASE_DIR+'/listmodels.sh'
        rx=subprocess.Popen(['/usr/bin/env', 'bash',
            path_to_script],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = rx.stdout.read(), rx.stderr.read()
        self.assertEqual(err,'')
        self.assertNotEqual(out,'')
        self.assertTrue('Session:1' in out)
        filename = datetime.now().date().strftime('%d_%m_%Y')+'.dat'
        filename = settings.BASE_DIR+'/'+filename
        file = open(filename, 'r')
        res = file.read()
        self.assertTrue('error' in res)
        self.assertTrue('Session:1' in res)
        file.close()
        os.unlink(filename)



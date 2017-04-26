from django.test import TestCase
from pestyle.models import *
from pestyle.lists import *
from datetime import datetime
from django.core.management import call_command
from django.test import Client
from django.urls import reverse

#замена print(), django так крут, что не даёт выводить инфу в тесте принтом, написание тестов превращается в еблю
#но костыль приходит на помощь и выводит инфу
def prtest(e):
    call_command('prtest', e=e)

class MyTestCase(TestCase):
    fixtures = ['te44st_db.json']
    @classmethod
    def setUpTestData(cls):
        call_command('fill_test')

    def setUp(self):
        self.user = User.objects.get(email='test@test.ru')

    def test_like_look_if_not_logged_in(self):
        c = Client()
        r = c.post(reverse('like_look'), {'look_id': 1,})
        self.assertRedirects(r, '/login_window/?next=/api/like_look/', target_status_code=302)


    def test_like_look_wrong_data(self):
        c = Client(enforce_csrf_checks=True)
        c.login(email=self.user.email, password='1')
        r = c.post(reverse('like_look'), {'look_id': Look.objects.exclude(user=self.user).order_by('?').first(),})
        self.assertEqual(r.status_code, 403)


    def test_like_look(self):
        c = Client()
        c.login(email=self.user.email, password='1')
        lid = Look_suggestions.objects.filter(user=self.user).order_by('?').first()
        r = c.post(reverse('like_look'), { 'look_id': lid.pk,})
        self.assertJSONEqual(
            str(r.content, encoding='utf8'),
            {'status': 'ok', 'look_id': lid.pk,}
        )

    '''def test_redirect_if_not_logged_in(self):
        c = Client(enforce_csrf_checks=True)
        resp = c.get('/look_choice/')
        self.assertRedirects(resp, '/login_window/?next=/look_choice/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(email=self.user.email, password='1')
        resp = self.client.get(reverse('look_choice'))
        #Check our user is logged in
        self.assertEqual(str(resp.context['user']), str(self.user))
        #Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)
        #Check we used correct template
        self.assertTemplateUsed(resp, 'look_choice.html')'''

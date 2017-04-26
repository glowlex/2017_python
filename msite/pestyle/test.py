from django.test import TestCase
from pestyle.models import *
from pestyle.lists import *
from datetime import datetime
from django.core.management import call_command
from django.test import Client
from django.urls import reverse
from django.core.exceptions import EmptyResultSet, ObjectDoesNotExist
from django.core import serializers
from django.db.models import Q
import json

#замена print(), django так крут, что не даёт выводить инфу в тесте принтом, написание тестов превращается в еблю
#но костыль приходит на помощь и выводит инфу
nexist_id = 10000

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
        c = Client()
        c.login(email=self.user.email, password='1')
        #объект другого юзера
        r = c.post(reverse('like_look'), {'look_id': Look.objects.exclude(user=self.user).order_by('?').first().pk,})
        self.assertEqual(r.status_code, 403)
        #объекта нет
        r = c.post(reverse('like_look'), {'look_id': nexist_id,})
        self.assertEqual(r.status_code, 403)

    def test_like_look(self):
        c = Client()
        c.login(email=self.user.email, password='1')
        lid = Look_suggestions.objects.filter(user=self.user).order_by('?').first()
        r = c.post(reverse('like_look'), { 'look_id': lid.pk if lid else 0,})
        self.assertJSONEqual(
            str(r.content, encoding='utf8'),
            {'status': 'ok', 'look_id': lid.pk if lid else 0,}
        )

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(email=self.user.email, password='1')
        resp = self.client.get(reverse('look_choice'))
        #Check our user is logged in
        self.assertEqual(str(resp.context['user']), str(self.user))
        #Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)
        #Check we used correct template
        self.assertTemplateUsed(resp, 'look_choice.html')

    def test_delete_item(self):
        c = Client()
        c.login(email=self.user.email, password='1')
        item = Item.objects.filter(user=self.user).order_by('?').first()
        r = c.post(reverse('delete_item'), { 'item_id': item.pk,})
        self.assertJSONEqual(
            str(r.content, encoding='utf8'),
            {'status': 'ok'}
        )
        self.assertEqual(Item.objects.filter(pk=item.pk).count(), 0)

    def test_delete_item_wrong_data(self):
        c = Client()
        c.login(email=self.user.email, password='1')
        #объект другого юзера
        r = c.post(reverse('delete_item'), {'item_id': Item.objects.exclude(user=self.user).order_by('?').first().pk,})
        self.assertEqual(r.status_code, 403)
        #объекта нет
        r = c.post(reverse('delete_item'), {'item_id': nexist_id,})
        self.assertEqual(r.status_code, 403)

    def test_set_item(self):
        c = Client()
        c.login(email=self.user.email, password='1')
        item_type = ITEM_TYPE_LIST[1][0]
        style = STYLE_LIST[1][0]
        color = COLOR_LIST[1][0]
        season = SEASON_LIST[1][0]
        temperature = TEMPERATURE_LIST[1][0]
        sky = SKY_LIST[1][0]

        item = Item.objects.filter(user=self.user).order_by('?').first()
        r = c.post(reverse('set_item'), {'item_id': item.pk, 'item_type':item_type, 'style': style, 'color':color, 'season':season,
        'temperature':temperature, 'sky':sky})
        item = Item.objects.filter(pk=item.pk)
        self.assertJSONEqual(
            r.content,
            serializers.serialize('json', item)
        )
        self.assertEqual(item.first().item_type, item_type)

    def test_set_item_wrong_data(self):
        c = Client()
        c.login(email=self.user.email, password='1')
        item_type = ITEM_TYPE_LIST[1][0]
        style = STYLE_LIST[1][0]
        color = COLOR_LIST[1][0]
        season = SEASON_LIST[1][0]
        temperature = TEMPERATURE_LIST[1][0]
        sky = SKY_LIST[1][0]

        item = Item.objects.exclude(user=self.user).order_by('?').first()
        #объект другого юзера
        r = c.post(reverse('delete_item'), {'item_id': item.pk, 'item_type':item_type, 'style': style, 'color':color, 'season':season,
        'temperature':temperature, 'sky':sky})
        self.assertEqual(r.status_code, 403)
        #объекта нет
        r = c.post(reverse('delete_item'), {'item_id': nexist_id, 'item_type':item_type, 'style': style, 'color':color, 'season':season,
        'temperature':temperature, 'sky':sky})
        self.assertEqual(r.status_code, 403)

    def test_get_items(self):
        c = Client()
        c.login(email=self.user.email, password='1')
        qu = Q(item_type=ITEM_TYPE_LIST[1][0]) | Q(item_type=ITEM_TYPE_LIST[4][0])
        items = Item.objects.filter(Q(user=self.user.id) & qu).order_by('-pk')
        l = list()
        l.append(ITEM_TYPE_LIST[1][0])
        l.append(ITEM_TYPE_LIST[4][0])
        r = c.get(reverse('get_items'), { 'itype': json.dumps(l),})
        self.assertJSONEqual(
            r.content,
            serializers.serialize('json', items)
        )











#end

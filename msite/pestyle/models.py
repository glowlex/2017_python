from django.db import models

from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from pestyle.lists import *
from django.conf import settings
import os

#для хитрых имён
from uuid import uuid4
from django.utils.deconstruct import deconstructible
@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)


class MyUserManager(BaseUserManager):
	def create_user(self, email, name, sex, city, password=None, last_name=None, birthday=None, avatar=None, **kwargs):
		#пароля нет, чтобы авторизоваться через сторонние сервисы, но тут почта уникальна. TODO:нужно поправить
		if not email:
			raise ValueError('Users must have an email')

		user = self.model(name=name, last_name=last_name, email =email,
		 sex =sex, birthday =birthday, city=city, password=password, avatar =avatar)
		if avatar:
			user.avatar.save("a.jpg", avatar, save=True)
		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_superuser(self, name, email, sex, birthday, city, password, last_name=None, avatar=None):
		user = self.create_user(email, name, sex, birthday, city, password,  last_name)
		user.is_admin = True
		user.save(using=self._db)
		return user




class User(AbstractBaseUser):
	name = models.CharField(max_length=32)
	last_name = models.CharField(max_length=32, blank=True, null=True)
	email = models.EmailField(max_length=64, unique=True)
	sex = models.CharField(max_length=1, choices=SEX_LIST, default=SEX_LIST[1][1])
	birthday = models.DateField(blank=True, null=True)
	city = models.IntegerField(default=524901) #москва
	#static/images/ для отладочного серва, просто avatar/ для nginx
	avatar = models.ImageField(upload_to=PathAndRename('avatar/'), blank=True, null=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name', 'sex', 'birthday', 'city',]
	objects = MyUserManager()
	def __str__(self):
		return u'%s %s' % (self.name, self.last_name)

	def get_avatar(self):
		return self.avatar

	def get_short_name(self):
		return self.name

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return True

	def get_full_name(self):
		return self.name

	def get_short_name(self):
		return self.name

	def set_avatar(self, avatar):
		if self.avatar:
			try:
				os.remove(self.avatar.path)
			except OSError:
				pass
		self.avatar.save("a.jpg", avatar, save=True)





class Event(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateField()
	event_type = models.CharField(max_length=1, choices=STYLE_LIST,)
	description = models.CharField(max_length=256, blank=True, null=True)
	name = models.CharField(max_length=32)

	class Meta:
		db_table = 'Calendar'
		ordering = ['-pk']



	@classmethod
	def create_event(cls, user, date, event_type, name='blank', description=None):
		event =cls(user=user, date=date, event_type=event_type, name=name, description=description)
		event.save()
		return event

	def __str__(self):
		return u'%s' % self.user.email




class Item(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	item_type = models.CharField(max_length=16, choices=ITEM_TYPE_LIST)
	photo = models.ImageField(upload_to=PathAndRename('item_photo/'),)
	style= models.CharField(max_length=1, choices=STYLE_LIST,)
	color = models.CharField(max_length=16, choices=COLOR_LIST)
	season = models.CharField(max_length=2, choices=SEASON_LIST)
	temperature = models.CharField(max_length=16, choices=TEMPERATURE_LIST)
	sky = models.CharField(max_length=8, choices=SKY_LIST)
	last_date = models.DateField(blank=True, null=True, )
	rate = models.IntegerField(default=0)
	#likes = models.ForeignKey('Like', on_delete=models.SET_NULL, null=True)

	class Meta:
		db_table = 'Items'
		get_latest_by = 'last_date'
		ordering = ['item_type']
		indexes = [
			models.Index(fields=['user', 'item_type']),
		]


	@classmethod
	def create_item(cls, user, item_type, photo, style, color, season, temperature, sky, rate=0, last_date =None,):
		item =cls(user =user, item_type =item_type, photo =photo, style =style,
		 color =color, season =season, temperature =temperature, sky =sky, last_date =last_date, rate=rate)
		item.photo.save("i.jpg", photo, save=True)
		item.save()
		return item

	def delete(self):
		for l in self.look_set.all():
			l.delete()
		super(Item, self).delete()

	def __str__(self):
		return u'%s' % self.item_type




#TODO разобраться в наследовании в разные таблицы, или перенести предложеные хранение в оперативке
class Look(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	style= models.CharField(max_length=1, choices=STYLE_LIST,)
	items = models.ManyToManyField(Item)
	class Meta:
		db_table = 'Look_like'
		ordering = ['-pk']

	@classmethod
	def create_look(cls, user, style, items):
		if len(items)<1:
			raise ValueError('not enough items')
		look =cls(user=user, style=style)
		look.save()
		if isinstance(items[0], Item):
			for i in items:
				item = Item.objects.get(pk=i.pk)
				look.items.add(item)
		else:
			for i in items:
				item = Item.objects.get(pk=i)
				look.items.add(item)
		return look

	def __str__(self):
		return u'%s' % self.user.email


class Look_suggestions(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	style= models.CharField(max_length=1, choices=STYLE_LIST,)
	items = models.ManyToManyField(Item)
	like = models.BooleanField(default=False)
	class Meta:
		db_table = 'Look_suggestions'
		ordering = ['-pk']
	@classmethod
	def create_look(cls, user, style, items, like=False):
		if len(items)<1:
			raise ValueError('not enough items')
		look =cls(user=user, style=style)
		look.save()
		if isinstance(items[0], Item):
			for i in items:
				item = Item.objects.get(pk=i.pk)
				look.items.add(item)
		else:
			for i in items:
				item = Item.objects.get(pk=i)
				look.items.add(item)
		return look

	def set_like(self, up=True):
		self.like = True if up else False
		self.save()

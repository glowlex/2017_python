from django.db import models

from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from pestyle.lists import *
from django.conf import settings


class MyUserManager(BaseUserManager):
	def create_user(self, name, email, sex, birthday, city, password=None, last_name=None, avatar=None):
		if not login:
			raise ValueError('Users must have an login')

		user = self.model(name=name, last_name=last_name, email =email, sex =sex, birthday =birthday, city=city, password=password, avatar =avatar)
		if avatar:
			user.avatar=avatar
			user.set_password(password)
			user.save(using=self._db)
			return user

	def create_superuser(self, name, email, sex, birthday, city, password, last_name=None, avatar=None):
		user = self.create_user(name, last_name, email, sex, birthday, city, password)
		user.is_admin = True
		user.save(using=self._db)
		return user




class User(AbstractBaseUser):
	name = models.CharField(max_length=32)
	last_name = models.CharField(max_length=32, blank=True)
	email = models.EmailField(max_length=64, unique=True)
	sex = models.CharField(max_length=1, choices=(('M', 'male'), ('F', 'female')))
	birthday = models.DateField()
	city = models.IntegerField()
	avatar = models.FilePathField(path=settings.FILE_PATH_FIELD_DIRECTORY, allow_folders=True, blank=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name', 'sex', 'birthday', 'city',]
	objects = MyUserManager()
	def __unicode__(self):
		return self.name + " " + self.last_name

	def get_avatar(self):
		return self.avatar

	def get_short_name(self):
		return self.name




class Event(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateField()
	event_type = models.CharField(max_length=1, choices=STYLE_LIST,)
	description = models.CharField(max_length=256, blank=True)
	name = models.CharField(max_length=32)

	class Meta:
		db_table = 'Calendar'

	@classmethod
	def create_event(cls, user, date, event_type, name, description=None):
		event =cls(user, date, event_type, name, description)
		event.save()
		return event

	def __unicode__(self):
		return self.user




class Item(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	item_type = models.CharField(max_length=16, choices=ITEM_TYPE_LIST)
	photo = models.FilePathField(path=settings.FILE_PATH_FIELD_DIRECTORY, allow_folders=True)
	style= models.CharField(max_length=1, choices=STYLE_LIST,)
	color = models.CharField(max_length=16, choices=COLOR_LIST)
	season = models.CharField(max_length=2, choices=SEASON_LIST)
	temperature = models.CharField(max_length=16, choices=TEMPERATURE_LIST)
	sky = models.CharField(max_length=8, choices=SKY_LIST)
	last_date = models.DateField(blank=True)
	#likes = models.ForeignKey('Like', on_delete=models.SET_NULL, null=True)

	class Meta:
		db_table = 'Items'

	@classmethod
	def create_item(cls, user, item_type, photo, style, color, season, temperature, sky, last_date =None):
		item =cls(user, user =user, item_type =item_type, photo =photo, style =style,
		 color =color, season =season, temperature =temperature, sky =sky, last_date =last_date)
		item.save()
		return item

	def delete(self):
		for l in self.look_set.all():
			l.delete()
		super(Item, self).delete()

	def __unicode__(self):
		return self.item_type 






class Look(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	style= models.CharField(max_length=1, choices=STYLE_LIST,)
	items = models.ManyToManyField(Item)
	class Meta:
		db_table = 'Look_like'

	@classmethod
	def create_look(cls, user, style, items):
		look =cls(user=user, style=style)
		look.save()
		for i in items:
			item = Item.objects.get(pk=i)
			look.items.add(item)
		return look

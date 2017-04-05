from django.db import models

from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from pestyle.lists import *


class MyUserManager(BaseUserManager):
	def create_user(self, login, nick, email, password=None, avatar=None):
		if not login:
			raise ValueError('Users must have an login')

		user = self.model(login=login, nick = nick, email=email,)
		if avatar:
			user.avatar=avatar
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, login, nick, email, password):
		user = self.create_user(login, nick, email, password)
		user.is_admin = True
		user.save(using=self._db)
		return user




class User(AbstractBaseUser):
	name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32, blank=True)
    email = models.EmailField(max_length=64, unique=True)
    sex = models.CharField(max_length=1, choices=(('M'), ('F')))
    birthday = models.DateField()
    city = models.DecimalField()

	is_admin = models.BooleanField(default=False)
	avatar = models.CharField(max_length=255, blank=True)
	USERNAME_FIELD = 'login'
	REQUIRED_FIELDS = ['email', 'nick']
	objects = MyUserManager()
	def __unicode__(self):
		return self.login

	def get_full_name(self):
		return self.login

	def get_short_name(self):
		return self.nick

	def has_perm(self, perm, obj=None):
		return True
	def has_module_perms(self, app_label):
		return True
	def get_avatar(self):
		return "/upload/" + self.avatar


	@property
	def is_staff(self):
		return True





class Event(models.Model):
    user = model.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    event_type = models.CharField(max_length=1, choices=STYLE_LIST,)
    description = models.CharField(max_length=256, blank=True)
    name = models.CharField(max_length=32)

    class Meta:
        db_table = 'Calendar'





class Item(models.Model):
    user = model.ForeignKey(User, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=16, choices=ITEM_TYPE_LIST)
    photo = models.FilePathField(path=settings.FILE_PATH_FIELD_DIRECTORY, allow_folders=True)
    style= models.CharField(max_length=1, choices=STYLE_LIST,)
    color = models.CharField(max_length=16, choices=COLOR_LIST)
    season = models.CharField(max_length=16, choices=SEASON_LIST)
    temperature = models.CharField(max_length=16, choices=TEMPERATURE_LIST)
    sky = models.CharField(max_length=8, choices=SKY_LIST)
    last_date = models.DateField(blank=True)
    likes = model.ForeignKey(Like, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'Items'





class Like(models.Model):
    user = model.ForeignKey(User, on_delete=models.CASCADE)
    style= models.CharField(max_length=1, choices=STYLE_LIST,)
    class Meta:
        db_table = 'Look_like'

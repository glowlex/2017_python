from django.contrib import admin

# Register your models here.
from pestyle.models import *

admin.site.register(User)
admin.site.register(Item)
admin.site.register(Look)
admin.site.register(Event)

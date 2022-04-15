from django.contrib import admin

# Register your models here.
from .models import User, Protector, Student

admin.site.register(User)
admin.site.register(Protector)
admin.site.register(Student)
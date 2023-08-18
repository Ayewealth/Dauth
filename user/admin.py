from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(InstructorProfile)
admin.site.register(StudentProfile)
admin.site.register(Course)

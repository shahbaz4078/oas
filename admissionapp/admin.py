from django.contrib import admin
from .models import Enquiry
from .models import Student
from.models import Courses


# Register your models here.
admin.site.register(Enquiry)
admin.site.register(Student)
admin.site.register(Courses)
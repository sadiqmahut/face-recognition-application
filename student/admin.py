from django.contrib import admin
from .models import Division, Department, Student, TempFileTest, Classrooms
# Register your models here.


admin.site.register(Division)
admin.site.register(Department)
admin.site.register(Student)
admin.site.register(TempFileTest)
admin.site.register(Classrooms)

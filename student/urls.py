from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_home,name='studentregister'),
    path('loginrequired/', views.login_mandatory,name='loginrequired'),
    path('classrooms/', views.classromm_list,name='classrooms'),
    path('classrooms/success/', views.success_page,name='success'),
    path('registerclass/', views.register_class,name='registerclass'),
    path('test_video/<str:dept>/<str:div>', views.test_page,name='test_vidfeed'),
    path('vidfeed/<str:dept>/<str:div>/', views.vidfeed,name='vidfeed'),
]
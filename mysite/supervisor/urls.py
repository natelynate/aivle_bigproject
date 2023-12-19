from django.urls import path
from supervisor import views
# from django.views.generic import ListView
from django.http import HttpResponse

app_name = 'supervisor'

urlpatterns = [
    path('', lambda resp: HttpResponse('기획자를 위한 메인 페이지입니다')),
    path('testpage/', views.testpage),
    
]

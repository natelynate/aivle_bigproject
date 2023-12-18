from django.urls import path
from subject import views
# from django.views.generic import ListView
from django.http import HttpResponse

app_name = 'subject'

urlpatterns = [
    path('', lambda resp: HttpResponse('테스트 참여자를 위한 메인 페이지입니다')),
    path('testpage/', views.testpage),
    
]

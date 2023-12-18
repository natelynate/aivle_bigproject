from django.urls import path
from subject import views

app_name = 'subject'

urlpatterns = [
    path('testpage/', views.testpage),
    
]

from django.urls import path
from supervisor import views

app_name = 'supervisor'

urlpatterns = [
    path('testpage/', views.testpage),
    
]

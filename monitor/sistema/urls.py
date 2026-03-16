from django.urls import path

from .views import dashboard

app_name = 'sistema'

urlpatterns = [
    path('', dashboard, name='dashboard'),
]

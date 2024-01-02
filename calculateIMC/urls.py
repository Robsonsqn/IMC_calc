from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('process_data/', views.process_data, name='process_data'),
    path('enviar_email/', views.enviar_email, name='enviar_email'),
]

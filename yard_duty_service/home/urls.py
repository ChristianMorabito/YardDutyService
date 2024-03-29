from django.urls import path
from . import views


urlpatterns = [
	path('', views.home, name='main-home'),
	path('about/', views.about, name='main-about'),
	path('update_duty/', views.update_duty, name='update_duty'),
	path('load_json/', views.load_json, name='load_json'),
	path('get_username/', views.get_username, name='get_username'),
]
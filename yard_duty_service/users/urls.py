from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
	path('', views.home, name='users-home'),
	path('login/', auth_views.LoginView.as_view(template_name='users/login.html',
	                                            redirect_authenticated_user=True), name='users-login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='users-logout')
]
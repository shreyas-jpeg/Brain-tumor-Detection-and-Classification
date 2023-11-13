from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url

urlpatterns = [
    path('accounts/login', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('accounts/confirmation', views.confirmation, name='confirmation'),
    path('accounts/logout', auth_views.LogoutView.as_view(next_page="login"), name='logout'),
    path('accounts/signup', views.signup, name='signup'),
    #path('accounts/account_activation_sent', views.account_activation_sent, name='account_activation_sent'),
    #url(r'^accounts/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #    views.activate, name='activate'),
]
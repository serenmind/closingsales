from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from .views import SignupView
from .views import UserNameAvailableView
from .views import ActionActivationSentView
from .views import ActivateAccount
from .views import AccountActivationInvalidView
from .views import ChangePasswordView
from .views import ProfileView

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='signin', permanent=False)),
    url(r'^usernameavailable/$', UserNameAvailableView.as_view(), name='usernameavailable'),
    url(r'^activationsent/$', ActionActivationSentView.as_view(), name='account_activation_sent'),
    url(r'^accountinvalid/$', AccountActivationInvalidView.as_view(), name='account-activation-invalid'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', ActivateAccount.as_view(), name='account_activate'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='signin'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^password/$', ChangePasswordView.as_view(), name='change_password'),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
]

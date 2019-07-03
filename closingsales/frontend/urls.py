from django.urls import path
from django.urls import re_path

from .views import HomepageView
from .views import ContactView
from .views import AboutView
from .views import ClassifiedsDetailView
from .views import ClassifiedsView
from .views import PrivacyplicyView

urlpatterns = [
    path('', HomepageView.as_view(), name='home'),
    re_path(r'^classifieds/(?P<pk>[0-9]+)/$', ClassifiedsDetailView.as_view(), name='classified-detail'),
    path('classifieds', ClassifiedsView.as_view(), name='classifieds'),
    path('about-us', AboutView.as_view(), name='about'),
    # path('contact', ContactView.as_view(), name='contact'),
    path('privacy', PrivacyplicyView.as_view(), name='privacy'),
    path('contact-us', ContactView.as_view(), name='contact'),
]

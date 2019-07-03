from django.conf.urls import url
from .views import DashboardView
from .views import CategoryListView
from .views import SubCategoryListView
from .views import AdvertisementListView


from .views import AdvertisementCreateView
from .views import AdvertisementDetailView
from .views import AdvertisementUpdateView
from .views import AdvertisementDeleteView


# handeling upload image
from .views import UploadImageView


urlpatterns = [
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'^categories/$', CategoryListView.as_view(), name='categories-list'),
    url(r'^subcategories/$', SubCategoryListView.as_view(), name='subcategories-list'),
    url(r'^advertisements/$', AdvertisementListView.as_view(), name='advertisements-list'),
    url(r'^advertisements/(?P<pk>\d+)/$', AdvertisementDetailView.as_view(), name='ad-detail'),
    url(r'^advertisements/(?P<pk>\d+)/edit/$', AdvertisementUpdateView.as_view(), name='ad-edit'),
    url(r'^advertisements/(?P<pk>\d+)/delete/$', AdvertisementDeleteView.as_view(), name='ad-delete'),
    url(r'^advertisements/(?P<pk>\d+)/upload/$', UploadImageView.as_view(), name='uploadimage'),
    url(r'^advertisements/new$', AdvertisementCreateView.as_view(), name='advertisement-new'),
]

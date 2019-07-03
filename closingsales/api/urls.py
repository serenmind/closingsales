from django.conf.urls import url
from django.urls import include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

from api.views import CategoryViewSet
from api.views import SubcategoryViewSet
from api.views import AdvertisementViewSet
from api.views import CountryViewSet
from api.views import AdImageViewSet
from api.views import latest_ads

router = routers.DefaultRouter()

router.register(r'categories', CategoryViewSet, base_name='categories')
router.register(r'subcategories', SubcategoryViewSet, base_name='subcategories')
router.register(r'classifides', AdvertisementViewSet, base_name='classifides')
router.register(r'countries', CountryViewSet, base_name='countries')
router.register(r'adimages', AdImageViewSet, base_name='adimages')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^latest_ads/$', latest_ads),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

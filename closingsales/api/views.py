from rest_framework import viewsets
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from products.models import Category
from products.models import Subcategory
from products.models import Advertisement
from products.models import AdImage
from address.models import Country

from api.serializers import CategorySerailizer
from api.serializers import SubcategorySerializer
from api.serializers import AdvertisementSerializer
from api.serializers import CountrySerializer
from api.serializers import AdImageSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerailizer

    @action(methods=['get'], detail=True)
    def subcategories(self, request, pk=None):
        if pk is None:
            return Response({'results': []}, status=status.HTTP_200_OK)

        subcategories = Subcategory.objects.filter(category=pk)
        serializer = SubcategorySerializer(subcategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return self.queryset
        return self.queryset.filter(user=user)

    @action(methods=['post'], detail=True)
    def status(self, request, pk):
        try:
            advertisement = Advertisement.objects.get(pk=pk)
            advertisement.status = self.request.POST.get('status')
            advertisement.save()
            serializer = self.serializer_class(advertisement)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Advertisement.DoesNotExist:
            return Respone({'error': 'cannot update'}, staus=HTTP_404_NOT_FOUND)


class CountryViewSet(viewsets.ModelViewSet):
    queryset         = Country.objects.all()
    serializer_class = CountrySerializer


class AdImageViewSet(viewsets.ModelViewSet):
    queryset         = AdImage.objects.all()
    serializer_class = AdImageSerializer

@api_view(['GET'])
@permission_classes((AllowAny, ))
def latest_ads(request, format=None):
    all_ads = Advertisement.objects.latest_ads()
    serializer = AdvertisementSerializer(all_ads, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


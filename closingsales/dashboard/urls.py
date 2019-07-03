from django.urls import path
from .views import DashboardIndexView

urlpatterns = [
        path('', DashboardIndexView, name='dashboard-index'),
        ]

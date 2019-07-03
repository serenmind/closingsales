from django.shortcuts import render

# Create your views here.
def DashboardIndexView(request):
    return render(request, 'dashboard/index.html')


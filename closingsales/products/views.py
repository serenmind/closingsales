from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

from .utils import process_ad_form
from .models import Category, Subcategory, Advertisement
from .models import AdImage
from .forms import AdImageForm

from address.models import Country


class DashboardView(TemplateView):
    template_name = 'products/index.html'


class CategoryListView(ListView):
    model = Category


class SubCategoryListView(ListView):
    model = Subcategory


class AdvertisementListView(ListView):
    template_name       = 'products/advertisements.html'
    model               = Advertisement
    context_object_name = 'advertisements'
    paginate_by         = 10

    def get_context_data(self, **kwargs):
        ctx             = super().get_context_data(**kwargs)
        search          = self.request.GET.get('search', '')
        ctx['search']   = search
        return ctx

    def get_queryset(self):
        user        = self.request.user
        search      = self.request.GET.get('search', '')
        type        = self.request.GET.get('type')
        query       = Q(description__icontains=search) | Q(title__icontains=search)
        query_set   = Advertisement.objects.exclude(status=Advertisement.ARCHIVED).order_by('-updated_at').distinct()
        """
        order = ['yes', 'no', 'not_sure']
        return sorted(qs, key=lambda x: order.index(x.status))

        ## Using raw query and it is good for performance
        qs = self.model._default_manager.get_queryset()
        newquery = qs.query+' ORDER BY idx(array'+order.__str__()+', status)'
        return self.model._default_manager.raw(newquery)
        """
        if user.is_superuser:
            return query_set.filter(query)
        return query_set.filter(query).filter(user=user)


class AdvertisementCreateView(CreateView):
    template_name   = 'products/advertisement_new.html'
    model           = Advertisement
    fields          = ['subcategory','title', 'description', 'start_date',
                        'state', 'zipcode', 'address', 'address1', 'longitude', 'latitude']

    def get_context_data(self, **kwargs):
        ctx                 = super().get_context_data(**kwargs)
        categories          = Category.objects.all()
        # TODO support other  countries also
        # Currently supports only Germany
        germany             = Country.objects.filter(name='Germany').first()
        states              = germany.states.all()
        ctx['states']       = states
        ctx['categories']   = categories
        return ctx

    # this assumes that all the validation is done in frontend.
    # TODO: handle with custom forms
    def post(self, request):
        user        = request.user
        form_data   = process_ad_form(request)
        advertisement = Advertisement.objects.create(
            user=user,
            subcategory=Subcategory.objects.get(pk=form_data['subcategory']),
            title=form_data['title'],
            description=form_data['description'],
            start_date=form_data['start_date'],
            end_date=form_data['end_date'],
            state=form_data['state'],
            zipcode=form_data['zipcode'],
            address=form_data['address'],
            open_at=form_data['open_at'],
            closed_at=form_data['closed_at'],
            address1=form_data['address1'],
            longitude=form_data['longitude'],
            latitude=form_data['latitude']
        )
        advertisement.save()
        return redirect('uploadimage', pk=advertisement.id)


class AdvertisementDetailView(DetailView):
    template_name   = 'products/advertisement_detail.html'
    model           = Advertisement


class AdvertisementUpdateView(UpdateView):
    template_name   = 'products/advertisement_update.html'
    model           = Advertisement
    fields          = ['title', 'description', 'start_date',
                        'state', 'zipcode', 'address', 'address1', 'longitude',
                        'latitude']

    def get_context_data(self, **kwargs):
        ctx                  = super().get_context_data(**kwargs)
        categories           = Category.objects.all()
        subcategory          = self.object.subcategory
        category             = subcategory.category
        images               = self.object.images.all()
        states               = Country.objects.filter(name='Germany').first().states.all()
        ctx['subcategory']   = subcategory
        ctx['category']      = category
        ctx['categories']    = categories
        ctx['images']        = images
        ctx['advertisement'] = self.object
        ctx['states']        = states

        return ctx

    def post(self, request, *args, **kwargs):
        form_data = process_ad_form(request)

        advertisement               = get_object_or_404(Advertisement, pk=kwargs.get('pk'))
        advertisement.subcategory   = Subcategory.objects.get(pk=form_data['subcategory'])
        advertisement.title         = form_data['title']
        advertisement.description   = form_data['description']
        advertisement.start_date    = form_data['start_date']
        advertisement.end_date      = form_data['end_date']
        advertisement.state         = form_data['state']
        advertisement.zipcode       = form_data['zipcode']
        advertisement.address       = form_data['address']
        advertisement.address1      = form_data['address1']
        advertisement.longitude     = form_data['longitude']
        advertisement.latitude      = form_data['latitude']
        advertisement.open_at       = form_data['open_at']
        advertisement.closed_at     = form_data['closed_at']
        advertisement.save()
        return redirect('uploadimage', pk=advertisement.id)


class AdvertisementDeleteView(DeleteView):
    template_name   = 'products/advertisement_delete.html'
    model           = Advertisement
    success_url     = reverse_lazy('advertisements-list')

    def delete(self, *args, **kwargs):
        advertisement           = get_object_or_404(
                                    self.model, pk=kwargs.get('pk')
                                )
        advertisement.status    = self.model.ARCHIVED
        advertisement.save()
        return redirect(self.success_url)

class UploadImageView(View):

    def get(self, request, pk):
        advertisement = get_object_or_404(Advertisement, pk=pk)
        images = AdImage.objects.filter(advertisement=advertisement)
        return render(self.request, 'products/uploadimage.html', {'images': images, 'advertisement': advertisement})

    def post(self, request, pk):
        advertisement = get_object_or_404(Advertisement, pk=pk)
        form = AdImageForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            ad_img = form.save(commit=False)
            ad_img.advertisement = advertisement
            ad_img.save()
            data = {'is_valid': True, 'name': ad_img.file.name, 'url': ad_img.file.url, 'id': ad_img.id }
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
    
    def delete(self, request, pk):
        try:
            ad_image = AdImage.objects.get(pk=pk)
            ad_image.delete()
            return JsonResponse({'sucess': True, 'message': 'Image delted sucessfully'})
        except AdImage.DoesNotExist:
            return JsonResponse({'sucess': False, 'error': True, 'message': 'Requested Image is not found'})


from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.views.generic import View
from django.views.generic import ListView
from products.models import Advertisement, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


class HomepageView(TemplateView):
    template_name = 'frontend/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        all_ads = Advertisement.objects.latest_ads()
        categories = Category.objects.all()
        map_infos = []
        for ad in all_ads:
            gmap = {}
            gmap['lat'] = ad.latitude
            gmap['lng'] = ad.longitude
            map_infos.append(gmap)
        ctx['maps'] = map_infos
        ctx['latest_ads'] = all_ads[:4]
        ctx['categories'] = categories
        return ctx


class ContactView(TemplateView):
    template_name = 'frontend/contact.html'

    def post(self, request, *args, **kwargs):
        subject = 'New Message from closingshops.de'
        message = render_to_string('frontend/email.html', {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'message': request.POST.get('message')
        })
        customer_email = request.POST.get('email')
        send_mail(subject, message, customer_email, ['contact@closingshops.de'])
        context = {
            'message': 'Thankyou for contacting us. We will get back to you soon.'
        }
        return render(request, self.template_name, context)

class AboutView(TemplateView):
    template_name = 'frontend/aboutus.html'


class ClassifiedsDetailView(TemplateView):
    template_name = 'frontend/advertisement.html'

    def get(self, request, pk, **kwargs):
        advertisement = get_object_or_404(Advertisement, pk=pk)
        owner = advertisement.user
        images = advertisement.images.all()
        context = {
            'advertisement': advertisement,
            'images': images,
            'owner': owner,
            **kwargs
        }

        if advertisement.status != 'APPROVED':
            if self.request.user != owner and not self.request.user.is_superuser:
                raise Http404

        return render(request, self.template_name, context)


class ClassifiedsView(TemplateView):
    template_name = 'frontend/classifieds.html'
    paginate_by = 10

    def get(self, request, **kwargs):
        category        = self.request.GET.get('category', '')
        location        = self.request.GET.get('location', '')
        keyword         = self.request.GET.get('keyword', '')
        page            = self.request.GET.get('page', 1)

        advertise_list  = Advertisement.objects.latest_ads().filter(Q(description__icontains=keyword) | Q(title__icontains=keyword),
                                subcategory__category__name__icontains=category,
                                address__icontains=location)
        # advertise_list  = Advertisement.objects.latest_ads().filter (title__icontains=keyword,
        #                         subcategory__category__name__icontains=category,
        #                         address__icontains=location)

        paginator = Paginator(advertise_list, self.paginate_by)
        try:
            advertisements = paginator.page(page)
        except PageNotAnInteger:
            advertisements = paginator.page(1)

        except EmptyPage:
            advertisements = paginator.page(paginator.num_pages)

        # against the functional programming principle
        if category:
            category = Category.objects.filter(name=category).first()

        categories  = Category.objects.all()
        ctx = {**kwargs}
        ctx['advertisements'] = advertisements
        ctx['category'] = category
        ctx['location'] = location
        ctx['keyword']  = keyword
        ctx['categories'] = categories

        return render(request, self.template_name, ctx)


class PrivacyplicyView(TemplateView):
    template_name = 'frontend/policy.html'


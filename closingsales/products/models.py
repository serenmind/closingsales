import datetime
from django.db.models import Count
from django.utils.text import slugify
from django.db.models import Q
from django.db import models
from django.urls import reverse
from account.models import User


class TimeStampedModel(models.Model):
    """
    An Abstract base class model that proides self-updating
    `created_at` and `modified_at` fields.
    """
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CategoryManager(models.Manager):

    def top_subcateories(self):
        query = super().get_queryset()
        # Category.objects.all().prefetch_related('subcategories')
        # Subcategory.objects.annotate(num_ad=Count('advertisement'))

        # Category.objects.all().prefetch_related('subcategories').annotate(num_ad=Count('advertisement'))
        return query
        

class Category(TimeStampedModel):
    name        = models.CharField(max_length=200, unique=True)
    image       = models.ImageField(upload_to='categories', null=True, blank=True)
    fa_icon     = models.CharField(max_length=100, blank=True, null=True, default='')
    slug        = models.SlugField()

    objects     = CategoryManager()

    def save(self, *arg, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super().save(*arg, **kwargs)

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class SubcategoryManager(models.Manager):

    def advertisement_count(self, pk):
        subcategory = Subcategory.objects.get(pk=pk).annotate(num=Count('advertisement'))


class Subcategory(TimeStampedModel):
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='subcategories', related_query_name='subcategory')
    name        = models.CharField(max_length=200, unique=True)
    image       = models.ImageField(upload_to='subcategories', null=True, blank=True)
    slug        = models.SlugField()

    def save(self, *arg, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super().save(*arg, **kwargs)

    def get_absolute_url(self):
        return reverse('subcategory-detail', kwargs={'pk': self.pk})

    @property
    def total_ads(self):
        # TODO: this query method may be bad in near future
        count = len([ad for ad in self.advertisements.all() if ad.is_active])
        return count

    def __str__(self):
        return self.name


class AdvertisementManager(models.Manager):

    def latest_ads(self):
        return super().get_queryset().filter(
                Q(status= Advertisement.APPROVED)
                & Q(start_date__lte=datetime.date.today())
                & Q(end_date__gte=datetime.date.today())
            ).order_by('-created_at')

    def latest_ads_with_images(self):
        query_set = self.latest_ads()
        # TODO: the following query may not be good

        adversiments = []
        for ad in query_set:
            images = ad.images
            if images.count():
                ad['url'] = images.first().file.url
            else:
                ad['url'] = ''
            adversiments.append(ad)
        return adversiments


class Advertisement(TimeStampedModel):
    APPROVED    = 'APPROVED'
    PENDING     = 'PENDING'
    DENIED      = 'DENIED'
    ARCHIVED    = 'ARCHIVED'
    OPTIONS     = (
        (APPROVED, 'APPROVED'),
        (PENDING, 'PENDING'),
        (DENIED, 'DENIED'),
        (ARCHIVED, 'ARCHIVED')
        )
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='advertisements', related_query_name='advertisement')
    user        = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title       = models.CharField(max_length=255)
    description = models.TextField()
    status      = models.CharField(max_length=8, choices=OPTIONS, default=PENDING)
    start_date  = models.DateField()
    end_date    = models.DateField()
    open_at     = models.TimeField(null=True, blank=True)
    closed_at   = models.TimeField(null=True, blank=True)
    state       = models.CharField(max_length=300)
    zipcode     = models.CharField(max_length=10)
    address     = models.CharField(max_length=100)
    address1    = models.CharField(max_length=100, null=True, default='', blank=True)
    longitude   = models.CharField(max_length=50, null=True, default='')
    latitude    = models.CharField(max_length=50, null=True, default='')

    objects     = AdvertisementManager()


    class Meta:
        get_latest_by = 'created_at'

    def get_absolute_url(self):
        return reverse('advertisement-detail', kwargs={'pk': self.pk })

    @property
    def is_active(self):
        today = datetime.date.today()
        return self.status == Advertisement.APPROVED and self.start_date <= today and self.end_date >= today

    def __str__(self):
        return self.title



class AdImage(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='images', blank=True, null=True)
    file = models.ImageField(upload_to='classifieds')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.advertisement.title

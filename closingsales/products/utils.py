import moment
import time

def parse_time(str_time):
    strt = time.strptime(str_time, '%I:%M %p')
    return time.strftime('%H:%M', strt)

def process_ad_form(request):
    subcategory     = request.POST.get('subcategory')
    title           = request.POST.get('title')
    description     = request.POST.get('description')
    date_range      = request.POST.get('start_date')
    date_range      = date_range.split('-')
    opening_hour    = parse_time(request.POST.get('opening_hour'))
    closing_hour    = parse_time(request.POST.get('closing_hour'))

    start_date      = moment.date(date_range[0]).date
    end_date        = moment.date(date_range[1]).date
    state           = request.POST.get('state')
    zipcode         = request.POST.get('zipcode')
    address         = request.POST.get('address')
    address1        = request.POST.get('address1')
    longitude       = request.POST.get('longitude')
    latitude        = request.POST.get('latitude')

    return {
        'subcategory': subcategory,
        'title': title,
        'description': description,
        'start_date': start_date,
        'end_date': end_date,
        'state': state,
        'zipcode': zipcode,
        'address': address,
        'address1': address1,
        'open_at': opening_hour,
        'closed_at': closing_hour,
        'longitude': longitude,
        'latitude': latitude
    }
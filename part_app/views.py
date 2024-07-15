import json

from django.db.models import Sum
from django.http import JsonResponse
from django.core.serializers import serialize
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .forms import SearchForm


# Create your views here.


def mark_view(request):
    qs = Mark.objects.all()
    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    json_data = serialize('json', page_obj)
    return JsonResponse({'data': json_data,
                         'page': page_obj.number}, content_type='application/json', safe=False)


def model_view(request):
    qs = Model.objects.all()
    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    json_data = serialize('json', page_obj)
    return JsonResponse({'data': json_data,
                         'page': page_obj.number}, content_type='application/json', safe=False)


@csrf_exempt
def search_part_view(request):
    if request.method == 'POST':
        json_request = dict(request.POST)
        if json_request.get('mark_name') not in [None, '']:
            qs = Part.objects.filter(name__contains=json_request.get('part_name')[0],
                                     mark_id__name__contains=json_request.get('mark_name')[0],
                                     price__gte=float(json_request.get('price_gte')[0]),
                                     price__lte=float(json_request.get('price_lte')[0]),
                                     json_data__contains=json.loads(json_request.get('params')[0]))
        elif json_request.get('mark_list') not in [None, '']:
            qs = Part.objects.filter(name__contains=json_request.get('part_name')[0],
                                     mark_id__in=eval(json_request.get('mark_list')[0]),
                                     price__gte=float(json_request.get('price_gte')[0]),
                                     price__lte=float(json_request.get('price_lte')[0]),
                                     json_data__contains=json.loads(json_request.get('params')[0]))
        print(qs)
        paginator = Paginator(qs, 10)
        page_number = request.GET.get('page') or request.POST.get('page')
        page_obj = paginator.get_page(page_number)
        json_data = serialize('json', page_obj)
        return JsonResponse({'response': json_data,
                             'count': paginator.count,
                             'summ': qs.aggregate(Sum('price')),
                             'page': page_obj.number}, content_type='application/json', safe=False)

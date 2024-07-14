
from django.http import JsonResponse
from django.core.serializers import serialize
from django.core.paginator import Paginator
from .models import *
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


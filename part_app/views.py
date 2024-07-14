
from django.http import JsonResponse
from django.core.serializers import serialize
from .models import *
# Create your views here.


def mark_view(request):
    qs = Mark.objects.all()
    jsom_data = serialize('json', qs)
    return JsonResponse(jsom_data, content_type='application/json', safe=False)


def model_view(request):
    qs = Model.objects.all()
    jsom_data = serialize('json', qs)
    return JsonResponse(jsom_data, content_type='application/json', safe=False)


from django.shortcuts import render
from django.db.models.aggregates import Sum, Min, Max, Avg, Count
from django.http import HttpResponse
from django.db.models import Q, F
from store.models import Product, Customer, Collection, Order, OrderItem
# Create your views here.


def say_hello(request):

    result = Product.objects.filter(collection__id=3) \
        .aggregate(max=Max('unit_price'),
                   min=Min('unit_price'), avg=Avg('unit_price'))
    return render(request, 'hello.html', {'name': 'Mohamed Montaser', 'result': result})

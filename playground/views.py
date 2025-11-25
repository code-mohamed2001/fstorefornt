from django.shortcuts import render
from django.db.models.aggregates import Sum, Min, Max, Avg, Count
from django.http import HttpResponse
from django.db import transaction
from django.db.models import Q, F
from store.models import Product, Customer, Collection, Order, OrderItem, CartItem, Cart
# Create your views here.


@transaction.atomic()
def say_hello(request):

    return render(request, 'hello.html', {'name': 'Mohamed Montaser'})

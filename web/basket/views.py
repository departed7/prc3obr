from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Concert
from .basket import Basket

def concert_list(request):
    concerts = Concert.objects.all()
    return render(request, 'basket/concert_list.html', {'concerts': concerts})

@require_POST
def basket_add(request, concert_id):
    basket = Basket(request)
    concert = get_object_or_404(Concert, id=concert_id)
    basket.add(concert=concert)
    return redirect('basket:basket_detail')

def basket_remove(request, concert_id):
    basket = Basket(request)
    concert = get_object_or_404(Concert, id=concert_id)
    basket.remove(concert)
    return redirect('basket:basket_detail')

def basket_detail(request):
    basket = Basket(request)
    return render(request, 'basket/basket_detail.html', {'basket': basket})

@login_required
def basket_checkout(request):
    basket = Basket(request)
    # Очистка после "покупки"
    basket.clear()
    return render(request, 'basket/success.html')
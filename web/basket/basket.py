from decimal import Decimal
from django.conf import settings
from .models import Concert

class Basket:
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if not basket:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, concert, count=1, update_count=False):
        concert_id = str(concert.id)
        if concert_id not in self.basket:
            self.basket[concert_id] = {'count': 0, 'price': str(concert.price)}
        if update_count:
            self.basket[concert_id]['count'] = count
        else:
            self.basket[concert_id]['count'] += count
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, concert):
        concert_id = str(concert.id)
        if concert_id in self.basket:
            del self.basket[concert_id]
            self.save()

    def __iter__(self):
        concert_ids = self.basket.keys()
        concerts = Concert.objects.filter(id__in=concert_ids)
        basket = self.basket.copy()
        for concert in concerts:
            basket[str(concert.id)]['concert'] = concert
        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['count']
            yield item

    def __len__(self):
        return sum(item['count'] for item in self.basket.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['count'] for item in self.basket.values())

    def clear(self):
        del self.session[settings.BASKET_SESSION_ID]
        self.save()
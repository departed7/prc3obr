from django.db import models

# Create your models here.
from django.db import models

class Concert(models.Model):
    artist = models.CharField(max_length=255, verbose_name='Артист')
    title = models.CharField(max_length=255, verbose_name='Название тура')
    poster = models.ImageField(upload_to='posters/', verbose_name='Афиша')
    date = models.DateTimeField(verbose_name='Дата и время')
    city = models.CharField(max_length=100, verbose_name='Город')
    venue = models.CharField(max_length=255, verbose_name='Площадка')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена от')

    def __str__(self): return f'{self.artist} в {self.city}'

    class Meta:
        verbose_name = 'Концерт'
        verbose_name_plural = 'Афиша концертов'
from django.db import models
from django.urls import reverse

# Create your models here.

class List(models.Model):
    text = models.TextField(default='')

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    text = models.TextField(default='')
    saving_list = models.ForeignKey(List,
            default=None,
            on_delete=models.CASCADE,
        )

    class Meta:
        ordering = ('id', )
        unique_together = ('saving_list', 'text')

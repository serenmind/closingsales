from django.db import models


class Country(models.Model):
    name            = models.CharField(unique=True, max_length=100)
    currency        = models.CharField(max_length=2)
    language        = models.CharField(max_length=50)
    language_symbol = models.CharField(max_length=5)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Countries'

class State(models.Model):
    country         = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states')
    name            = models.CharField(unique=True, max_length=100)
    state_number    = models.IntegerField()

    def __str__(self):
        return self.name

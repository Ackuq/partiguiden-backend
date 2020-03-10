from django.db import models


class Party(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=50, verbose_name="Partinamn")
    abbreviation = models.CharField(max_length=10, verbose_name="Partiförkortning")

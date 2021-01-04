from django.db import models
from django.contrib.postgres.fields import ArrayField


class Party(models.Model):
    def __str__(self):
        return self.name

    abbreviation = models.CharField(max_length=10, verbose_name="Partiförkortning", unique=True, primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Partinamn", unique=True)


class Subject(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=50, verbose_name="Sakområde", unique=True)
    related_subject = models.ManyToManyField("self", verbose_name="Relaterade sakområden", blank=True)


class Standpoint(models.Model):
    def __str__(self):
        return f"{self.title} - {self.party}"

    id = models.CharField(max_length=64, primary_key=True)
    link = models.CharField(max_length=100, verbose_name="Länk", unique=True)
    title = models.CharField(max_length=50, verbose_name="Ståndpunkt", default="Titel")
    content = ArrayField(models.CharField(max_length=200), verbose_name="Åsikt")
    date = models.DateField(verbose_name="datum", null=True, auto_now_add=True)
    party = models.ForeignKey(Party, on_delete=models.CASCADE, verbose_name="Parti")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Sakområde", null=True, blank=True)

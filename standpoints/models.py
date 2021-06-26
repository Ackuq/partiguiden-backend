from django.contrib.postgres.fields import ArrayField
from django.db import models

from .constants import DB_COLLATION


class Party(models.Model):
    def __str__(self):
        return self.name

    id = models.CharField(max_length=10, verbose_name="Partiförkortning", primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Partinamn", unique=True, db_collation=DB_COLLATION)

    class Meta:
        ordering = ["name"]


class Subject(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=50, verbose_name="Sakområde", unique=True, db_collation=DB_COLLATION)
    related_subjects = models.ManyToManyField("self", verbose_name="Relaterade sakområden", blank=True)

    class Meta:
        ordering = ["name"]


class Standpoint(models.Model):
    def __str__(self):
        return f"{self.title} - {self.party}"

    id = models.CharField(max_length=64, primary_key=True)
    link = models.CharField(max_length=150, verbose_name="Länk", unique=True)
    title = models.CharField(max_length=100, verbose_name="Ståndpunkt", default="Titel", db_collation=DB_COLLATION)
    content = ArrayField(models.CharField(max_length=1000), verbose_name="Åsikt")
    date = models.DateField(verbose_name="datum", null=True, auto_now_add=True)
    party = models.ForeignKey(Party, on_delete=models.CASCADE, verbose_name="Parti")
    subject = models.ForeignKey(
        Subject, on_delete=models.SET_NULL, verbose_name="Sakområde", null=True, blank=True, related_name="standpoints"
    )

    class Meta:
        ordering = ["party", "title"]

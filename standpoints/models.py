# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Party(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=50, verbose_name="Partinamn")
    abbreviation = models.CharField(max_length=10, verbose_name="Partiförkortning")


class Subject(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=50, verbose_name="Sakområde")
    date = models.DateField(verbose_name="datum", null=True, auto_now_add=True)
    related_subject = models.ManyToManyField("self", verbose_name="Relaterade sakområden", blank=True)


class Standpoint(models.Model):
    def __str__(self):
        return f"{self.title} - {self.party}"

    title = models.CharField(max_length=50, verbose_name="Ståndpunkt", default="Titel")
    content = models.TextField(verbose_name="Åsikt")
    party = models.ForeignKey(Party, on_delete=models.CASCADE, verbose_name="Parti", null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, verbose_name="Sakområde", null=True, blank=True)


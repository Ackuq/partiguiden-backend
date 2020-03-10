from django.db import models


class Subject(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=50, verbose_name="Sakområde")
    related_subject = models.ManyToManyField("self", verbose_name="Relaterade sakområden", blank=True)

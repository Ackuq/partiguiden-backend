from django.db import models

from ...models import Party, Subject


class Standpoint(models.Model):
    def __str__(self):
        return f"{self.title} - {self.party}"

    title = models.CharField(max_length=50, verbose_name="Ståndpunkt", default="Titel")
    content = models.TextField(verbose_name="Åsikt")
    date = models.DateField(verbose_name="datum", null=True, auto_now_add=True)
    link = models.CharField(max_length=100, verbose_name="Länk", blank=True, unique=True)
    party = models.ForeignKey(Party, on_delete=models.CASCADE, verbose_name="Parti", null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, verbose_name="Sakområde", null=True, blank=True)


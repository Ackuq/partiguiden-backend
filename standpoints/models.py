from django.db import models


class Party(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=50, verbose_name="Partinamn")
    abbreviation = models.CharField(max_length=10, verbose_name="Partiförkortning")


class Subject(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=50, verbose_name="Sakområde")
    related_subject = models.ManyToManyField("self", verbose_name="Relaterade sakområden", blank=True)


def get_default_subject():
    return Subject.objects.get_or_create(name="Default", related_subject=[])


class Standpoint(models.Model):
    def __str__(self):
        return f"{self.title} - {self.party}"

    title = models.CharField(max_length=50, verbose_name="Ståndpunkt", default="Titel")
    content = models.TextField(verbose_name="Åsikt")
    date = models.DateField(verbose_name="datum", null=True, auto_now_add=True)
    link = models.CharField(max_length=100, verbose_name="Länk", unique=True)
    party = models.ForeignKey(Party, on_delete=models.CASCADE, verbose_name="Parti")
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, verbose_name="Sakområde", default=get_default_subject
    )

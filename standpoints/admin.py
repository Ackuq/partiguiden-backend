# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Party, Subject, Standpoint

# Parties
admin.site.register(Party)

# Subjects
admin.site.register(Subject)

# Standpoints
admin.site.register(Standpoint)


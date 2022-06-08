# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models

class TBA(models.Model):
    words = models.CharField(max_length=150)

    def __str__(self):
        return self.name

# -*- coding: utf8 -*-
from django.db import models

class AppliedMigration(models.Model):
    """Model that holds information about applied migrations"""
    classname = models.CharField(max_length=100)
    migrated_at = models.DateTimeField(auto_now_add=True)

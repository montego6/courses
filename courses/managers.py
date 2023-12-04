from django.db import models
from django.db.models import Q

class CourseManager(models.Manager):
    def search_by_query(self, query):
        return self.filter(Q(name__icontains=query) | Q(short_description__icontains=query) | Q(full_description__icontains=query))
from django.db import models
from django.db.models import Q, Avg, OuterRef, Subquery

import courses.models as cmodels
from core import consts
from reviews.models import Review


class CourseManager(models.Manager):
    def search_by_query(self, query):
        return self.filter(Q(name__icontains=query) | Q(short_description__icontains=query) | Q(full_description__icontains=query))
    
    def by_subcategory(self, subcategory_id):
        price = cmodels.CoursePrice.objects.filter(course=OuterRef('id'), option=consts.COURSE_OPTION_BASIC).values('amount')
        rating = Review.objects.filter(course=OuterRef('id')).\
            annotate(avg_rating=models.Func(models.F('rating'), function='AVG', output_field=models.DecimalField())).values('avg_rating')
        return self.filter(subject__parent_subcategory__id=subcategory_id).select_related('subject').select_related('author').prefetch_related('students').annotate(price=Subquery(price), 
                                                                                                              rating=Subquery(rating))
    


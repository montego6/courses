from django.db import models
from django.db.models import Q, Avg, OuterRef, Subquery

import courses.models as cmodels
from core import consts
from reviews.models import Review


class CourseManager(models.Manager):
    def search_by_query(self, query):
        price = cmodels.CoursePrice.objects.filter(course=OuterRef('id'), option=consts.COURSE_OPTION_BASIC).values('amount')
        rating = Review.objects.filter(course=OuterRef('id')).\
            annotate(avg_rating=models.Func(models.F('rating'), function='AVG', output_field=models.DecimalField())).values('avg_rating')
        return self.filter(Q(name__icontains=query) | Q(short_description__icontains=query) | Q(full_description__icontains=query)).select_related('subject').select_related('author').prefetch_related('students').annotate(price=Subquery(price), 
                                                                                                              rating=Subquery(rating))
    
    def by(self, **kwargs):
        price = cmodels.CoursePrice.objects.filter(course=OuterRef('id'), option=consts.COURSE_OPTION_BASIC).values('amount')
        rating = Review.objects.filter(course=OuterRef('id')).\
            annotate(avg_rating=models.Func(models.F('rating'), function='AVG', output_field=models.DecimalField())).values('avg_rating')
        return self.filter(**kwargs).select_related('subject').select_related('author').prefetch_related('students').annotate(price=Subquery(price), 
                                                                                                              rating=Subquery(rating))
    
    def by_subcategory(self, subcategory_id):
        return self.by(subject__parent_subcategory__id=subcategory_id)
    
    def by_subject(self, subject_id):
        return self.by(subject_id=subject_id)

    def by_category(self, category_id):
        return self.by(subject__parent_subcategory__parent_category=category_id)
    


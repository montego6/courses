from django.db import models
from django.db.models import Q

from categories.utils import get_current_month, get_current_year
import courses.models as cmodels
import reviews.models as rmodels

class CourseManager(models.Manager):
    def search_by_query(self, query):
        return self.filter(Q(name__icontains=query) | Q(short_description__icontains=query) | Q(full_description__icontains=query))
    

class CourseStatisticsManager(models.Manager):
    def by_subject(self, subject_id):
        cur_year, cur_month = get_current_year(), get_current_month()
        
        total_amount = cmodels.CoursePayment.objects.filter(course=models.OuterRef('id')).\
            annotate(total=models.Func(models.F('amount'), function='SUM')).values('total')

        cur_month_amount = cmodels.CoursePayment.objects.\
            filter(course=models.OuterRef('id')).\
            filter(payment_datetime__year=cur_year, payment_datetime__month=cur_month).\
                    annotate(total=models.Func(models.F('amount'), function='SUM')).values('total')

        total_reviews = rmodels.Review.objects.filter(course=models.OuterRef('id')).count('id')
        rating = rmodels.Review.objects.filter(course=models.OuterRef('id')).\
            annotate(rating=models.Func(models.F('rating'), function='AVG')).values('total')

        query = self.filter(subject_id=subject_id).annotate(
            reviews=models.Subquery(total_reviews),
            rating=models.Subquery(rating),
            payments=models.Subquery(total_amount),
            cur_month_payments=models.Subquery(cur_month_amount),
            students=models.Count('students', distinct=True),
            ).order_by('payments')
        return query
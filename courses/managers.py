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

        total_reviews = rmodels.Review.objects.filter(course=models.OuterRef('id')).\
            annotate(count=models.Func(models.F('id'), function='COUNT')).values('count')
        rating = rmodels.Review.objects.filter(course=models.OuterRef('id')).\
            annotate(avg_rating=models.Func(models.F('rating'), function='AVG', output_field=models.DecimalField())).values('avg_rating')

        num_students = self.\
            annotate(students_count=models.Func(models.F('students'), function='COUNT')).values('students_count')
        
        query = self.filter(subject_id=subject_id).only('id', 'name').annotate(
            num_reviews=models.Subquery(total_reviews),
            rating=models.Subquery(rating),
            total_payments=models.Subquery(total_amount),
            cur_month_payments=models.Subquery(cur_month_amount),
            num_students=models.Subquery(num_students),
            ).order_by('total_payments')
        return query
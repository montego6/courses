from django.db import models
# import courses.models 
from .utils import get_current_month, get_current_year
import reviews.models as rmodels
from django.apps import apps



class CategoryStatisticsManager(models.Manager):
    def all(self):
        cur_year, cur_month = get_current_year(), get_current_month()

        CoursePayment = apps.get_model(app_label='courses', model_name='CoursePayment')
        total_amount = CoursePayment.objects.filter(course__subject__parent_subcategory__parent_category=models.OuterRef('id')).\
            annotate(total=models.Func(models.F('amount'), function='SUM')).values('total')

        cur_month_amount = CoursePayment.objects.\
            filter(course__subject__parent_subcategory__parent_category=models.OuterRef('id')).\
            filter(payment_datetime__year=cur_year, payment_datetime__month=cur_month).\
                    annotate(total=models.Func(models.F('amount'), function='SUM')).values('total')
        
        query = self.annotate(
            courses=models.Count('subcategories__subjects__courses', distinct=True),
            payments=models.Subquery(total_amount),
            cur_month_payments=models.Subquery(cur_month_amount),
            students=models.Count('subcategories__subjects__courses__students', distinct=True),
            authors=models.Count('subcategories__subjects__courses__author', distinct=True)
            ).order_by('payments')
        return query
    

class SubCategoryStatisticsManager(models.Manager):
    def by_category(self, category_id):
        cur_year, cur_month = get_current_year(), get_current_month()

        CoursePayment = apps.get_model(app_label='courses', model_name='CoursePayment')
        total_amount = CoursePayment.objects.filter(course__subject__parent_subcategory=models.OuterRef('id')).\
            annotate(total=models.Func(models.F('amount'), function='SUM')).values('total')

        cur_month_amount = CoursePayment.objects.\
            filter(course__subject__parent_subcategory=models.OuterRef('id')).\
            filter(payment_datetime__year=cur_year, payment_datetime__month=cur_month).\
                    annotate(total=models.Func(models.F('amount'), function='SUM')).values('total')
        
        query = self.filter(parent_category_id=category_id).annotate(
            courses=models.Count('subjects__courses', distinct=True),
            payments=models.Subquery(total_amount),
            cur_month_payments=models.Subquery(cur_month_amount),
            students=models.Count('subjects__courses__students', distinct=True),
            authors=models.Count('subjects__courses__author', distinct=True)
            ).order_by('payments')
        return query
    

class SubjectStatisticsManager(models.Manager):
    def by_subcategory(self, subcategory_id):
        cur_year, cur_month = get_current_year(), get_current_month()
        
        CoursePayment = apps.get_model(app_label='courses', model_name='CoursePayment')
        total_amount = CoursePayment.objects.filter(course__subject=models.OuterRef('id')).\
            annotate(total=models.Func(models.F('amount'), function='SUM')).values('total')

        cur_month_amount = CoursePayment.objects.\
            filter(course__subject=models.OuterRef('id')).\
            filter(payment_datetime__year=cur_year, payment_datetime__month=cur_month).\
                    annotate(total=models.Func(models.F('amount'), function='SUM')).values('total')
        
        query = self.filter(parent_subcategory_id=subcategory_id).annotate(
            courses_num=models.Count('courses', distinct=True),
            payments=models.Subquery(total_amount),
            cur_month_payments=models.Subquery(cur_month_amount),
            students=models.Count('courses__students', distinct=True),
            authors=models.Count('courses__author', distinct=True)
            ).order_by('payments')
        return query
    

class CourseStatisticsManager(models.Manager):
    def by_subject(self, subject_id):
        cur_year, cur_month = get_current_year(), get_current_month()
        
        CoursePayment = apps.get_model(app_label='courses', model_name='CoursePayment')
        total_amount = CoursePayment.objects.filter(course=models.OuterRef('id')).\
            annotate(total=models.Func(models.F('amount'), function='SUM')).values('total')

        cur_month_amount = CoursePayment.objects.\
            filter(course=models.OuterRef('id')).\
            filter(payment_datetime__year=cur_year, payment_datetime__month=cur_month).\
                    annotate(total=models.Func(models.F('amount'), function='SUM')).values('total')

        total_reviews = rmodels.Review.objects.filter(course=models.OuterRef('id')).\
            annotate(count=models.Func(models.F('id'), function='COUNT')).values('count')
        rating = rmodels.Review.objects.filter(course=models.OuterRef('id')).\
            annotate(avg_rating=models.Func(models.F('rating'), function='AVG', output_field=models.DecimalField())).values('avg_rating')

        num_students = self.filter(id=models.OuterRef('id')).\
            annotate(students_count=models.Func(models.F('students'), function='COUNT')).values('students_count')
        
        query = self.filter(subject_id=subject_id).only('id', 'name').annotate(
            num_reviews=models.Subquery(total_reviews),
            rating=models.Subquery(rating),
            total_payments=models.Subquery(total_amount),
            cur_month_payments=models.Subquery(cur_month_amount),
            num_students=models.Subquery(num_students),
            ).order_by('total_payments')
        return query
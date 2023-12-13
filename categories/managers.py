

from datetime import datetime
from django.db import models

from courses.models import CoursePayment


class CategoryStatisticsManager(models.Manager):
    def all(self):
        cur_year, cur_month = datetime.now().year, datetime.now().month
        # total_amount_2 = CoursePayment.objects.\
        #     filter(course__subject__parent_subcategory__parent_category=models.OuterRef('id')).\
        #         values('course__subject__parent_subcategory__parent_category_id').\
        #             annotate(total=models.Sum('amount')).values('total')
        
        total_amount = CoursePayment.objects.filter(course__subject__parent_subcategory__parent_category=models.OuterRef('id')).\
            annotate(total=models.Func(models.F('amount'), function='SUM')).values('total')

        # cur_month_amount = CoursePayment.objects.\
        #     filter(course__subject__parent_subcategory__parent_category=models.OuterRef('id')).\
        #     filter(payment_datetime__year=cur_year, payment_datetime__month=cur_month).\
        #         values('course__subject__parent_subcategory__parent_category_id').\
        #             annotate(total=models.Sum('amount')).values('total')
        

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
            )
        print(query.query)
        return query
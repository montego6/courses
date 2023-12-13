

from django.db import models

from courses.models import CoursePayment


class CategoryStatisticsManager(models.Manager):
    def all(self):
        total_amount = CoursePayment.objects.\
            filter(course__subject__parent_subcategory__parent_category=models.OuterRef('id')).\
                values('course__subject__parent_subcategory__parent_category_id').\
                    annotate(total=models.Sum('amount')).values('total')
        query = self.annotate(
            courses=models.Count('subcategories__subjects__courses', distinct=True),
            payments=models.Subquery(total_amount),
            students=models.Count('subcategories__subjects__courses__students', distinct=True),
            authors=models.Count('subcategories__subjects__courses__author', distinct=True)
            )
        return query
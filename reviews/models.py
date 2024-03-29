
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Review(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    comment = models.CharField(max_length=400)
    rating = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(rating__lte=5), name='rating_lte_5')
        ]

    def __str__(self) -> str:
        return f'Review for course id={self.course.id} by student id={self.student.id}'
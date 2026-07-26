from django.db import models
from django.contrib.auth.models import User
from exchanges.models import SkillExchange


class Review(models.Model):

    exchange = models.OneToOneField(
        SkillExchange,
        on_delete=models.CASCADE
    )

    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='given_reviews'
    )

    reviewee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_reviews'
    )

    rating = models.PositiveSmallIntegerField()

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer.username} → {self.reviewee.username}"
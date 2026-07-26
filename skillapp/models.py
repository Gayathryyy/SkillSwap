from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):

    SKILL_TYPES = (

        ('teach', 'Can Teach'),
        ('learn', 'Want to Learn'),

    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='skills'
    )

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    skill_type = models.CharField(
        max_length=10,
        choices=SKILL_TYPES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.username} - {self.name}"
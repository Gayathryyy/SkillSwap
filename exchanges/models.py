from django.db import models
from django.contrib.auth.models import User
from skillapp.models import Skill


class SkillExchange(models.Model):

    STATUS_CHOICES = (

        ('pending', 'Pending'),

        ('accepted', 'Accepted'),

        ('rejected', 'Rejected'),

        ('completed', 'Completed'),

    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_exchanges'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_exchanges'
    )

    skill_requested = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name='requested_skill'
    )

    skill_offered = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name='offered_skill'
    )

    message = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.sender.username} → {self.receiver.username}"
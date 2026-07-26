from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from exchanges.models import SkillExchange
from .forms import ReviewForm
from .models import Review
from notifications.models import Notification

@login_required
def add_review(request, exchange_id):

    exchange = get_object_or_404(

        SkillExchange,

        id=exchange_id,

        sender=request.user,

        status='completed'

    )

    if Review.objects.filter(exchange=exchange).exists():

        messages.info(

            request,

            "You have already reviewed this exchange."

        )

        return redirect('sent_requests')

    if request.method == "POST":

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.exchange = exchange

            review.reviewer = request.user

            review.reviewee = exchange.receiver

            review.save()

            Notification.objects.create(
                user=exchange.receiver,
                message=f"{request.user.username} left you a review."
            )

            messages.success(

                request,

                "Review submitted successfully."

            )

            return redirect('sent_requests')

    else:

        form = ReviewForm()

    return render(

        request,

        'add_review.html',

        {

            'form': form,

            'exchange': exchange

        }

    )
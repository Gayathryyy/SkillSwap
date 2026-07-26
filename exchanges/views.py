from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from skillapp.models import Skill

from .models import SkillExchange

from .forms import SkillExchangeForm

from django.contrib import messages
from django.shortcuts import get_object_or_404
from notifications.models import Notification


@login_required
def send_exchange_request(request, user_id):

    receiver = get_object_or_404(

        User,

        id=user_id

    )

    form = SkillExchangeForm()

    form.fields['skill_requested'].queryset = Skill.objects.filter(

        user=receiver,

        skill_type='teach'

    )

    form.fields['skill_offered'].queryset = Skill.objects.filter(

        user=request.user,

        skill_type='teach'

    )

    if request.method == "POST":

        form = SkillExchangeForm(request.POST)

        form.fields['skill_requested'].queryset = Skill.objects.filter(

            user=receiver,

            skill_type='teach'

        )

        form.fields['skill_offered'].queryset = Skill.objects.filter(

            user=request.user,

            skill_type='teach'

        )

        if form.is_valid():
            exchange = form.save(commit=False)

            exchange.sender = request.user

            exchange.receiver = receiver

            exchange.save()

            print("Exchange saved successfully!")

            Notification.objects.create(
                user=receiver,
                message=f"{request.user.username} sent you a skill exchange request."
            )

            print("Notification created successfully!")

            messages.success(
                request,
                "Skill exchange request sent successfully."
            )

            return redirect('browse_skills')

    return render(

        request,

        'send_exchange.html',

        {

            'form': form,

            'receiver': receiver

        }

    )

@login_required
def exchange_inbox(request):

    requests = SkillExchange.objects.filter(
        receiver=request.user
    ).order_by('-created_at')


    return render(
        request,
        'exchange_inbox.html',
        {
            'requests': requests
        }
    )

@login_required
def accept_exchange(request, request_id):

    exchange = get_object_or_404(

        SkillExchange,

        id=request_id,

        receiver=request.user

    )

    exchange.status = "accepted"

    exchange.save()

    Notification.objects.create(
        user=exchange.sender,
        message=f"{request.user.username} accepted your skill exchange request."
    )

    messages.success(

        request,

        "Exchange request accepted."

    )

    return redirect("exchange_inbox")


@login_required
def reject_exchange(request, request_id):

    exchange = get_object_or_404(

        SkillExchange,

        id=request_id,

        receiver=request.user

    )

    exchange.status = "rejected"

    exchange.save()

    Notification.objects.create(
        user=exchange.sender,
        message=f"{request.user.username} rejected your skill exchange request."
    )

    messages.success(

        request,

        "Exchange request rejected."

    )

    return redirect("exchange_inbox")

@login_required
def complete_exchange(request, request_id):

    exchange = get_object_or_404(

        SkillExchange,

        id=request_id,

        receiver=request.user

    )

    if exchange.status == "accepted":

        exchange.status = "completed"

        exchange.save()

        Notification.objects.create(
            user=exchange.sender,
            message=f"{request.user.username} marked your exchange as completed."
        )

        messages.success(

            request,

            "Exchange marked as completed."

        )

    return redirect("exchange_inbox")


@login_required
def sent_requests(request):

    requests = SkillExchange.objects.filter(
        sender=request.user
    ).order_by('-created_at')

    return render(
        request,
        'sent_requests.html',
        {
            'requests': requests
        }
    )


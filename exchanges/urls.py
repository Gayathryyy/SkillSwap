from django.urls import path
from . import views

urlpatterns = [

    path(
        'request/<int:user_id>/',
        views.send_exchange_request,
        name='send_exchange'
    ),

    path(
        'inbox/',
        views.exchange_inbox,
        name='exchange_inbox'
    ),
path(
    'accept/<int:request_id>/',
    views.accept_exchange,
    name='accept_exchange'
),

path(
    'reject/<int:request_id>/',
    views.reject_exchange,
    name='reject_exchange'
),

path(
    'sent/',
    views.sent_requests,
    name='sent_requests'
),

path(
    'complete/<int:request_id>/',
    views.complete_exchange,
    name='complete_exchange'
),

]
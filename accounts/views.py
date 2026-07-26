from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from profiles.models import Profile
from .forms import RegisterForm
from .models import EmailOTP
from .utils import generate_otp, send_otp_email
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

from skillapp.models import Skill
from exchanges.models import SkillExchange
from reviews.models import Review
from notifications.models import Notification


def home(request):
    return render(request, 'home.html')


def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Username already exists?
            if User.objects.filter(username=username).exists():
                messages.error(
                    request,
                    "Username already exists. Please login instead."
                )

                return redirect('register')

            # Email already exists?
            if User.objects.filter(email=email).exists():
                messages.error(
                    request,
                    "Email already registered. Please login instead."
                )

                return redirect('register')

            otp = generate_otp()

            EmailOTP.objects.update_or_create(
                email=email,
                defaults={
                    'otp': otp,
                    'is_verified': False
                }
            )

            request.session['registration_data'] = {
                'username': username,
                'email': email,
                'password': password,
            }

            send_otp_email(email, otp)

            return redirect('verify_otp')

    else:

        form = RegisterForm()

    return render(request, 'register.html', {
        'form': form
    })

def verify_otp(request):

    if request.method == "POST":

        entered_otp = request.POST.get('otp')

        registration_data = request.session.get('registration_data')


        if not registration_data:
            messages.error(request, "Registration session expired. Please register again.")
            return redirect('register')


        email = registration_data['email']


        try:

            otp_record = EmailOTP.objects.get(email=email)


            if otp_record.otp == entered_otp:

                user = User.objects.create_user(
                    username=registration_data['username'],
                    email=registration_data['email'],
                    password=registration_data['password']
                )

                Profile.objects.create(
                    user=user
                )


                otp_record.is_verified = True
                otp_record.save()


                del request.session['registration_data']


                messages.success(
                    request,
                    "Account created successfully. Please login."
                )


                return redirect('login')


            else:

                messages.error(
                    request,
                    "Invalid OTP. Please try again."
                )


        except EmailOTP.DoesNotExist:

            messages.error(
                request,
                "OTP not found. Please register again."
            )


    return render(request, 'otp_verify.html')



def user_login(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user is not None:

            login(request, user)

            messages.success(
                request,
                "Login successful!"
            )

            return redirect('dashboard')


        else:

            messages.error(
                request,
                "Invalid username or password."
            )


    return render(request, 'login.html')

@login_required
def dashboard(request):

    user = request.user

    teaching_count = Skill.objects.filter(
        user=user,
        skill_type='teach'
    ).count()

    learning_count = Skill.objects.filter(
        user=user,
        skill_type='learn'
    ).count()

    pending_requests = SkillExchange.objects.filter(
        receiver=user,
        status='pending'
    ).count()

    completed_exchanges = SkillExchange.objects.filter(
        receiver=user,
        status='completed'
    ).count()

    unread_notifications = Notification.objects.filter(
        user=user,
        is_read=False
    ).count()

    average_rating = Review.objects.filter(
        reviewee=user
    ).aggregate(
        Avg('rating')
    )['rating__avg']

    return render(
        request,
        'dashboard.html',
        {
            'teaching_count': teaching_count,
            'learning_count': learning_count,
            'pending_requests': pending_requests,
            'completed_exchanges': completed_exchanges,
            'unread_notifications': unread_notifications,
            'average_rating': average_rating
        }
    )
def user_logout(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect('login')
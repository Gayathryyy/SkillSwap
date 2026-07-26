from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Skill
from .forms import SkillForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from profiles.models import Profile
from .models import Skill
from reviews.models import Review
from django.db.models import Avg



@login_required
def add_skill(request):

    if request.method == "POST":

        form = SkillForm(request.POST)

        if form.is_valid():

            skill = form.save(commit=False)

            skill.user = request.user

            skill.save()

            messages.success(
                request,
                "Skill added successfully!"
            )

            return redirect('my_skills')

    else:

        form = SkillForm()

    return render(
        request,
        'add_skill.html',
        {
            'form': form
        }
    )

@login_required
def my_skills(request):

    skills = request.user.skills.all()

    return render(
        request,
        'my_skills.html',
        {
            'skills': skills
        }
    )

@login_required
def edit_skill(request, skill_id):

    skill = Skill.objects.get(
        id=skill_id,
        user=request.user
    )

    if request.method == "POST":

        form = SkillForm(
            request.POST,
            instance=skill
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Skill updated successfully."
            )

            return redirect('my_skills')

    else:

        form = SkillForm(instance=skill)

    return render(
        request,
        'edit_skill.html',
        {
            'form': form
        }
    )


@login_required
def delete_skill(request, skill_id):

    skill = Skill.objects.get(
        id=skill_id,
        user=request.user
    )

    if request.method == "POST":

        skill.delete()

        messages.success(
            request,
            "Skill deleted successfully."
        )

        return redirect('my_skills')

    return render(
        request,
        'delete_skill.html',
        {
            'skill': skill
        }
    )

@login_required
def browse_skills(request):

    search = request.GET.get('search', '')

    users = User.objects.exclude(
        id=request.user.id
    )

    if search:

        users = users.filter(

            Q(username__icontains=search) |

            Q(profile__location__icontains=search) |

            Q(skills__name__icontains=search),

            skills__skill_type='teach'

        ).distinct()

    return render(

        request,

        'browse_skills.html',

        {

            'users': users,

            'search': search

        }

    )

@login_required
def public_profile(request, user_id):

    user = get_object_or_404(
        User.objects.select_related('profile').prefetch_related('skills'),
        id=user_id
    )

    reviews = Review.objects.filter(
        reviewee=user
    ).select_related(
        'reviewer'
    ).order_by(
        '-created_at'
    )

    average_rating = reviews.aggregate(
        Avg('rating')
    )['rating__avg']

    return render(
        request,
        'public_profile.html',
        {
            'profile_user': user,
            'reviews': reviews,
            'average_rating': average_rating
        }
    )
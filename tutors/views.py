from datetime import date, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
from django.contrib.auth.models import User
from . models import Location, Category, Tutors, Reviews
from .forms import TutorForm, ReviewForm, RatingForm, TutorImageForm


def tutors(request):
    """
    A view to display all the tutors and some information
    """

    tutors = Tutors.objects.all()
    active_tutors = Tutors.objects.filter(active=True)

    # date_joined = Tutors.objects.values_list("date_added", flat=True)

    
    # gone = Tutors.objects.filter(date_added__lt=expiry)
    # print(gone)
    # for g in gone:
    #     print(g)
    

    if active_tutors.exists():
        tutors = active_tutors
    else:
        tutors = None

    for tut in tutors:
        joined = tut.date_added
        day_joined = joined.day
        validity = day_joined + 6
        today = date.today() # - timedelta(days=1)
        if today.day < validity:
            tut.active = True
            print('I am still active')
        else:
            tut.active = False
            tut.save()
            print('I am no longer active')
            

    query = None

    sort = request.GET.get('sort')

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']

            queries = Q(name__icontains=query) | Q(subject__icontains=query) | Q(category__name__icontains=query) | Q(location__name__icontains=query)

            tutors = tutors.filter(queries)

    if sort == "price_low":
        tutors = tutors.order_by('price')
    elif sort == "price_high":
        tutors = tutors.order_by('-price')
    elif sort == "most_recent":
        tutors = tutors.order_by('-date_added')
    elif sort == "highest_rating":
        tutors = tutors.filter(rating__gt=0).order_by('-rating')

    context = {
                'tutors': tutors,
                'search': query,
                # 'expired': g
                }

    return render(request, 'tutors/tutors.html', context)


def tutor_details(request, tutor_id):
    """
    A view to show the details of each individual tutor
    """

    tutor = get_object_or_404(Tutors, pk=tutor_id)

    reviews = Reviews.objects.filter(tutor=tutor)

    template = 'tutors/tutor-details.html'

    context = {
        'tutor': tutor,
        'reviews': reviews,
        }

    return render(request, template, context)


def image_load(request, tutor_id):
    tutor = get_object_or_404(Tutors, pk=tutor_id)

    if request.method == 'POST':
        image_form = TutorImageForm(request.POST, request.FILES, instance=tutor)
        if image_form.is_valid():
            image_form.save()
            messages.success(request, 'Your Profile has succesfully been set up')
            send_mail(
                    'Profile Setup',
                    f"Dear {tutor.name}! \
                        Welcome to Tutor Line! You have succesfully setup your Tutor profile",
                    "info@tutor-line.co.uk",
                    [tutor.email],
                    fail_silently=False,
                )
            return redirect('tutors')
    else:
        image_form = TutorImageForm()

    context = {
        'tutor': tutor,
        'image_form': image_form
    }
    
    return render(request, 'tutors/image-load.html', context)


@login_required
def create_tutor(request, user_id):

    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = TutorForm(request.POST, user_id, request.FILES)
        if form.is_valid():
            tutor = form.save(commit=False)
            tutor.user = request.user
            tutor = form.save()
            if tutor.is_male:
                return redirect('image_load', tutor_id=tutor.id)
            else:
                messages.success(request, 'Your Profile has succesfully been set up')
                send_mail(
                    'Profile Setup',
                    f"Dear {tutor.name}! \
                        Welcome to Tutor Line! You have succesfully setup your Tutor profile",
                    "info@tutor-line.co.uk",
                    [user.email],
                    fail_silently=False,
                )
                return redirect('tutors')

    else:
        form = TutorForm()

    context = {
        'form': form,
        'user': user,
        }

    return render(request, 'tutors/create-tutor.html', context)


def review_tutor(request, tutor_id):

    tutor = get_object_or_404(Tutors, pk=tutor_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, tutor_id)

        if form.is_valid():
            # Save the new review
            review = form.save(commit=False)
            review.tutor = tutor
            review.save()

            # Recalculate the tutor's average rating
            avg_rating = Reviews.objects.filter(tutor=tutor).aggregate(
                avg=Avg('rating')
            )['avg']

            # Update tutor model
            Tutors.objects.filter(pk=tutor.pk).update(rating=avg_rating or 0)
            # tutor.rating = avg_rating or 0
            # tutor.save()
            messages.success(request, f'You have succesfully reviewed {tutor.name}')

            return redirect('tutors')
        
    else:
        form = ReviewForm()

    total = Reviews.objects.filter(tutor=tutor).aggregate(total=Sum('rating'))['total']

    context = {
        'form': form,
        'tutor': tutor,
        'total': total,
    }

    return render(request, 'tutors/review-tutor.html', context)

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

    """
    variables to show current date in day month and year
    """
    today = date.today()
    """
    loop over tutors to get date joined and compare to current date
    to check if account is still active
    """

    for tut in tutors:
        joined = tut.date_added
        expiry_date = today - timedelta(days=30)
        print(joined)
        print(f"if you joined on or before {expiry_date} you are no longer valid")

        """
        if statement to check if account is still active
        if account is no longer active, set active to false and save
        """
        if joined < expiry_date:
            tut.active = False
            tut.save()
            print("Your acount has expired, please renew here")
        else:
            tut.active = True
            print("Your account is still active")
        
        # validity = day_joined + 1
        # today = date.today() # - timedelta(days=1)
        # if today.day < validity:
        #     tut.active = True
        #     print('I am still active')
        # else:
        #     tut.active = False
        #     tut.save()
        #     print('I am no longer active')

    if active_tutors.exists():
        tutors = active_tutors
    else:
        tutors = None

    
            
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
                }

    return render(request, 'tutors/tutors.html', context)


def tutor_details(request, tutor_id):
    """
    A view to show the details of each individual tutor
    """

    tutor = get_object_or_404(Tutors, pk=tutor_id)

    if tutor.active == False:
        messages.error(request, 'This tutor is no longer active, please choose another tutor')
        return redirect('tutors')

    reviews = Reviews.objects.filter(tutor=tutor)

    template = 'tutors/tutor-details.html'

    context = {
        'tutor': tutor,
        'reviews': reviews,
        }

    return render(request, template, context)


def image_load(request, tutor_id):
    tutor = get_object_or_404(Tutors, pk=tutor_id)

    if request.user != tutor.user:
        messages.error(request, "You have no permission for this action.")
        return redirect('tutors')

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


def image_update(request, tutor_id):
    tutor = get_object_or_404(Tutors, pk=tutor_id)

    if request.user != tutor.user:
        messages.error(request, "You have no permission for this action.")
        return redirect('tutors')

    if request.method == 'POST':
        image_form = TutorImageForm(request.POST, request.FILES, instance=tutor)
        if image_form.is_valid():
            image_form.save()
            messages.success(request, 'Your Profile has succesfully been updated')
            send_mail(
                    'Profile Updated',
                    f"Dear {tutor.name}! \
                        Welcome to Tutor Line! You have succesfully updated your Tutor profile",
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
    
    return render(request, 'tutors/image-update.html', context)


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


@login_required
def edit_tutor(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    tutor = get_object_or_404(Tutors, user=user)

    if request.user.id != user_id:
        messages.error(request, "You are not allowed to edit this profile.")
        return redirect('tutors')


    if request.method == 'POST':
        form = TutorForm(request.POST, instance=tutor)
        if form.is_valid():
            form.save()
            if tutor.is_male:
                return redirect('image_update', tutor_id=tutor.id)
            else:
                messages.success(request, 'Your Profile has succesfully been updated')
                send_mail(
                    'Profile Updated',
                    f"Dear {tutor.name}! \
                        Welcome to Tutor Line! You have succesfully updated your Tutor profile",
                    "info@tutor-line.co.uk",
                    [user.email],
                    fail_silently=False,
                )
                return redirect('tutors')
    else:
        form = TutorForm(instance=tutor)

    context = {
        'form': form,
        'user': user,
        }

    return render(request, 'tutors/edit-tutor.html', context)


def payment_setup(request):
    return render(request, 'tutors/payment-setup.html')


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

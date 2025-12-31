from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.db.models import Sum
from . models import Location, Category, Tutors, Reviews
from .forms import TutorForm, ReviewForm, RatingForm


# Create your views here.
def tutors(request):
    """
    A view to display all the tutors and some information
    """

    tutors = Tutors.objects.all()
    query = None

    sort = request.GET.get('sort')

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']

            queries = Q(name__icontains=query) | Q(subject__icontains=query) | Q(category__name__icontains=query) | Q(location__name__icontains=query)

            tutors = tutors.filter(queries)

    rating_none = tutors.filter(rating=0)
    print(rating_none)

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

    reviews = Reviews.objects.filter(tutor=tutor)

    template = 'tutors/tutor-details.html'

    context = {
        'tutor': tutor,
        'reviews': reviews,
        }

    return render(request, template, context)


def create_tutor(request):

    if request.method == 'POST':
        form = TutorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tutors')
    else:
        form = TutorForm()

    return render(request, 'tutors/create-tutor.html', {'form': form})


def review_tutor(request, tutor_id):

    tutor = get_object_or_404(Tutors, pk=tutor_id)
    total = Reviews.objects.filter(tutor=tutor).aggregate(total=Sum('rating'))['total']
    print('the total number of ratings for this tutor is', total)

    if request.method == 'POST':
        form = ReviewForm(request.POST, tutor_id)
        form2 = RatingForm(request.POST, instance=tutor)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return redirect('tutors')
    else:
        form = ReviewForm()
        form2 = RatingForm()
  
    context = {'form': form,
               'tutor': tutor,
               'form2': form2,
               'total': total
               }

    return render(request, 'tutors/review-tutor.html', context)

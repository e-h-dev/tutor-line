from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from . models import Location, Category, Tutors, Reviews


# Create your views here.
def tutors(request):
    """
    A view to display all the tutors and some information
    """

    tutors = Tutors.objects.all()

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']

            queries = Q(name__icontains=query) | Q(subject__icontains=query) | Q(category__name__icontains=query) | Q(location__name__icontains=query)

            tutors = tutors.filter(queries)

    context = {'tutors': tutors}
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

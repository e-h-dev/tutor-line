from django.shortcuts import render, get_object_or_404
from . models import Location, Category, Tutors


# Create your views here.
def tutors(request):
    """
    A view to display all the tutors and some information
    """

    tutors = Tutors.objects.all()
    context = {'tutors': tutors}
    return render(request, 'tutors/tutors.html', context)


def tutor_details(request, tutor_id):
    """
    A view to show the details of each individual tutor
    """

    tutor = get_object_or_404(Tutors, pk=tutor_id)

    template = 'tutors/tutor-details.html'

    context = {'tutor':tutor}

    return render(request, template, context)

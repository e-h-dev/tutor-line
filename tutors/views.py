from django.shortcuts import render
from . models import Location, Category, Tutors


# Create your views here.
def tutors(request):
    """
    A view to display all the tutors and some information
    """

    tutors = Tutors.objects.all()
    context = {'tutors': tutors}
    return render(request, 'tutors/tutors.html', context)


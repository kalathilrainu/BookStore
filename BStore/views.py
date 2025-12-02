from django.shortcuts import render

def home(request):
    """
    Landing page – lets user choose Admin or User.
    """
    return render(request, 'landing.html')

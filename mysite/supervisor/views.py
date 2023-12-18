from django.shortcuts import render, get_object_or_404

# Create your views here.

def testpage(request):
    return render(request, 'supervisor/list.html', {})

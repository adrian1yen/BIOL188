from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

@csrf_protect
@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html')

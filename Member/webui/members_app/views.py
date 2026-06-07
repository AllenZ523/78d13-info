from django.shortcuts import render
from .models import Member


def index(request):
    qs = Member.objects.all()[:200]
    return render(request, 'members_app/index.html', {'members': qs})

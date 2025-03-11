from django.shortcuts import render
from .models import Member

def nba_list(request):
    members = Member.objects.all()

    return render(request, 'members/nba_list.html', {'members': members})
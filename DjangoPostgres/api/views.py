from django.shortcuts import render
from api.models import ResUsers

# Create your views here.
def index_page(request):
  users = ResUsers.objects.all()

  data = {
    'users': users
  }

  return render(request, 'user/index.html', data)

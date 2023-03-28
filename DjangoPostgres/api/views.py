from django.shortcuts import render
from api.models import ResUsers
import numpy as np

import xmlrpc.client

# Configurar la conexión
url = 'http://localhost:8069'
db = 'odooDB'
username = 'email@email.com'
password = 'odooDB'

# Establecer la conexión
info = xmlrpc.client.ServerProxy('https://demo.odoo.com/start').start()
url, db, username, password = info['host'], info['database'], info['user'], info['password']

#Login
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
common.version()
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
models.execute_kw(db, uid, password, 'res.partner', 'check_access_rights', ['read'], {'raise_exception': False})


# Create your views here.
def index_page(request):
  users = ResUsers.objects.all()

  data = {
    'users': users
  }

  return render(request, 'user/index.html', data)

def home_page(request):

  response = models.execute_kw(db, uid, password, 'product.product', 'search_read', [], {'fields': ['name', 'description', 'lst_price', 'categ_id', 'sale_ok' ]})
  # print('response', response)

  # category_ids = []
  # for x in response:
  #   for y in x['categ_id']:
  #     if (isinstance(y, int)):
  #       category_ids.append(y)
  
  # print('Categories:', category_ids)
  # response2 = models.execute_kw(db, uid, password, 'product.category', 'search_read', [[('id', 'in', category_ids)]], {'fields': ['name'], 'limit': 1})
  # print('Response2:', response2)

  data = {
    'object_list': response
  }

  return render(request, 'index.html', data)

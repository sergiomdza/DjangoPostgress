from django.shortcuts import render, redirect
from api.models import ResUsers

import xmlrpc.client

# Configurar la conexión
url = 'http://18.223.171.177:8069'
db = 'odooDB'
username = 'sergio_mdza@outlook.com'
password = 'odoo'

#Login
common = xmlrpc.client.ServerProxy('%s/xmlrpc/2/common' % url)
common.version()
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy('%s/xmlrpc/2/object' % url)
models.execute_kw(db, uid, password, 'res.partner', 'check_access_rights', ['read'], {'raise_exception': False})

# Create your views here.
def index_page(request):
  users = ResUsers.objects.all()

  data = {
    'users': users
  }

  return render(request, 'user/index.html', data)

def home_page(request):

  response = models.execute_kw(db, uid, password, 'product.product', 'search_read', [], { 'fields': ['name', 'description', 'lst_price', 'categ_id', 'sale_ok' ] })

  data = {
    'object_list': response
  }

  return render(request, 'index.html', data)

def product_details(request, id):

  response = models.execute_kw(db, uid, password, 'product.product', 'search_read', [[['id', '=', id]]], { 'fields': ['id', 'name', 'description', 'lst_price'] })

  stockResponse = models.execute_kw(db, uid, password, 'stock.quant', 'search_read', [[['product_id', '=', id]]], { 'fields': ['id', 'product_id', 'company_id', 'location_id', 'quantity' ], 'limit': 1 })

  data = {
    'object': response[0],
    'quantity': stockResponse[0]['quantity'] if len(stockResponse) > 0 else 0
  }

  return render(request, 'details.html', data)

def add_product(request):
  if request.method == 'POST':
    name, description, price = request.POST.get('name'), request.POST.get('description'), request.POST.get('price')

    id = models.execute_kw(db, uid, password, 'product.product', 'create', [{ 
      "name": name,
      "description": description,
      "list_price": int(price)
    }])

    # models.execute_kw(db, uid, password, 'stock.quant', 'create', [{ 
    #   "product_id": id,
    #   "company_id": 1,
    #   "location_id": 1,
    #   "reserved_quantity": 0
    # }])

    return redirect('home_page')

  return render(request, 'add_product.html')

def edit_product(request, id):
  if request.method == 'POST':
    name, description, price = request.POST.get('name'), request.POST.get('description'), request.POST.get('price')

    models.execute_kw(db, uid, password, 'product.product', 'write', [[id], { "name": name, "description": description, "price": price }])

    return redirect('product_details', id=id)

  response = models.execute_kw(db, uid, password, 'product.product', 'search_read', [[['id', '=', id]]], { 'fields': ['id', 'name', 'description', 'lst_price'] })

  data = {
    'object': response[0]
  }

  return render(request, 'edit_product.html', data)

def delete_product(request, id):
  models.execute_kw(db, uid, password, 'product.product', 'unlink', [[id]])

  return redirect('home_page')

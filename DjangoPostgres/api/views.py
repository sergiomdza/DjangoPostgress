from django.shortcuts import render, redirect
from api.models import ResUsers

import xmlrpc.client
import base64
import chardet

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

def get_decoded_image(byte_string):
  product_image = base64.b64decode(byte_string) if byte_string else None
  src = None

  if product_image != None:
      src = 'data:image/jpeg;base64,' + base64.b64encode(product_image).decode('latin1')

  return src

# Create your views here.
def index_page(request):
  users = ResUsers.objects.all()

  data = {
    'users': users
  }

  return render(request, 'user/index.html', data)

def home_page(request):

  response = models.execute_kw(db, uid, password, 'product.product', 'search_read', [], { 'fields': ['name', 'description', 'lst_price', 'categ_id', 'sale_ok', 'image_512' ] })

  for object in response:
    object['image_512'] = get_decoded_image(object['image_512'])

  data = {
    'object_list': response
  }

  return render(request, 'index.html', data)

def product_details(request, id):

  response = models.execute_kw(db, uid, password, 'product.product', 'search_read', [[['id', '=', id]]], { 'fields': ['id', 'name', 'description', 'lst_price', 'image_512'] })

  image_src_string = get_decoded_image(response[0]['image_512'])

  # stockResponse = models.execute_kw(db, uid, password, 'stock.quant', 'search_read', [[['product_id', '=', id]]], { 'fields': ['id', 'product_id', 'company_id', 'location_id', 'quantity' ], 'limit': 1 })

  data = {
    'object': response[0],
    'quantity': 0,
    'product_image': image_src_string
    # 'quantity': stockResponse[0]['quantity'] if len(stockResponse) > 0 else 0
  }

  return render(request, 'details.html', data)

def add_product(request):
  if request.method == 'POST':
    name, description, price = request.POST.get('name'), request.POST.get('description'), request.POST.get('price')
    image = request.FILES['image'].read()
    encoded_image = base64.b64encode(image)

    id = models.execute_kw(db, uid, password, 'product.product', 'create', [{ 
      "name": name,
      "description": description,
      "list_price": int(price),
      "image_1920": encoded_image.decode('latin1')
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

    image = None

    product_data = {
        "name": name,
        "description": description,
        "price": price
      }

    try:
      image = request.FILES['image'].read()
      image = base64.b64encode(image)

      if image:
        product_data['image_1920'] = image.decode('latin1')

      models.execute_kw(db, uid, password, 'product.product', 'write', [[id], product_data])

      return redirect('product_details', id=id)
    except:
      models.execute_kw(db, uid, password, 'product.product', 'write', [[id], product_data])

      return redirect('product_details', id=id)

  response = models.execute_kw(db, uid, password, 'product.product', 'search_read', [[['id', '=', id]]], { 'fields': ['id', 'name', 'description', 'lst_price'] })

  data = {
    'object': response[0]
  }

  return render(request, 'edit_product.html', data)

def delete_product(request, id):
  models.execute_kw(db, uid, password, 'product.product', 'unlink', [[id]])

  return redirect('home_page')

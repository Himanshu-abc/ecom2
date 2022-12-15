import json
import os
import datetime
import aspose.words as aw
import mimetypes
import re

from io import BytesIO
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.forms import inlineformset_factory
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from collections import *

from .utils import *
from .decorator import *
from .forms import *


# Create your views here.

@unauthenticated_user
def register(request):
    if request.method == 'POST':

        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('name')
            messages.success(request, 'Account created successfully Please complete the necessary details in account '
                                      'settings on first login for better experience', username)
            return redirect('login')

    form = RegisterForm()
    context = {'form': form}

    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(store)
        else:
            messages.info(request, 'username or password incorrect')
    return render(request, 'accounts/login_page.html')


def logout_page(request):
    logout(request)
    return redirect(login_page)


@login_required(login_url='login')
@allowed_roles(allowed_role=['shopkeeper'])
def shopkeeper_product_add(request):
    shopkeeper = Shopkeeper.objects.get(user=request.user)
    form = productAddForm()
    if request.method == 'POST':
        form = productAddForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.shopkeeper = shopkeeper
            product.save()
            return redirect(shopkeeper_product_add)

    data = cartData(request)
    cart_quantity = data['cart_quantity']

    context = {'form': form, 'cart_quantity': cart_quantity}
    return render(request, 'accounts/product_add.html', context)


@login_required(login_url='login')
@allowed_roles(allowed_role=['shopkeeper'])
def shopkeeper_create_tag(request):
    form = createTagForm()
    if request.method == 'POST':
        form = createTagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store')

    data = cartData(request)
    cart_quantity = data['cart_quantity']

    context = {'form': form, 'cart_quantity': cart_quantity}
    return render(request, 'accounts/create_tag.html', context)


@login_required(login_url='login')
@allowed_roles(allowed_role=['shopkeeper'])
def shopkeeper_multiple_product_add(request):
    productFormSet = inlineformset_factory(Shopkeeper, Product, fields=('__all__'), exclude=['shopkeeper', 'id'],
                                           extra=5)
    shopkeeper = Shopkeeper.objects.get(user=request.user)
    formset = productFormSet(queryset=Product.objects.none(), instance=shopkeeper)
    if request.method == 'POST':
        formset = productFormSet(request.POST, request.FILES, instance=shopkeeper)
        if formset.is_valid():
            formset.save()
            return redirect(store)

    data = cartData(request)
    cart_quantity = data['cart_quantity']

    context = {'form': formset, 'cart_quantity': cart_quantity}
    return render(request, 'accounts/product_multiple_add.html', context)


@login_required(login_url='login')
@allowed_roles(allowed_role=['shopkeeper'])
def shopkeeper_all_products(request):
    shopkeeper = Shopkeeper.objects.get(user=request.user)
    products = Product.objects.filter(shopkeeper=shopkeeper)

    data = cartData(request)
    cart_quantity = data['cart_quantity']

    context = {'products': products, 'shopkeeper': shopkeeper, 'cart_quantity': cart_quantity}
    return render(request, 'accounts/product_all.html', context)


@login_required(login_url='login')
@allowed_roles(allowed_role=['shopkeeper'])
def shopkeeper_product_update(request, pk):
    product = Product.objects.get(pk=pk)
    form = productAddForm(instance=product)

    if request.method == 'POST':
        form = productAddForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect(shopkeeper_all_products)

    data = cartData(request)
    cart_quantity = data['cart_quantity']

    context = {'form': form, 'cart_quantity': cart_quantity}
    return render(request, 'accounts/product_add.html', context)


@login_required(login_url='login')
@allowed_roles(allowed_role=['shopkeeper'])
def shopkeeper_product_delete(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect(shopkeeper_all_products)

    data = cartData(request)
    cart_quantity = data['cart_quantity']

    context = {'product': product, 'cart_quantity': cart_quantity}
    return render(request, 'accounts/product_delete.html', context)


@login_required(login_url='login')
def product_view(request, pk):
    product = Product.objects.get(pk=pk)

    data = cartData(request)
    cart_quantity = data['cart_quantity']

    context = {'product': product, 'cart_quantity': cart_quantity}
    return render(request, 'accounts/view_product.html', context)


@login_required(login_url='login')
def add_address(request):
    data = cartData(request)
    cart_quantity = data['cart_quantity']
    user = data["current_user"]
    form = addressForm()
    if request.method == 'POST':
        form = addressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.content_object = user
            address.save()
            return redirect('account_setting')

    context = {'form': form, 'cart_quantity': cart_quantity}
    return render(request, 'accounts/add_address.html', context)


@login_required(login_url='login')
def edit_address(request, pk):
    data = cartData(request)
    cart_quantity = data['cart_quantity']

    address = Address.objects.get(pk=pk)
    form = addressForm(instance=address)

    if request.method == 'POST':
        form = addressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('account_setting')

    context = {'form': form, 'cart_quantity': cart_quantity}
    return render(request, 'accounts/edit_address.html', context)


@login_required(login_url='login')
def manage_address(request):
    group = str(request.user.groups.get())
    if group == 'customer':
        user = Customer.objects.get(user=request.user)
        address = Address.objects.filter(customer__name=user.name)
    elif group == 'shopkeeper':
        user = Shopkeeper.objects.get(user=request.user)
        address = Address.objects.filter(shopkeeper__name=user.name)

    data = cartData(request)
    cart_quantity = data['cart_quantity']
    selected_address = data['selected_address']

    if request.method == 'POST':
        addr = request.POST.get('address')
        if addr is not None:
            new_selected = Address.objects.get(id=addr)
        else:
            messages.warning(request, 'Please add or select an address')
            return redirect(manage_address)

        if selected_address:
            selected_address.selected = False
            selected_address.save()
        new_selected.selected = True
        new_selected.save()
        return redirect('account_setting')

    context = {'address': address, 'cart_quantity': cart_quantity}
    return render(request, 'accounts/manage_address.html', context)


@login_required(login_url='login')
def account_settings(request):
    group = str(request.user.groups.get())
    if group == 'customer':
        user = Customer.objects.get(user=request.user)
        form = customerSettingForm(instance=user)

    elif group == 'shopkeeper':
        user = Shopkeeper.objects.get(user=request.user)
        form = shopkeeperSettingForm(instance=user)

    if request.method == 'POST':
        if group == 'customer':
            form = customerSettingForm(request.POST, request.FILES, instance=user)
        elif group == 'shopkeeper':
            form = shopkeeperSettingForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('store')

    data = cartData(request)
    cart_quantity = data['cart_quantity']
    selected_address = data['selected_address']

    address_form = None
    if selected_address is not None:
        address_form = addressForm(instance=selected_address)

    context = {'form': form, 'cart_quantity': cart_quantity, 'user': user, 'selected_address': selected_address,
               'address_form': address_form}

    return render(request, 'accounts/accounts_setting.html', context)


@login_required(login_url='login')
def store(request):
    group = str(request.user.groups.get())
    if group == 'customer':
        current_user = Customer.objects.get(user=request.user)
        products = Product.objects.all()
    elif group == 'shopkeeper':
        current_user = Shopkeeper.objects.get(user=request.user)
        products = Product.objects.exclude(shopkeeper=current_user)

    data = cartData(request)
    cart_quantity = data['cart_quantity']

    context = {'products': products, 'cart_quantity': cart_quantity}

    return render(request, 'accounts/store.html', context)


@login_required(login_url='login')
def update_cart(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    product = Product.objects.get(id=product_id)

    data = cartData(request)
    order = data['order']

    orderItem, created = OrderItem.objects.get_or_create(product=product, order=order)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)

    if action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    if action == 'delete':
        orderItem.quantity = 0

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    if order.final_amount != 0:
        order.final_amount = 0
        order.save()

    return JsonResponse('Item was added', safe=False)


@login_required(login_url='login')
def cart(request):
    data = cartData(request)
    cart_quantity = data['cart_quantity']
    items = data['items']
    cart_total = data['cart_total']

    context = {'cart_total': cart_total, 'items': items, 'cart_quantity': cart_quantity}

    return render(request, 'accounts/cart.html', context)


@login_required(login_url='login')
def checkout(request):
    data = cartData(request)
    cart_quantity = data['cart_quantity']
    items = data['items']
    cart_total = data['cart_total']
    order = data['order']
    current_user = data['current_user']
    selected_address = data['selected_address']

    context = {'cart_total': cart_total, 'items': items, 'cart_quantity': cart_quantity, 'user': current_user,
               'order': order, 'selected_address': selected_address}

    return render(request, 'accounts/checkout.html', context)


@login_required(login_url='login')
def process_order(request):
    data = json.loads(request.body)

    data1 = cartData(request)
    order = data1['order']
    current_user = data1['current_user']

    total = float(data['form']['total'])

    # total_inside = (order.getCartTotal + order.getTax)
    # total_inside = float("%.2f" % total_inside)
    # print('total_inside', total_inside)
    # if total == total_inside:

    order.completed = True
    order.save()
    print("all ok here")

    # order.completed = True
    order.delivered = True
    order.save()

    Invoice.objects.create(content_object=current_user, order=order, date=datetime.date.today(),
                           name=data['form']['name'], email=data['form']['email'], phone=data['form']['phone'],
                           address=data['shipping']['address'], city=data['shipping']['city'],
                           state=data['shipping']['state'], zipcode=data['shipping']['zipcode'],
                           country=data['shipping']['country'], )
    print('object created')

    return JsonResponse('Payment submitted....', safe=False)


# @csrf_exempt
# def search(request):
#     data = json.loads(request.body)
#     query = data['query']
#     product = Product.objects.filter(product_name__icontains=query)
#     products = serializers.serialize('json', product)
#     print(products[0])
#     return HttpResponse(products, content_type="application/json")

@login_required(login_url='login')
def user_orders(request):
    data = cartData(request)
    current_user = data['current_user']
    orders = current_user.order.all()
    cart_quantity = data['cart_quantity']
    context = {'current_user': current_user, 'orders': orders, 'cart_quantity': cart_quantity}
    return render(request, 'accounts/orders.html', context)


@login_required(login_url='login')
def categories(request, tag):
    products = Product.objects.filter(tags__tag_name=tag)
    if len(products) == 0:
        messages.info(request, 'No item found, please return Home')
    data = cartData(request)
    cart_quantity = data['cart_quantity']
    context = {'products': products, 'cart_quantity': cart_quantity}
    return render(request, 'accounts/store.html', context)


@login_required(login_url='login')
@csrf_exempt
def search2(request):
    query = request.GET.get("search_query")
    # products = Product.objects.filter(product_name__icontains=query)

    text = query
    text = re.escape(text)  # make sure there are no regex specials
    products = Product.objects.filter(product_name__iregex=r"(^|\s)%s" % text)

    data = cartData(request)
    cart_quantity = data['cart_quantity']
    if len(products) == 0:
        messages.info(request, 'No item found, please return Home')
    context = {'products': products, 'cart_quantity': cart_quantity}
    return render(request, 'accounts/store.html', context)


# @login_required(login_url='login')
# def download_and_view_invoice(request, pk):
#     order = Order.objects.get(pk=pk)
#     invoice_id = order.invoice.id
#     invoice = Invoice.objects.get(pk=invoice_id)
#
#     path = (os.path.join(os.getcwd(), 'invoice_files'))
#     f = open(path + "/invoice_" + str(datetime.datetime.now()) + "_.txt", "a")
#     f.write(str(vars(invoice)))
#     f.close()
#
#     # load the text file path
#     file = (os.path.join(path, f.name))
#
#     # load TXT document for pdf conversion
#     doc = aw.Document(file)
#
#     # save TXT as PDF file
#     pdf_name = f.name[:-4] + ".pdf"
#     doc.save(pdf_name, aw.SaveFormat.PDF)
#
#     # get pdf file path
#     pdf_path = (os.path.join(path, pdf_name))
#
#     # delete the text file
#     os.remove(f.name)
#
#     # Open the file for reading content
#     path = open(pdf_path, 'rb')
#     # Set the mime type
#     mime_type, _ = mimetypes.guess_type(pdf_path)
#     # Set the return value of the HttpResponse
#     response = FileResponse(path, content_type=mime_type)
#     # Set the HTTP header for sending to browser
#     response['Content-Disposition'] = "attachment; filename=%s" % pdf_path
#     # Return the response value
#     return response

@login_required(login_url='login')
def view_invoice(request, pk):
    order = Order.objects.get(pk=pk)
    invoice_id = order.invoice.id
    invoice = Invoice.objects.get(pk=invoice_id)

    # path = (os.path.join(os.getcwd(), 'invoice_files'))
    # f = open(path + "/invoice_" + str(datetime.datetime.now()) + "_.txt", "a")
    # f.write(str(vars(invoice)))
    # f.close()
    # file = (os.path.join(path, f.name))
    # path = open(file, 'r')
    # os.remove(f.name)
    # return HttpResponse(path)
    context = {'invoice': invoice}
    return render(request, 'accounts/invoice.html', context)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


@login_required(login_url='login')
# Opens up page as PDF and then download manually
def view_and_download_invoice(request, pk):
    order = Order.objects.get(pk=pk)
    invoice_id = order.invoice.id
    invoice = Invoice.objects.get(pk=invoice_id)
    context = {'invoice': invoice}

    file_path = 'accounts/templates/accounts/invoice.html'
    path1 = (os.path.join(os.getcwd(), file_path))

    pdf = render_to_pdf(path1, context)
    return HttpResponse(pdf, content_type='application/pdf')


@login_required(login_url='login')
# Automatically downloads to PDF file
def download_invoice(request, pk):
    order = Order.objects.get(pk=pk)
    invoice_id = order.invoice.id
    invoice = Invoice.objects.get(pk=invoice_id)
    context = {'invoice': invoice}

    file_path = 'accounts/templates/accounts'
    path1 = (os.path.join(os.getcwd(), file_path + '/invoice.html'))

    pdf = render_to_pdf(path1, context)

    response = HttpResponse(pdf, content_type='application/force-download')
    filename = "Invoice_" + str(pk) + "_%s.pdf" % str(datetime.datetime.now().replace(microsecond=0))
    content = "attachment; filename='%s'" % filename
    response['Content-Disposition'] = content
    return response


@login_required(login_url='login')
@allowed_roles(allowed_role=['shopkeeper'])
def shop_orders(request):
    data = cartData(request)
    shopkeeper = data['current_user']
    cart_quantity = data['cart_quantity']
    data2 = shopOrdersData(request)
    shop_name = data2['shop_name']
    records_list = data2['records']

    context = {'records': records_list, 'shop_name': shop_name, 'cart_quantity': cart_quantity}
    return render(request, 'accounts/shop_orders.html', context)


def users_list(request):
    data1 = cartData(request)
    cart_quantity = data1['cart_quantity']
    data2 = shopOrdersData(request)
    records_list = data2['records']

    users = set()
    for i in records_list:
        users.add(i.user)
    users = list(users)

    # common coupons
    coupons = Coupon.objects.filter(created_for=None)

    context = {'users': users, 'cart_quantity': cart_quantity, 'coupons': coupons}
    return render(request, 'accounts/user_list.html', context)


def create_coupon(request, user_name):
    print(user_name)
    data = cartData(request)
    current_user = data['current_user']
    # coupons = Coupon.objects.filter(created_for=user_name)
    coupons = Coupon.objects.filter(created_for=user_name, creator_name=current_user)
    form = createCoupon()
    if request.method == 'POST':
        form = createCoupon(request.POST)
        if form.is_valid():
            coupon = form.save(commit=False)
            if user_name != 'all':
                coupon.creator_name = current_user
                coupon.created_for = user_name
            coupon.save()
        return redirect(users_list)

    context = {'form': form, 'user_name': user_name, 'coupons': coupons}
    return render(request, 'accounts/create_coupon.html', context)


def get_coupon(request, user_name):
    # coupons = Coupon.objects.filter(created_for=user_name)
    coupons = Coupon.objects.filter(Q(created_for=user_name) | Q(created_for=None))
    context = {'coupons': coupons, 'user_name': user_name}
    return render(request, 'accounts/user_coupons.html', context)


def apply_coupon(request):
    data = json.loads(request.body)
    code = data['coupon_code']
    data1 = cartData(request)
    current_user = data1['current_user']
    order = data1['order']

    # coupons = Coupon.objects.filter(created_for=str(current_user))
    coupons = Coupon.objects.filter(Q(created_for=str(current_user)) | Q(created_for=None))
    is_applicable = 'NO'

    for coupon in coupons:
        if coupon.coupon_code == code:
            if not coupon.is_expired() and coupon.used is False:
                is_applicable = 'YES'
                break

    if is_applicable == 'YES':
        # -1 for coupon not applicable cause cart total below coupon offer limit
        if order.netAfterCoupon(0) < coupon.allowed_above:
            final_value = -1
        else:
            discount = coupon.discount
            final_value = order.netAfterCoupon(discount)
            coupon.used = True
            coupon.save()

    # 0 means coupon code not found or coupon expired
    if is_applicable == 'NO':
        final_value = 0

    final_value = round(final_value, 2)
    order.final_amount = final_value
    order.save()
    print(order.final_amount)

    data = {'final_value': order.final_amount, 'is_applied': is_applicable}
    return JsonResponse(data, safe=False)


def temp(request):
    coupon = Coupon.objects.all()
    for i in coupon:
        print(i.created_for)
        print(i.creator_name)
    context = {}
    return render(request, 'accounts/temp.html', context)


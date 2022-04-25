from .models import *
from django.contrib.auth.decorators import login_required
from collections import *


@login_required(login_url='login')
def cartData(request):
    group = str(request.user.groups.get())
    if group == 'customer':
        current_user = Customer.objects.get(user=request.user)
        address = Address.objects.filter(customer__name=current_user.name)
    elif group == 'shopkeeper':
        current_user = Shopkeeper.objects.get(user=request.user)
        address = Address.objects.filter(shopkeeper__name=current_user.name)
    try:
        order = current_user.order.all().get(completed=False)
    except:
        order = Order(content_object=current_user, completed=False)
        order.save()

    items = order.orderitem_set.all()
    cart_quantity = order.getCartQuantity
    cart_total = order.getCartTotal

    selected_address = None
    if len(address):
        for item in address:
            if item.selected:
                selected_address = item
                break

    return {'current_user': current_user, 'cart_total': cart_total, 'items': items, 'cart_quantity': cart_quantity,
            'order': order, 'selected_address': selected_address}


@login_required(login_url='login')
def shopOrdersData(request):
    data = cartData(request)
    shopkeeper = data['current_user']
    shop_name = shopkeeper.shop_name
    record = namedtuple('Record',
                        ['order_id', 'order_date', 'user', 'user_id', 'product_name', 'quantity', 'price',
                         'product_total'])
    records_list = []

    orders = Order.objects.filter(completed=True)
    for order in orders:
        for item in order.orderitem_set.all():
            if item.product.shopkeeper.shop_name == shop_name:
                r = record(order.id, order.date_ordered, order.content_object, order.object_id,
                           item.product.product_name, item.quantity,
                           item.product.price, item.getTotal)
                records_list.append(r)

    return {'records': records_list, 'shop_name': shop_name, }

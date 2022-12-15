import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.core.validators import MinValueValidator, MaxValueValidator
import decimal


# Create your models here.

class Person(models.Model):
    # on_delete defines what will happen when parent model is deleted
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    profile_pic = models.ImageField(default='default.jpg', blank=True, null=True)
    date_created = models.DateField(auto_now_add=True, null=True)

    class Meta:
        abstract = True
        ordering = ['date_created']

    def __str__(self):
        return self.user.username


class Order(models.Model):
    # Generic foreign Key
    # on_delete defines what will happen when parent model is deleted
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    date_ordered = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    final_amount = models.FloatField(default=0, null=True, blank=True)

    class Meta:
        ordering = ['-date_ordered', 'delivered', 'completed']

    def __str__(self):
        return str(self.id)

    @property
    def getCartQuantity(self):
        quantity = 0
        orderItems = self.orderitem_set.all()
        for item in orderItems:
            quantity += item.quantity
        return quantity

    @property
    def getCartTotal(self):
        total = 0
        orderItems = self.orderitem_set.all()
        for item in orderItems:
            total += item.getTotal
            total = float("%.2f" % total)
        return total

    @property
    def getTax(self):
        total = self.getCartTotal
        tax = total * (12 / 100)
        tax = float("%.2f" % tax)
        return tax

    @property
    def netValue(self):
        total = self.getCartTotal
        tax = self.getTax
        return total + tax

    def netAfterCoupon(self, discount=0):
        net_value = self.netValue
        total_discount = net_value * (float(discount) / 100)
        final_value = net_value - total_discount
        return final_value


class Address(models.Model):
    # Generic foreign Key user
    # on_delete defines what will happen when parent model is deleted
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    address = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zipcode = models.PositiveIntegerField(null=True, blank=True)
    date = models.DateField(auto_created=True, null=True, blank=True)
    selected = models.BooleanField(default=False)

    def __str__(self):
        return self.address

    @property
    def get_id(self):
        return str(self.id)


class Invoice(models.Model):
    # Generic foreign Key user
    # on_delete defines what will happen when parent model is deleted
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    # order
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, blank=True, null=True)

    # user info
    name = models.CharField(max_length=100, null=True, blank=False)
    email = models.CharField(max_length=100, null=True, blank=False)
    phone = models.CharField(max_length=20, null=True, blank=False)

    # shipping info
    address = models.CharField(max_length=200, null=True, blank=False)
    city = models.CharField(max_length=50, null=True, blank=False)
    state = models.CharField(max_length=50, null=True, blank=False)
    country = models.CharField(max_length=50, null=True, blank=False)
    zipcode = models.PositiveIntegerField(null=True, blank=False)
    date = models.DateField(auto_created=True, null=True, blank=False)

    def __str__(self):
        return str(self.id)


class Customer(Person):
    order = GenericRelation(Order, related_query_name='customer')
    invoice = GenericRelation(Invoice, related_query_name='customer')
    address = GenericRelation(Address, related_query_name='customer')


class Shopkeeper(Person):
    shop_name = models.CharField(max_length=100, blank=True, null=True)
    order = GenericRelation(Order, related_query_name='shopkeeper')
    invoice = GenericRelation(Invoice, related_query_name='shopkeeper')
    address = GenericRelation(Address, related_query_name='shopkeeper')


class Coupon(models.Model):
    PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

    creator_name = models.ForeignKey(Shopkeeper, on_delete=models.CASCADE, blank=True, null=True,
                                     help_text='coupon creator')
    created_for = models.CharField(max_length=50, blank=True, null=True, help_text='coupon for')
    coupon_name = models.CharField(max_length=50, blank=True, null=True, help_text='coupon name')
    coupon_code = models.CharField(max_length=10, blank=True, null=True, unique=True, help_text='coupon code')
    allowed_above = models.PositiveIntegerField(help_text='coupon is allowed above the price of')
    start_on = models.DateField(help_text='coupon start date')
    expire_on = models.DateField(help_text='coupon end date')
    discount = models.DecimalField(help_text='please enter discount percentage %', max_digits=3, decimal_places=0,
                                   default=decimal.Decimal(0), validators=PERCENTAGE_VALIDATOR)
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.coupon_name

    def is_expired(self):
        return self.expire_on <= datetime.date.today()


class Tag(models.Model):
    tag_name = models.CharField(max_length=200, null=True, unique=True)

    def __str__(self):
        return self.tag_name


class Product(models.Model):
    shopkeeper = models.ForeignKey(Shopkeeper, on_delete=models.CASCADE, blank=True, null=True)
    product_name = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.CharField(max_length=300, blank=True, null=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    available = models.BooleanField(default=True, null=True, blank=True)
    image = models.ImageField(default='placeholder.png', null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ('date_added', 'product_name')

    def __str__(self):
        return self.product_name


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def getTotal(self):
        total = self.quantity * self.product.price
        return total

    def __str__(self):
        return str(self.id)

import django.forms as forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

from .models import *


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(label='Enter password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password',
                                widget=forms.PasswordInput)

    group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   initial=0, label='Are you a')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'group')
        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
            'group': None,
        }

    def save(self, commit=True):
        instance = super().save(commit=commit)
        if commit:
            instance.groups.add(self.cleaned_data['group'])

        group = self.cleaned_data['group'].name

        if group == 'customer':
            Customer.objects.create(user=instance, name=instance.username)
        elif group == 'shopkeeper':
            Shopkeeper.objects.create(user=instance, name=instance.username)

        return instance


class productAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ['shopkeeper']


class createTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'


class customerSettingForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        exclude = ['user']


class shopkeeperSettingForm(forms.ModelForm):
    class Meta:
        model = Shopkeeper
        fields = "__all__"
        exclude = ['user']


class addressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        exclude = ['date', 'content_type', 'object_id']


class DateInput(forms.DateInput):
    input_type = 'date'


class createCoupon(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = '__all__'
        exclude = ['creator_name', 'created_for']
        widgets = {
            'start_on': DateInput(),
            'expire_on': DateInput()
        }

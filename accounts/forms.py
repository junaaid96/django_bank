# here we use UserCreationForm to create a form for user registration. if we use ModelForm then we have to write 3 ModelForm for 3 models which is in models.py file. so we make a relationship to built in user model along with extra data(extending the built-in user model, which is a common approach in Django for adding custom fields to the user model.) so that only usercreationform is enough to create a form for user registration.

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django_bank.constants import ACCOUNT_TYPE, GENDER_TYPE
from django.contrib.auth.models import User
from .models import UserBankAccount, UserAddress


class UserRegistrationForm(UserCreationForm):
    # Here the first 3 fields are in built in user model. so we don't need to write them again. but for required=True we have to write them again.
    first_name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={'required': True}))
    last_name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={'required': True}))
    email = forms.EmailField(
        max_length=100, widget=forms.TextInput(attrs={'required': True}))

    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'account_type',
                  'gender', 'birth_date', 'street_address', 'city', 'postal_code', 'country']

    def save(self, commit=True):
        customer = super().save(commit=False)
        if commit == True:
            customer.save()  # we save data to user model

            account_type = self.cleaned_data.get('account_type')
            gender = self.cleaned_data.get('gender')
            birth_date = self.cleaned_data.get('birth_date')
            street_address = self.cleaned_data.get('street_address')
            city = self.cleaned_data.get('city')
            postal_code = self.cleaned_data.get('postal_code')
            country = self.cleaned_data.get('country')

            UserAddress.objects.create(
                user=customer,
                street_address=street_address,
                city=city,
                postal_code=postal_code,
                country=country
            )

            UserBankAccount.objects.create(
                user=customer,
                account_no=2024000 + customer.id,
                account_type=account_type,
                gender=gender,
                birth_date=birth_date
            )

            return customer

    # Here we use the init method to add a class attribute to all fields for styling. We can also use the django-widget-tweaks package to add or modify HTML attributes and CSS classes of the fields in the template. The init method is a special method that is automatically invoked when an object is created from a class. It allows the class to initialize the attributes of the object. That means it sets the initial state of the object that is created from the class.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # here add class to all fields for styling
        for field in self.fields:
            # self.fields[field].widget.attrs['required'] = True
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })

# update user profile


class UserUpdateForm(forms.ModelForm):
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })

        # here we use initial method to set initial value of the fields
        if self.instance:
            try:
                user_account = self.instance.account
                user_address = self.instance.address
            except UserBankAccount.DoesNotExist:
                user_account = None
                user_address = None

            if user_account:
                self.fields['account_type'].initial = user_account.account_type
                self.fields['gender'].initial = user_account.gender
                self.fields['birth_date'].initial = user_account.birth_date
                self.fields['street_address'].initial = user_address.street_address
                self.fields['city'].initial = user_address.city
                self.fields['postal_code'].initial = user_address.postal_code
                self.fields['country'].initial = user_address.country

    def save(self, commit=True):
        customer = super().save(commit=False)
        if commit == True:
            customer.save()

            # get_or_create() method returns a tuple of (object, created), where object is the retrieved or created object and created is a boolean specifying whether a new object was created.
            user_account, created = UserBankAccount.objects.get_or_create(
                user=customer)
            user_address, created = UserAddress.objects.get_or_create(
                user=customer)

            user_account.account_type = self.cleaned_data['account_type']
            user_account.gender = self.cleaned_data['gender']
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.save()

            user_address.street_address = self.cleaned_data['street_address']
            user_address.city = self.cleaned_data['city']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.country = self.cleaned_data['country']
            user_address.save()

        return customer

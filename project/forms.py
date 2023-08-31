from django import forms
from project.models import Product, Comment, PaymentMethod


class ContactForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100)
    email = forms.EmailField(label="Email", max_length=100)
    message = forms.CharField(label="Message", widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class RegisterForm(forms.Form):
    first_name = forms.CharField(label="Name", max_length=100)
    last_name = forms.CharField(label="Lastname", max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label="Email", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    city = forms.CharField(label='City', max_length=100)
    address = forms.CharField(label='The address of your residence', max_length=100)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            if not isinstance(field.field.widget, forms.RadioSelect):
                field.field.widget.attrs["class"] = "form-control"


class PersonalInfoForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100)
    surname = forms.CharField(label="Lastname", max_length=100)
    email = forms.EmailField(label="Email", max_length=100)
    address = forms.CharField(label='The address of your residence', max_length=100)
    city = forms.CharField(label='City', max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(PersonalInfoForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ("seller", "is_approved",)
        labels = {
            'category': 'Category',
            'image': 'Image of the product',
            'name': 'Name of the product',
            'stock': 'Stock',
            'price': 'Price',
            'description': 'Description of our product',
        }

    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ("author", "date_created", "product",)

    def __init__(self, *args, **kwargs):
        super(AddCommentForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            if not isinstance(field.field.widget, forms.RadioSelect):
                field.field.widget.attrs["class"] = "form-control"


class SelectPaymentMethodForm(forms.ModelForm):
    expiry_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = PaymentMethod
        fields = '__all__'
        exclude = ("buyer",)

    def __init__(self, *args, **kwargs):
        super(SelectPaymentMethodForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            if not isinstance(field.field.widget, forms.RadioSelect):
                field.field.widget.attrs["class"] = "form-control"

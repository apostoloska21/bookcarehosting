from django.contrib.auth import get_user_model, logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from project.models import Category, Product, Comment, PaymentMethod, Role, Cart, CartItem, Order, \
    CustomUser, \
    OrderItem
from django.views.decorators.http import require_POST
from project.forms import ContactForm, LoginForm, RegisterForm, PersonalInfoForm, AddProductForm, AddCommentForm, \
    SelectPaymentMethodForm


# Create your views here.
def HomePage(request):
    return render(request, "home.html")


def Products(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    products = Product.objects.filter(category__name=selected_category) if selected_category else Product.objects.all()

    customuser = None
    if request.user.is_authenticated:
        customuser = CustomUser.objects.filter(user=request.user).first()

    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'customuser': customuser
    }
    return render(request, "products.html", context=context)


def Contact(request):
    contact_form = ContactForm
    context = {'form': contact_form}
    return render(request, "contactus.html", context=context)


def AboutUs(request):
    return render(request, "aboutus.html")


def Login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                login_form = LoginForm
                context = {'error': 'Wrong username or password', 'form': login_form}
                return render(request, 'login.html', context=context)

        login_form = LoginForm
        context = {"form": login_form}
        return render(request, "login.html", context=context)
    else:
        return redirect('/')


def Logout(request):
    logout(request)
    return redirect('/')


def Register(request):
    roles = Role.objects.all()
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                city = form.cleaned_data['city']
                role_name = request.POST['role']
                role = get_object_or_404(Role, role=role_name)
                address = form.cleaned_data['address']
                username = form.cleaned_data['username']

                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username is already taken.')
                    return render(request, "register.html", {'form': form, 'roles': roles, 'username_taken': True})

                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email, password=password)
                cuser = CustomUser.objects.create(user=user, city=city, address=address, role=role)
                return redirect('/')
        else:
            form = RegisterForm()
        return render(request, "register.html", {'form': form, 'roles': roles, 'username_taken': False})
    else:
        return redirect('/')


@login_required
def StartPage(request):
    return render(request, 'start.html')


def PersonalInfo(request):
    personal_info_form = PersonalInfoForm
    context = {'form': personal_info_form}
    return render(request, "personalinfo.html", context=context)


@login_required
def SuccessfullyAddedProduct(request):
    if request.user.customuser.role.role != 'Seller':
        raise Http404

    return render(request, "ProductSentToAdminTeam.html")


def DetailProductInfo(request, id):
    product = Product.objects.get(id=id)
    categories = Product.objects.all()
    comments = Comment.objects.filter(product=product)
    context = {'product': product, 'comments': comments, 'categories': categories}
    return render(request, "detailview.html", context=context)


@login_required
def AddComment(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        commentForm = AddCommentForm(request.POST)
        if commentForm.is_valid():
            comment = commentForm.save(commit=False)
            comment.author = request.user
            comment.product = product
            comment.save()
            return redirect('detailproductinfo', id=id)
    else:
        commentForm = AddCommentForm()
    context = {'form': commentForm, 'product': product}
    return render(request, "addComment.html", context=context)


@login_required
def PaymentSuccessful(request):
    if request.user.customuser.role.role != 'Buyer':
        raise Http404

    return render(request, "paymentSuccess.html")


@login_required
def SelectPaymentMethod(request):
    cart_items = []
    total_price = 0
    cart = None

    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = cart.total_price
    except Cart.DoesNotExist:
        pass

    if request.user.customuser.role.role != 'Buyer':
        raise Http404

    if request.method == 'POST':
        paymentMethodForm = SelectPaymentMethodForm(request.POST)
        if paymentMethodForm.is_valid():
            selected_payment_method = paymentMethodForm.save(commit=False)
            selected_payment_method.buyer = request.user
            selected_payment_method.save()

            if cart:
                return redirect('selectpaymentmethod')

    else:
        paymentMethodForm = SelectPaymentMethodForm()

    payment_methods = PaymentMethod.objects.filter(buyer=request.user)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': paymentMethodForm,
        'payment_methods': payment_methods,
    }
    return render(request, "paymentMethodSelect.html", context=context)


def PersonalInfo(request, username):
    user = User.objects.get(username=username)
    customerUser = CustomUser.objects.get(user=user)
    context = {'user': user, 'cuser': customerUser}
    return render(request, "personalinfo.html", context=context)


@login_required
def increase_quantity(request, item_id):
    item = CartItem.objects.get(id=item_id)

    if item.cart.user != request.user and request.user.customuser.role.role != 'Buyer':
        raise Http404

    item.quantity += 1
    item.save()
    return redirect('view_cart')


@login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)

    if item.cart.user != request.user and request.user.customuser.role.role != 'Buyer':
        raise Http404

    if item.quantity > 1:
        item.quantity -= 1
        item.save()

    return redirect('view_cart')


@login_required
def update_user_info(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        if username and username != user.username:
            raise Http404

        edited_user = CustomUser.objects.filter(user=user).first()
        if not edited_user:
            raise Http404

        first_name = request.POST.get('name')
        last_name = request.POST.get('surname')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        new_password = request.POST.get('pass')

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        edited_user.address = address
        edited_user.city = city
        edited_user.save()

        if new_password:
            user.set_password(new_password)
            user.save()

            logout(request)
            return redirect('login')

        return redirect('personalinfo', username=user.username)

    custom_user = None
    if hasattr(request.user, 'customuser'):
        custom_user = request.user.customuser
    return render(request, 'personalinfo.html', {'user': request.user, 'cuser': custom_user})


@login_required
def update_profile_image(request, username):
    user = request.user

    if user.username != username:
        raise Http404

    if request.method == 'POST' and request.FILES.get('profile_image'):
        profile_image = request.FILES['profile_image']
        custom_user = get_object_or_404(CustomUser, user=user)
        custom_user.profile_image = profile_image
        custom_user.save()

    return redirect('personalinfo', username=username)


@login_required
def my_products(request):
    custom_user = CustomUser.objects.get(user=request.user)

    if not custom_user.role.role == 'Seller':
        raise Http404

    products = Product.objects.filter(seller=custom_user.user)

    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, "myProducts.html", context=context)


@login_required
def add_product(request):
    if request.user.customuser.role.role != 'Seller':
        raise Http404

    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            custom_user = request.user.customuser
            user_model = get_user_model()
            product.seller = user_model.objects.get(customuser=custom_user)
            form.save()
            return redirect('product_sent_to_admin')
    else:
        form = AddProductForm()

    context = {'form': form}
    return render(request, 'addproduct.html', context)


@login_required
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.user != product.seller and not request.user.is_superuser:
        raise Http404

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.stock = request.POST.get('stock')
        product.description = request.POST.get('desc')
        custom_user = request.user.customuser
        product.seller = custom_user.user
        product.save()
        return redirect('detailproductinfo', id=id)

    context = {'product': product}
    return render(request, 'editProduct.html', context=context)


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user != product.seller and not request.user.is_superuser:
        raise Http404

    if request.method == 'POST':
        product.delete()

        messages.success(request, 'Product deleted successfully.')

        return redirect('products')

    return redirect('products')


@login_required
def delete_my_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user != product.seller:
        raise Http404

    if request.method == 'POST':
        product.delete()

        messages.success(request, 'Product deleted successfully.')

        return redirect('myproducts')

    return redirect('products')


@login_required
def add_to_cart_view(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user

    if user.customuser.role.role != 'Buyer':
        raise Http404

    if product.stock < 1:
        messages.error(request, "No product stock available")
        return redirect('products')

    cart, created = Cart.objects.get_or_create(user=user, is_ordered=False)
    if not created and cart.user != user:
        raise Http404

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        if cart_item.product.stock > cart_item.quantity:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.error(request, "No product stock available")
            return redirect('products')

    return redirect('view_cart')


@login_required
def delete_item_cart(request, item_id):
    item = CartItem.objects.get(id=item_id)

    if item.cart.user != request.user:
        raise Http404

    item.delete()
    return redirect('view_cart')


@login_required
def view_cart(request):
    user = request.user

    if user.customuser.role.role != 'Buyer':
        raise Http404

    cart_items = []
    total_price = 0

    try:
        cart = Cart.objects.get(user=user)
        cart_items = cart.cartitem_set.all()
        total_price = cart.total_price
    except Cart.DoesNotExist:
        cart = None

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, "cart.html", context=context)


@login_required
def save_order(request):
    if request.method == 'POST':
        selected_payment_method_id = request.POST.get('payment_method')
        selected_payment_method = PaymentMethod.objects.get(id=selected_payment_method_id)

        user = request.user

        if user.customuser.role.role != 'Buyer':
            raise Http404

        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        order = Order.objects.create(user=user, payment_method=selected_payment_method)

        for cart_item in cart_items:
            if cart_item.product.stock < cart_item.quantity:
                messages.error(request, "Quantity exceeds available stock")
                order.delete()
                return redirect('view_cart')

            order_item = OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)

            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()

        cart.delete()

        return redirect('paymentsuccessful')

    return render(request, 'save_order.html')


@login_required
def order_list(request):
    user = request.user

    if user.customuser.role.role != 'Buyer':
        raise Http404

    orders = Order.objects.filter(user=user)
    context = {
        'orders': orders
    }
    return render(request, 'Orders.html', context=context)


@login_required
@require_POST
def update_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    user = request.user
    if user.customuser.role.role != 'Buyer' and not user.is_superuser and user != cart_item.product.seller:
        raise Http404

    quantity = int(request.POST.get('quantity', 1))
    cart_item.quantity = quantity
    cart_item.save()

    return redirect('view_cart')


@login_required()
def approve_product(request, product_id):
    user = request.user

    if not user.is_superuser:
        raise Http404

    product = get_object_or_404(Product, id=product_id)

    product.is_approved = True
    product.save()

    return redirect('non_approved_products')


@login_required
def non_approved_products(request):
    if not request.user.is_superuser:
        raise Http404

    products = Product.objects.filter(is_approved=False)
    pending_products_count = products.count()

    context = {
        'products': products,
        'pending_products_count': pending_products_count
    }
    return render(request, 'admin_approving.html', context=context)


@login_required()
def product_sent_to_admin(request):
    user = request.user

    if user.customuser.role.role != 'Seller':
        raise Http404

    return render(request, "ProductSentToAdminTeam.html")


@login_required
def edit_product_image(request, id):
    user = request.user

    product = get_object_or_404(Product, id=id)

    if not user.is_superuser:
        try:
            custom_user = user.customuser
            role = custom_user.role
        except (CustomUser.DoesNotExist, AttributeError):
            raise Http404

        if role is None or role.role == "Buyer":
            raise Http404

    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            product.image = image
            product.save()

    return redirect('detailproductinfo', id=id)

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from project.views import HomePage, Products, Contact, AboutUs, Login, Register, SuccessfullyAddedProduct, \
    DetailProductInfo, AddComment, PaymentSuccessful, SelectPaymentMethod, PersonalInfo, Logout, increase_quantity, \
    decrease_quantity, update_profile_image, update_user_info, my_products, add_product, edit_product, delete_product, \
    delete_my_product, add_to_cart_view, view_cart, delete_item_cart, save_order, order_list, update_quantity, \
    approve_product, non_approved_products, product_sent_to_admin, edit_product_image,StartPage

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', HomePage, name='home'),
                  path('products/', Products, name='products'),
                  path('contactus/', Contact, name='contactus'),
                  path('aboutus/', AboutUs, name='aboutus'),
                  path('register/', Register, name='register'),
                  path('login/', Login, name='login'),
                  path('start/', StartPage, name='start'),
                  path('logout/', Logout, name='logout'),
                  path('personalinfo/', PersonalInfo, name='personalinfo'),
                  path('products/add/success/', SuccessfullyAddedProduct, name='successfullyaddedproduct'),
                  path('products/<int:id>/', DetailProductInfo, name='detailproductinfo'),
                  path('products/<int:id>/comment/add/', AddComment, name='addcomment'),
                  path('payment/success/', PaymentSuccessful, name='paymentsuccessful'),
                  path('payment-method/', SelectPaymentMethod, name='selectpaymentmethod'),
                  path('users/<str:username>/details/', PersonalInfo, name='personalinfo'),
                  path('update_user_info/', update_user_info, name='update_user_info'),
                  path('users/<str:username>/details/update-profile-image/', update_profile_image,
                       name='update_profile_image'),
                  path('cart/<int:item_id>/increase_quantity/', increase_quantity, name='increase_quantity'),
                  path('cart/<int:item_id>/decrease_quantity/', decrease_quantity, name='decrease_quantity'),
                  path('myproducts/', my_products, name='myproducts'),
                  path('addproduct/', add_product, name='addproduct'),
                  path('product_sent_to_admin/', product_sent_to_admin, name='product_sent_to_admin'),
                  path('products/<int:id>/edit/', edit_product, name='editproduct'),
                  path('products/<int:pk>/delete_product/', delete_product, name='delete_product'),
                  path('products/<int:pk>/delete_my_product/', delete_my_product, name='delete_my_product'),
                  path('cart/add/<int:product_id>/', add_to_cart_view, name='add_to_cart'),
                  path('cart/', view_cart, name='view_cart'),
                  path('cart/<int:item_id>/delete/', delete_item_cart, name='delete_item_cart'),
                  path('saveorder/', save_order, name='saveorder'),
                  path('orders/', order_list, name='order_list'),
                  path('cart/<int:item_id>/update-quantity/', update_quantity, name='update_quantity'),
                  path('non-approved-products/', non_approved_products, name='non_approved_products'),
                  path('approving/<int:product_id>/', approve_product, name='approve_product'),
                  path('editproduct/<int:id>/image/', edit_product_image, name='edit_product_image'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.shortcuts import render,redirect
from .models import Product,Order
from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm,User
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login, logout,update_session_auth_hash

from django.views import View
def F1(request):
    return render(request,'main.html')

class Index(View):
    def post(self,request):
        if request.user.is_authenticated:
            product= request.POST.get('product')
            remove=request.POST.get('remove')
            cart = request.session.get('cart')
            if cart:
                quantity=cart.get(product)
                if quantity:
                    if remove:
                        if quantity<=1:
                            cart.pop(product)
                        else:
                            cart[product]=quantity-1

                    else:
                        cart[product] = quantity+1
                else:
                    cart[product]=1
            else:
                cart={}
                cart[product]=1

            request.session['cart']=cart
            print('cart',request.session['cart'])
            return redirect('/menu/')
        return redirect('/login/')


    def get(self,request):
            cart=request.session.get('cart')
            if not cart:
                request.session['cart']={}
            products = Product.get_all_products();
            data={}
            data['products']=products
            # data['categories']=categories
            print('You are :', request.session.get('user_id'))
            return render(request,'menu.html',data)




def F4(request):
    return render(request,'about.html')
def F5(request):
    return render(request,'service.html')
# def F6(request):
#     if request.method=="POST":
#         fm=user_feedback(request.POST)
#         if fm.is_valid():
#             fm.save()
#     else:
#         fm=user_feedback()
#     return render(request,'feedback.html',{'form':fm})

#signup
def sign_up(request):
    if request.method=='POST':
        fm=SignUpForm(request.POST)
        if fm.is_valid():
            fm.save()
        fm=SignUpForm()
    else:
        fm=SignUpForm()
    return render(request,'signup.html',{'form':fm})


#login page
def user_login(request):
    if request.method=='POST':
        fm=AuthenticationForm(request=request,data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user =authenticate(username=uname,password=upass)
            if user:
                login(request,user)
                request.session['user_id'] = user.id
                request.session['email'] = user.email
                return HttpResponseRedirect('/menu/')
    else:
        fm= AuthenticationForm()
        return render(request,'login.html',{'form':fm})




def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products= Product.get_products_by_id(ids)
        print(products)
        return render(request, 'cart.html', {'products':products})



class CheckOut(View):
    def post(self,request):
        address=request.POST.get('address')
        phone = request.POST.get('phone')
        user=request.session.get('user_id')
        cart=request.session.get('cart')
        products=Product.get_products_by_id(list(cart.keys()))
        print(address,phone,user,cart,products)

        for product in products:
            print(cart.get(str(product.id)))
            order=Order(user=User(id=user),product=product,price=product.price,address=address,phone=phone,quantity=cart.get(str(product.id)))

            order.placeOrder()
        request.session['cart'] = {}
        return redirect('cart')

class History(View):
    def get(self, request):
        user=request.session.get('user_id')
        history=Order.get_order_history_by_user(user)
        return render(request,'history.html',{'historys':history})

from django.urls import path
from .import views
from .views import Index,Cart,CheckOut,History

urlpatterns = [
    path('',views.F1,name='main'),
    path('menu/',Index.as_view(),name='menu'),
    path('about',views.F4),
    path('service',views.F5),
    # path('feedback/',views.F6),
    path('login/', views.user_login,name='login'),
    path('signup/', views.sign_up,name='signup'),
    path('logout/', views.user_logout,name='logout'),
    path('cart/',Cart.as_view(),name='cart'),
    path('check-out',CheckOut.as_view(),name='checkout'),
    path('history', History.as_view(), name='history'),


]

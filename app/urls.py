from django.urls import path 
from . import views


urlpatterns = [
    path("",views.Home.as_view(),name = "home"),
    path("list/",views.List.as_view(),name = "list"),
    path("detail/<slug>/",views.Detail.as_view(),name = "detail"),
    path("additem/<slug>",views.addItem,name = "additem"),
    path("order/",views.OrderView.as_view(),name = "order"),
    path("removeitem/<slug>",views.removeItem,name = "removeitem"),
    path("decreaseitem/<slug>",views.decreaseItem,name = "decreaseitem"),
    path("payment/",views.Payment.as_view(),name = "payment"),
    path("thanks/",views.Thanks.as_view(),name = "thanks")
]
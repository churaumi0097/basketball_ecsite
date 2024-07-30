from django.shortcuts import render,get_object_or_404, redirect
from django.views.generic import View,TemplateView,ListView, DetailView
from .models import Post,Order,OrderItem,Payment
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

CustomUser = get_user_model() 


class Home(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "home.html"


class List(LoginRequiredMixin,ListView):
    model = Post
    context_object_name = "posts"
    template_name = "list.html"

    def get_queryset(self):
        queryset = Post.objects.order_by("created")
        query = self.request.GET.get("query")

        if query:
            queryset = queryset.filter(
                Q(title__icontains = query) | Q(content__icontains = query) | Q(category__name__icontains = query)
            )
        messages.add_message(self.request, messages.INFO, query)
        return queryset


class Detail(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "detail.html"


def addItem(request,slug):
    post = get_object_or_404(Post,slug = slug)
    order_item,created = OrderItem.objects.get_or_create(
        post = post,
        user = request.user,
        ordered = False
    )
    order = Order.objects.filter(user = request.user ,ordered = False)
    
    if order.exists():
        order = order[0]
        if order.posts.filter(post__slug = post.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.posts.add(order_item)
    else:
        order = Order.objects.create(user = request.user,ordered_data = timezone.now())
        order.posts.add(order_item)

    return redirect("order")


class OrderView(View):
    def get(self,request,*args,**kwargs):
        try:
            order = Order.objects.get(user = self.request.user, ordered = False)
            context = {
                "order" : order
            }
            return render(request,"order.html",context)
        
        except ObjectDoesNotExist:
            return render(request,"order.html")


def removeItem(request,slug):
    post = get_object_or_404(Post,slug = slug)
    order = Order.objects.filter(user = request.user ,ordered = False)   
    if order.exists():
        order = order[0]
        if order.posts.filter(post__slug = post.slug).exists():
            order_post = OrderItem.objects.filter(
                post = post,
                user = request.user,
                ordered = False
            )[0]
            order.posts.remove(order_post)
            order_post.delete()
            return redirect("order")
    return redirect("list",slug = slug)


def decreaseItem(request,slug):
    post = get_object_or_404(Post,slug = slug)
    order = Order.objects.filter(user = request.user ,ordered = False)
    
    if order.exists():
        order = order[0]
        if order.posts.filter(post__slug = post.slug).exists():
            order_post = OrderItem.objects.filter(
                post = post,
                user = request.user,
                ordered = False
            )[0]
            if order_post.quantity > 1:
                order_post.quantity -= 1
                order_post.save()
        else:
            order.posts.remove(order_post)
            order_post.delete()
        return redirect("order")
    return redirect("list",slug = slug)


class Payment(TemplateView):
    template_name = "payment.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.get(user = self.request.user,ordered = False)
        user_data = CustomUser.objects.get(id = self.request.user.id)
        context["order"] = order
        context["user_data"] = user_data
        return context

    def post(self,request,*args,**kwargs):
        order = Order.objects.get(user = request.user,ordered = False)
        order_posts = order.posts.all()
        amount = order.total_price()

        payment = Payment(user = request.user)
        payment.charge_id = "charge_id"
        payment.amount = amount
        payment.save()

        order_posts.update(ordered = True)
        for post in order_posts:
            post.save()
        
        order.ordered = True
        order.payment = payment
        order.save()
        return redirect("thanks")


class Thanks(TemplateView):
    template_name = "thanks.html"
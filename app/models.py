from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="名前",
    )
    image = models.ImageField(
        verbose_name="画像",
        upload_to = "image"
    )

    def __str__(self):
        return self.name
        

class Post(models.Model):
    title = models.CharField(
        verbose_name="商品名",
        max_length=250
    )
    content = models.TextField(
        verbose_name="商品説明"
    )
    image = models.ImageField(
        verbose_name="商品説明",
        upload_to = "image"
    )
    slug = models.SlugField()

    price = models.PositiveIntegerField(
        verbose_name="値段"
    )
    category = models.ForeignKey(
        Category,
        verbose_name="カテゴリー",
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    created = models.DateTimeField(
        verbose_name="投稿日時",
        auto_now_add=True,
        editable=False
    )

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete = models.CASCADE
    )
    ordered = models.BooleanField(
        default = False
    )
    post = models.ForeignKey(
        Post,
        on_delete = models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        default = 1
    )

    def sub_total(self):
        return self.post.price * self.quantity

    def __str__(self):
        return self.post.title

class Order(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete = models.CASCADE
    )
    posts = models.ManyToManyField(
        OrderItem
    )
    ordered_data = models.DateTimeField(
        auto_now_add = True
    )
    ordered = models.BooleanField(
        default = False
    )

    def total_price(self):
        total = 0
        for price in self.posts.all():
            total += price.sub_total() 
        return total

    def __str__(self):
        return self.user.email


class Payment(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete = models.CASCADE,
        blank = True,
        null = True
    )
    charge_id = models.CharField(
        max_length = 50
    )
    amount = models.PositiveIntegerField(
    )
    timestamp = models.DateTimeField(
        auto_now_add = True
    )

    def __str__(self):
        return self.user.email
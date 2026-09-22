from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

STATUS_CHOICES = (
('gold', 'gold'),
('silver', 'silver'),
('bronze', 'bronze'),
('simple', 'simple'),
)

class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(16),
                                                       MaxValueValidator(90)],
                                           null=True,  blank=True)
    phone_number = PhoneNumberField(default='+996')
    avatar = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='simple')

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)
    category_image = models.ImageField(upload_to='category_images')

    def  __str__(self) -> str:
        return self.category_name

class SubCategory(models.Model):
    category =models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_sub')
    subcategory_name = models.CharField(max_length=64)
    subcategory_image = models.ImageField(upload_to='subcategory_image')

    def __str__(self) -> str:
        return f'{self.category.category_name} - {self.subcategory_name}'

class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='sub_product')
    product_name = models.CharField(max_length=255)
    price  = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    article_number = models.PositiveSmallIntegerField(unique=True)
    product_type = models.BooleanField(default=True)
    video = models.FileField(upload_to='product_videos/', null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    def  get_avg_people(self):
        ratings = [review.stars for review in self.product_review.all() if review.stars is not None]
        if not ratings:
           return 0
        return round(sum(ratings) / len(ratings), 1)

    def get_count_people(self):
        return self.product_review.count()



    def __str__(self) -> str:
        return f'{self.subcategory.subcategory_name} - {self.product_name}'

class ProductImage(models.Model):
    product =  models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_img')
    product_image = models.ImageField(upload_to='product_images/')


class Review(models.Model):
  user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_review')
  stars = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
  comment = models.TextField(null=True, blank=True)
  review_image = models.ImageField(upload_to='review_images/', null=True, blank=True)
  created_time = models.DateTimeField(auto_now_add=True)

  def __str__(self) -> str:
     return f'{self.user.username} - comment'



class Cart(models.Model):
      user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

      def get_total_price(self):
          return sum([i.get_total_price() for i in self.item.all()])

class CartItem(models.Model):
      cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='item')
      product = models.ForeignKey(Product, on_delete=models.CASCADE)
      quantity = models.PositiveSmallIntegerField(default=1)

      def get_total_price(self):
          return self.quantity * self.product.price

class Favorite(models.Model):
      user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

class FavoriteItem(models.Model):
      favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE, related_name='favorite_item')
      product = models.ForeignKey(Product, on_delete=models.CASCADE)
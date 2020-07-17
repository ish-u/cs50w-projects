from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topping(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

class Pizza(models.Model):
    type_choice = [
        ("Regular","Regular"),
        ("Sicilian","Sicilian")
    ]
    pizza_type = models.CharField(max_length=10,choices=type_choice,default="Regular")
    size_choice = [
        ("Large","Large"),
        ("Small","Small")
    ]
    size = models.CharField(max_length=5,choices=size_choice,default="Small")
    no_of_toppings = models.IntegerField(default=0)
    special = models.BooleanField(default=False)
    price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.id}. {self.pizza_type}-{self.size}-{self.no_of_toppings}"

class Subs(models.Model):
    name = models.CharField(max_length=50)
    size_choice = [
        ("Large","Large"),
        ("Small","Small")
    ]
    size = models.CharField(max_length=5,choices=size_choice,default="Small")
    price = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = 'Subs'

    def __str__(self):
        return f"{self.id}. {self.name}-{self.size}"

class Pasta(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.id}. {self.name}"

class Salad(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.id}. {self.name}"

class Dinner_Platter(models.Model):
    name = models.CharField(max_length=50)
    size_choice = [
        ("Large","Large"),
        ("Small","Small")
    ]
    size = models.CharField(max_length=5,choices=size_choice,default="Small")
    price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.id}. {self.name}-{self.size}"

class Pasta_Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Pasta = models.ForeignKey(Pasta, on_delete=models.CASCADE)
    Price = models.IntegerField(default=0)
    ordered = models.BooleanField(default=0)
    
    def __str__(self):
        return f"{self.Pasta.name} - {self.user}"

class Salad_Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Salad = models.ForeignKey(Salad, on_delete=models.CASCADE)
    Price = models.IntegerField(default=0)
    ordered = models.BooleanField(default=0)
    def __str__(self):
        return f"{self.Salad.name} - {self.user}"

class Platter_Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Platter = models.ForeignKey(Dinner_Platter,on_delete=models.CASCADE)
    Price = models.IntegerField(default=0)
    ordered = models.BooleanField(default=0)

    def __str__(self):
        return f"{self.Platter.name} - {self.user} "  

class Pizza_Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Pizza = models.ForeignKey(Pizza,on_delete=models.CASCADE)
    Toppings = models.ManyToManyField(Topping, blank = True)
    Price = models.FloatField(default=0)
    ordered = models.BooleanField(default=0)
    
    def __str__(self):
        return f"{self.Pizza.pizza_type} - {self.Pizza.size} - {self.user}"

class Subs_Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Subs = models.ForeignKey(Subs,on_delete=models.CASCADE)
    extra_cheese = models.BooleanField(default=False)
    Toppings = models.ManyToManyField(Topping, blank = True)
    Price = models.FloatField(default=0)
    ordered = models.BooleanField(default=0)
    
    def __str__(self):
        return f"{self.id}. {self.Subs.name} - {self.Subs.size}  - {self.user}"

class order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Pizza = models.ManyToManyField(Pizza_Order,blank=True)
    Subs = models.ManyToManyField(Subs_Order,blank=True)
    Pasta = models.ManyToManyField(Pasta_Order,blank=True)
    Salad = models.ManyToManyField(Salad_Order,blank=True)
    Platter = models.ManyToManyField(Platter_Order,blank=True)
    Price = models.FloatField(default=0)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.user.username}] Order No ->{self.id}"
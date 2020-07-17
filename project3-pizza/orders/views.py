from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import *
from django.urls import reverse
from django.db.models import Max, Sum
from random import choice

@login_required
def index(request):
    context = {
        "size":Pizza.objects.values('size').distinct(),
        "pizza_type":Pizza.objects.values('pizza_type').distinct(),
        "max_topping_pizza":Pizza.objects.filter(special=False).aggregate(Max("no_of_toppings")),
        "topping":Topping.objects.all(),
        "sub_name":Subs.objects.values('name').distinct(),
        "pasta_name":Pasta.objects.values('name').distinct(),
        "salad_name":Salad.objects.values('name').distinct(),
        "platter_name":Dinner_Platter.objects.values('name').distinct(),
    }
    return render(request,"order/index.html",context)

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        form = UserRegisterForm()
    return render(request,"users/register.html",{'form':form})

@login_required
def cart(request):
    if request.method == "GET":
        all_price = []
        all_price.append(Pizza_Order.objects.filter(user = request.user, ordered = False).aggregate(Sum('Price'))['Price__sum'])
        all_price.append(Subs_Order.objects.filter(user = request.user, ordered = False).aggregate(Sum('Price'))['Price__sum'])
        all_price.append(Pasta_Order.objects.filter(user = request.user, ordered = False).aggregate(Sum('Price'))['Price__sum'])
        all_price.append(Salad_Order.objects.filter(user = request.user, ordered = False).aggregate(Sum('Price'))['Price__sum'])
        all_price.append(Platter_Order.objects.filter(user = request.user, ordered = False).aggregate(Sum('Price'))['Price__sum'])
        price = 0
        for p in all_price:
            if p:
                price = price + p
        context = {
            "pizza_order":Pizza_Order.objects.filter(user = request.user),
            "sub_order":Subs_Order.objects.filter(user = request.user),
            "pasta_order":Pasta_Order.objects.filter(user = request.user),
            "salad_order":Salad_Order.objects.filter(user = request.user),
            "platter_order":Platter_Order.objects.filter(user = request.user),
            "orders":order.objects.filter(user = request.user),
            "subtotal":price,
        }
        return render(request,"order/cart.html",context)

#Order View
@login_required
def Order(request):
    if request.method == "POST":
        pizza = Pizza_Order.objects.filter(user=request.user, ordered=False)
        subs = Subs_Order.objects.filter(user=request.user, ordered=False)
        pasta = Pasta_Order.objects.filter(user=request.user, ordered=False)
        salad = Salad_Order.objects.filter(user=request.user, ordered=False)
        platter = Platter_Order.objects.filter(user=request.user, ordered=False)
        o = order(user=request.user)
        price = 0
        o.save()
        for i in pizza:
            i.ordered = True
            i.save()
            price = price + i.Price
            o.Pizza.add(i)
        for i in subs:
            i.ordered = True
            i.save()
            price = price + i.Price
            o.Subs.add(i)
        for i in pasta:
            i.ordered = True
            i.save()
            price = price + i.Price
            o.Pasta.add(i)
        for i in salad:
            i.ordered = True
            i.save()
            price = price + i.Price
            o.Salad.add(i)
        for i in platter:
            i.ordered = True
            i.save()
            price = price + i.Price
            o.Platter.add(i)
        o.Price = price
        o.save()
        return HttpResponseRedirect(reverse('cart'))

#Pizza Order
@login_required
def pizza_order(request):
    if request.method == "POST":
        if 'price' in request.POST:
            price = Pizza.objects.filter(pizza_type=request.POST["type"],size=request.POST["size"],no_of_toppings=request.POST["topping"])
            if not price.exists():
                return JsonResponse({"price":"0"})
            else:
                return JsonResponse({"price":price[0].price})
        else:
            topping = request.POST.getlist('topping')
            try:
                pizza = Pizza.objects.filter(pizza_type=request.POST["pizza_type"],size=request.POST["pizza_size"],no_of_toppings=len(topping))[0]
                order = Pizza_Order(user = request.user, Pizza = pizza, Price = pizza.price)
                order.save()
                for t in topping:
                    order.Toppings.add(Topping.objects.get(pk=t))
                order.save()
                return HttpResponseRedirect(reverse('index'))
            except KeyError:
                return HttpResponse(504)
#Sub Order
@login_required
def sub_order(request):
    if request.method == "POST":
        if 'price' in request.POST:
            price = Subs.objects.filter(name=request.POST["name"],size=request.POST["size"])
            if not price.exists():
                return JsonResponse({"price":"0"})
            else:
                return JsonResponse({"price":price[0].price})
        else:
            try:
                topping = request.POST.getlist('sub_topping')
                sub = Subs.objects.filter(name=request.POST["sub_name"],size = request.POST["sub_size"])[0]
                if request.POST["extra_cheese"]:
                    price = sub.price + 0.5
                    cheese = True
                else:
                    price = sub.price
                    cheese = False
                order = Subs_Order(user = request.user, Subs = sub, Price = price, extra_cheese=cheese)
                order.save()
                for t in topping:
                    order.Toppings.add(Topping.objects.get(pk=t))
                order.save()
                return HttpResponseRedirect(reverse('index'))
            except KeyError:
                return HttpResponse(504)

#Pasta Order
@login_required
def pasta_order(request):
    if request.method == "POST":
        if 'price' in request.POST:
            price = Pasta.objects.filter(name=request.POST["name"])
            if not price.exists():
                return JsonResponse({"price":"0"})
            else:
                return JsonResponse({"price":price[0].price})
        else:
            try:
                pasta = Pasta.objects.filter(name=request.POST["pasta_name"])[0]
                order = Pasta_Order(user = request.user, Pasta = pasta, Price = pasta.price)
                order.save()
                return HttpResponseRedirect(reverse('index'))
            except KeyError:
                return HttpResponse(504)
#Salad Order
@login_required
def salad_order(request):
    if request.method == "POST":
        if 'price' in request.POST:
            price = Salad.objects.filter(name=request.POST["name"])
            if not price.exists():
                    return JsonResponse({"price":"0"})
            else:
                return JsonResponse({"price":price[0].price})
        else:
            try:
                salad = Salad.objects.filter(name=request.POST["salad_name"])[0]
                order = Salad_Order(user = request.user, Salad = salad, Price = salad.price)
                order.save()
                return HttpResponseRedirect(reverse('index'))
            except KeyError:
                return HttpResponse(504)
#Diner Platter
@login_required
def platter_order(request):
    if request.method == "POST":
        if 'price' in request.POST:
            price = Dinner_Platter.objects.filter(name=request.POST["platter_name"],size=request.POST["size"])
            if not price.exists():
                    return JsonResponse({"price":"0"})
            else:
                return JsonResponse({"price":price[0].price})
        else:
            try:
                platter = Dinner_Platter.objects.filter(name=request.POST["platter_name"],size=request.POST["platter_size"])[0]
                order = Platter_Order(user = request.user, Platter = platter, Price = platter.price)
                order.save()
                return HttpResponseRedirect(reverse('index'))
            except KeyError:
                return HttpResponse(504)
        
#Special Pizza Order
def special(request):
    if request.method == "POST":
        if 'price' in request.POST:
            price = Pizza.objects.filter(special=1, pizza_type=request.POST["type"], size=request.POST["size"])
            print(price)
            if not price.exists():
                return JsonResponse({"price":0})
            else:
                return JsonResponse({"price":price[0].price})
        else:
            try:
                pizza = Pizza.objects.filter(pizza_type=request.POST["special_crust"], size=request.POST["special_size"], special=True)[0]
                topping_list = Topping.objects.values_list("pk", flat=True)
                toppings = []
                while(len(toppings) != 5):
                    topping = Topping.objects.filter(pk=choice(topping_list))[0]
                    if topping not in toppings:
                        toppings.append(topping)
                order = Pizza_Order(user = request.user, Pizza = pizza, Price = pizza.price)
                order.save()
                for topping in toppings:
                    order.Toppings.add(topping)
                order.save()
                return HttpResponseRedirect(reverse('index'))
            except KeyError:
                return HttpResponse(504)

#delete menu items route
@login_required
def delete_pizza(request):
    if request.method == "POST":
        try:
            pizza = Pizza_Order.objects.filter(pk=request.POST["id"])[0]
            pizza.delete()
            return HttpResponseRedirect(reverse('cart'))
        except:
            return HttpResponse(504)

@login_required
def delete_sub(request):
    if request.method == "POST":
        try:
            sub = Subs_Order.objects.filter(pk=request.POST["id"])[0]
            sub.delete()
            return HttpResponseRedirect(reverse('cart'))
        except KeyError:
            return HttpResponse(504)

@login_required
def delete_pasta(request):
    if request.method == "POST":
        try:
            pasta = Pasta_Order.objects.filter(pk=request.POST["id"])[0]
            pasta.delete()
            return HttpResponseRedirect(reverse('cart'))
        except:
            return HttpResponse(504)

@login_required
def delete_salad(request):
    if request.method == "POST":
        try:
            salad = Salad_Order.objects.filter(pk=request.POST["id"])[0]
            salad.delete()
            return HttpResponseRedirect(reverse('cart'))
        except:
            return HttpResponse(504)

@login_required
def delete_platter(request):
    if request.method == "POST":
        try:
            platter = Platter_Order.objects.filter(pk=request.POST["id"])[0]
            platter.delete()
            return HttpResponseRedirect(reverse('cart'))
        except:
            return HttpResponse(504)

@staff_member_required
def order_complete(request):
    if request.method == "GET":
        context = {
            "orders":order.objects.filter(status = False)
        }
        return render(request,"order/orders.html",context)
    elif request.method == "POST":
        try:
            o = order.objects.filter(pk=request.POST["id"])[0]
            o.status = True
            o.save()
            return HttpResponse(200)
        except KeyError:
            return HttpResponse(504)




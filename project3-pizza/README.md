# Project 3

Web Programming with Python and JavaScript. This is Pizza.

## <ins>orders/models.py</ins>
This file contains all the models that represent the menu of "Pinocchio's Pizza & Subs" :-
 ||||
-----------| -----------| ----------- 
Topping | Pizza |  Subs
Pasta | Salad | Dinner Platter
Pizza_Order | Subs_Order | Pasta_Order
Salad_Order | Platter_Order | order

## <ins>orders/urls.py</ins>
This file contains all the urls of the web-app:-
 ||||
-----------| -----------| ----------- 
"" | "register/" | "cart/"
"pizza_order" | "sub_order/" | "pasta_order/"
"salad_order/" | "platter_order/" | "special/"
"cart/delete_pizza/" | "cart/delete_sub/" | "cart/delete_pasta/"
"cart/delete_salad/" | "cart/delete_platter/" | "order_coplete/"


## <ins>orders/views.py</ins> 
This file contains all the views that are associated with a respective route.
1. **index** :- This view is linked to url "". It renders "template/order/index.html".
2. **register** :- This view is linked to "register/" url. This view creates a django form object which is used for user registeration. It renders "templates/users/register.html". The view renders an empty form for "GET" request. The view validates and saves(register) a user in the "django user model" for "POST" request.
3. **cart** :- This view is linked to "cart/" url. It renders "templates/order/cart.html" This view calculates the "price(subtotal)" of all items in the "user cart" and sends the all the objects from *Pizza_Order, Sub_Order, Pasta_Order, Salad_Order, Platter_Order, order"* models asociated with logged-in user to the "cart/" url.
4. **Order**: This view is linked with "order/" url. It creates a object of "order" model and saves the all the objects of *Pizza_Order, Sub_Order, Pasta_Order, Salad_Order, Platter_Order* models that are associated with the current logged-in user. TLDR; It saves an order of the user. It then redirects the user to "cart/" url.
5. **Add To Cart Views** :-
     view | model | url
    -----------| -----------| -----------
     pizza_order | Pizza_Order | "pizza_order/"
     sub_order | Subs_Order | "sub_order/"
     pasta_order | Pasta_Order | "pasta_order/"
     salad_order | Salad_Order | "salad_order/"
     platter_order | Platter_Order | "platter_order/"
     special | Pizza_Order | "pizza_order/"

    These views add an object to model associated with them and then redirect to "" url (index page). If the request object has 'price' attribute these views returns a JSON object containing 'price' key. This JSON object is used to display Price of a menu item in the index page.
6. **Remove From Cart Views** :-
     view | model | url
    -----------| -----------| -----------
     delete_pizza | Pizza_Order | "cart/delete_pizza"
     delete_sub | Subs_Order | "cart/delete_sub"
     delete_salad | Salad_Order | "cart/delete_salad"
     delete_pasta | Pasta_Order | "cart/delte_pasta"
     delete_platter | Platter_Order| "cart/delete_plater"

    These views delete and object from the model associated with them and redirect to "cart/" url.
7. **order_complete** :- This view is linked to "order_complete/" url. If the request is "POST" the view querys for an object came with <ins>id = request.POST["id"]</ins> and sets its "status" attribute to "True" and returns 200 as a HttpResponse.

## <ins>order/forms.py</ins> 
This file creates a Custom Form Class using django's UserFormCreation of ModalForm Class. This form is then used for registering the user.


## <ins>templates(folder)</ins>
* **layout/layout.hmtl**:- This file contains the layout of the web app. All the other pages in the web-app extends this file to generate this. This file acts as a layout for other files.
* **order/index.html**:- This file is the index page of the web-app. It extends "layout/layout.html". The page has 5 Forms for adding different items to cart. All these forms are located in 5 different Bootstrap Modals. The page displays 5 images that are wrapped around "a" tag which toggles a different model :-
    *   Form(id) | Modal(id) | Button that submits the Form(id)
        ----------- | ----------- | ------------|
        #pizza_form | #pizzaModal | #pizza_cart
        #sub_form | #subModal | #sub_cart
        #salad_form | #saladModal | #salad_cart
        #pasta_form | #pastaModal | #pasta_cart
        #platter_form | #platterModal | #platter_cart
* **order/cart.html**:- This page displays the user cart and current orders that the user has. It has a form "#order"(id) that orders all the menu-items that are currently in the cart. The menu items are represented in form of "cards" in the cart. Each of these "card" has a "cross button" associated with them that deletes the item from the cart. 
    *   Each of these "cross button" has a class associated.
        Menu Item | "Cross Button" Class 
        ----------- | ----------- | 
        Pizza | pizza_close
        Subs | sub_close
        Pasta | pasta_close
        Salad | salad_close
        Dinner Platter| platter_close
* **order/orders.html**:- This page is a ADMIN-only page. The page displays all the orders that the all users have made.  Orders are displayed in form of card with a "complete" button. The ADMIN can mark a order as "done" or "complete" using this page.

* **users/login.html**:- This page displays a form that logs in a user. The page uses **crispy-form app** of django to render form.

* **users/register.html**:- This page displays a form that registers a user. The page uses **crispy-form app** of django to render form.

## <ins>static(folder)</ins>
This folder contains all the static files for the web-app

* **price.js**:- This file is linked with "order/index.html" html file. This JS file has an event-listener for "DOMContentLoaded". This event has a call-back function that check for any changes that happens in the 5 Forms for ordering menu-items in "order/index.html". On change in any form a XMLHttpRequest() object is created and a request is sent to the server which returns the price of a menu item as a JSON object. When the request is loaded, the Form that sent the request chnages the element associated with price in that Form to the recieved value from server.
    *   Form(id) | request sent to url | Element Changed(id)
        ---------|-------------|----------|
        #pizza_form | "pizza_price/" | #pizza_price
        #sub_form | "sub_price/" | #sub_price
        #pasta_form | "pasta_price/" | #pasta_price
        #salad_form | "salad_Price/" | #salad_price
        #platter_form | "platter_price/" | #platter_form
* **cart.js**:- This file is linked with "order/cart.html" html file. This JS file has an event-listener for "DOMContentLoaded". This event has a callback function that waits for a Button Click associated with the menu-item cards in "order/cart.html". On Button Click the a XMLHttpRequest() object is created and a request is sent to the server which deletes the card whose button was clicked.
    *   Button Class | request sent to url
        ------------ | -------------------
        .pizza_close | "delete_pizza/"
        .sub_close | "delete_sub/"
        .pasta_close | "delete_pasta/"
        .salad_close | "delete_salad/"
        .platter_close | "delete_platter/"
* **order.js**:- This file is linked with "order/orders.html". This JS file has an event-listener for "DOMContentLoaded". This event has a callback function that waits for a Button Click. On Button click a XMLHttpRequest() object is created and the request is sent to server with the "order id". When the request is loaded the page is reloaded.
* All these JS files has a **getCookie()** function that is used to get the CSRF Token to make request. 
* This folder also contains ".png" files that are used in the index page.

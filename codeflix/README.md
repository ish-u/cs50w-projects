# codeflix (Final Project)

Web Programming with Python and JavaScript. This is **codeflix**. A *Netflix* for MOOCs, Tutorials and Free Online Courses. The web-app currently has around 400 playlists (all the playlists from **CS50** and **MITOCW** YouTube Channel).
### **Heroku App** :- *https://codeflix50.herokuapp.com/*

## <ins>youtubedl/models.py</ins>
This file contains the classes for the *Models* used in the project:-
* **Video** :- This represents a YouTube Video. It has a field for the `video id` of a unique YouTube Video.The Model contains the following fields:-
    * `title`
    * `video_id`
    * `thumbnail`
    * `date`
    * `duration`
* **Category** :- This represents the category of the *Playlist* objects. The Model contains the following fields:-
    * `name`
* **Playlist** :- This represents a Course/Title/Playlist. It is a collection of unique *Video* objects. The Model contains the following fields:-
    * `name`
    * `playlist_id`
    * `thumbnail`
    * `videos`
    * `categories`
    * `average_rating`
    * `duration`

## <ins>youtubedl/urls.py</ins>
This file contains all the urls of the youtubedl app of project:-
 ||||
-----------| -----------| ----------- 
`""` | `"video/"` | `"video/<str:id>"`
`"register"` | `"playlist/"` | `"playlist/<str:id>"`
`"admin-dashboard"` | `"remove/<str:id>"` | `"search"`

## <ins>youtubedl/views.py</ins>
This file contains all the views of the *youtubedl* app of **codeflix** project.

* **index** :-  This view is linked with the url ""(index). It renders the HTML page `templates/youtubedl/index.html`. This view also sends various querysets of the `Playlist` Model to the url. 

*  **playlist** :- This view is linked with two url "playlist/" and "playlist/\<str:id>\". It renders to the HTML page `templates/youtubedl/playlist.html`. If the request is **GET**, the view sends the `Playlist` object that with the requested `id` in the url. If the request is **POST**, the view sends a `JSONResponse` with videos and playlist as two key.

* **video** :- This view is linked with two url "video/" and "video/\<str:id>\". It renders the HTML page `templates/youtubedl/video.html`. The view only works for **GET** request. The view also retuns `Playlist` object of the requested `id` in the url.

* **register** :- This view is linked with the url "register/". It renders the HTML page `templates/youtubedl/register.html`. This view is used to register a User to the site. If the requet is ***GET**, it renders a form for registeration (sends a object of class `UserRegisterForm`) if the user is not authenticated , otherwise, it redirects to `index` view. If the request is **POST** the form is validated and the user is registered.

* **admin_dashboard** :- This view is linked with the url "admin-dashboard". It renders the HTML page `templates/youtubedl/admin.html`.If the request is **GET** the view returns a queryset with all the objects of `Playlist` Model and a `playlist_form` object. If the request is **POST** the and the `request` contains `search` in it, then the view performs a search for all the possible `Playlist` objects whose `name` field contains `request.POST["search"]`. If the **POST** the `request` does not contains `search` then the view saves the YouTube Playlist whose link was sent with the request in the Database.

* **search** :- This view is linked with the url "search". It renders the HTML page "templates/youtubedl/search.html". For **GET** requests thhe view redirects to "index" url. If the request is **POST** then the view performs a search for all the possible `Playlist` objects whose `name` field contains `request.POST["search"]` and returns.

* **remove** :- This view is linked with the url "remove". It does not render any template. When called it removes the `Playlist` object and all the `Video` objects associated with it whose `id` is passed to the view.

## <ins>templates(folder)</ins>
This folder contains all the templates of the web-app

* **layout/layout.html** :- This file contains the layout of the web app. All the other pages in the web-app extends this file to generate this. This file acts as a layout for other files in the templates folder. The HTML page is linked to the CSS file "static/youtube.dl/index.css" and the JS file "static/layout/layout.js". The HTML page contains a navbar and a div with class name `.hero`.

* **youtubedl/index.html** :- This is the index page of the web-app. The file extends "layout/layout.html". It has contains 3 `Handlebars` templates, i.e., `#episodes_template`, `#title_template`and `#slider_template`,  a `div` with the class name `.hero_details` that is appended as a child to the `div` with the class name `.hero` and 5 slider `div` that displays all the objects from 5 different `querysets` returned from the `index` view during rendering of this Page. The HTML file is linked with the JS file "static/youtube.dl/index.js". The 5 slider `div`s conatians the title and picture of an object from `Playlist` Model in backend. The `div`s inside each of thses slider has class name `.thumb`. A div with id name `#slider` is appeneded as a sibling to the slider `div` whose `div` with class `.thumb` is clicked. The div with class name `.hero` displays the a picture and details of a random playist.

* **youtube/playlist.html** :- This page displays a `Playlist` object. The div with class name `.hero` displays the deatils about the Playlist. The page list all the `Video` objects associated with the `Playlist` object. The user can click on any video to play it.

* **youtubedl/search.html** :- This page displays the result of a seacrh done by the user.

* **youtubedl/video.html** :- This page plays the video which was requested in the `video` view in views.py. It contains a `iframe` element that covers the whole screen.

 * **users/login.html** :- This page displays a form that logs in a user. The page uses **crispy-form app** of django to render form.

* **users/register.html** :- This page displays a form that registers a user. The page uses **crispy-form app** of django to render form.

* **admin_dashboard/admin.html** :- This page is the Administrator Page for the web-app. The site admin can add a Playlist from **YouTube** and  *add, remove and edit* any object in the `Playlist` model. The page displays a Form in which the admin can submit the `url` of the Playlist from `YouTube` they want to add. The Page also list all the `Playlist` Model objects in from of card which has the option of going to **Playlist Page**, **Remove The Object and all the Video Objects in relation to it** and **Oject's Django-Admin Page**. 

## <ins>static(folder)</ins>
This folder contains all the static files of the web-app:-

* **layout/layout.js** :- This File is linked to the file "templates/layout/layout.html". This JS file has an event-listener for "DOMContentLoaded". The callback function of the event listener check for `window.onScroll` and that changes the `background-color` of navbar to *black* accordingly.

* **youtube.dl/index.js** :- This file is linked to the file "templates/youtubedl/index.html". This JS file has an event-listener for "DOMContentLoaded". The callback function compiles the `Handlebars` templates in "templates/youtubedl/index.html". It looks for a Click event on all the `div`s with that have class `.thumb`. A "XMLHttpRequest()" is sent to 'playlist' url and the `pk` (primary key) of a playlist is sent in `FormData` object. The `pk` is from the `data` attribute of the div with `.thumb` class which was clicked by the user. The Server returns a JSON object with two Keys "Playlist" and "Videos" that contains the information and videos of the `Playlist` object whose `pk` was sent to server. If the viewport is mobile *(or smaller than 575px)*, the user is redirected to the Playlist page ("templates/youtubedl/playlist.html") of the requested `Playlist` object form the Server. The file also has a **getCookie()** function that is used to get the CSRF Token to make request. 

* **youtbe.dl/index.css** :- This CSS file is linked to the "templates/layout/layout.html" and conatins various CSS properties for all the HTML in templates(folder).


## <ins>**import.py**</ins>
This file has a `add(url,category,start_index,end_index)` function. This can be used to add certain number of Playlist from a Particular YouTube Channel.
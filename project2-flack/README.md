# Project 2

Web Programming with Python and JavaScript
This is Flack.

## <ins>application.py</ins>

1. **/** :- This route returns the index.html file (Index Route)

2. **/login**:- This route renders "login.html". The "login.html" html page asks users for a <ins>username</ins> when a user first visits the web-app. If the <ins>username</ins> entered is already used by some other user then the route flashes an error message that the user already exists. If the <ins>username</ins> entered is unique then a "permanent session" is created, <ins>username</ins> is added to the "users" list and the user is redirected to "index.html"

3. **@socketio.on('user_message')**:- This event on recieving the data from the client-side creates an object of "Message" class (which contains message, room, timestamp, username of the user) and stores this object in the "messages" list. After storing the message this event emits an event named "user_message" in the client-side sending username, message, timestamp and room.

4. **@socketio.on('join')**:- This event on recieving data from the client-side calls the "join_room()" function. This function is a built-in function of flask-socketio and allows us to group users in groups. With this event we make a user join a certain room or group. The data sent or recieved (messages, here) will only be visible to users that are in this group only. After joining the user to a room this event emits an event named "user_message" in the client-side sending infromation that user has joined a certain room.

5. **@socketio.on('leave')**:-  This event on recieving the data from the client-side calls "leave_room()" function, This is a bulit-in flask-socketio and allows users to leave a room they are joined in. After leaving the room this event emits an named "user_message" in the client side sending information to the room that the user left.

6. **@socketio.on('add_room')**:- This event creates a new room. After recieving the name of the "new room" from the client-side, this function checks if a room of that name already exists or not. If the name of the new room is unique than it is added to "room" list and an event named "add_room" is emitted to the client-side sending new room name. This client-side event is broadcated across all rooms.

7. **@socketio.on('change')**:- This event is used to chnage the username of the "user". This event on recieving data from the client-side changes the "old username" of the user to the "new username". It also chnages all the attributes with "old useraname" to the new one in all the "Message" objects in the "messages" list.In the end an event named "change" is emitted to the client-side sending "new username" and "old username". 

8. **@socketio.on('stored_message')**:- This event recieves the room name from the client side and sends all the "Message" objects from the recieved room name to the client-side by emiting the "stored_message" event.

## <ins>index.html</ins>

1. The page has following elements :-
    * **Channels**:- This exits on the right side of the navigation bar. It is a drop-down menu that displays all the avilable channels and allows users to change channels(or room). It also has a "New Channel" list-item that invokes a "#addChannelModal"(id) modal through which the user can new Channels(or room).
    * **Display Name**:- This is located to the right of the "Channels". It is a drop-down menu with "username" as the toggler for the menu. The menu has two option:-
        * **Darkmode** :- This list-item on clicking enables darkmode for the page. It calls the darkmode() function in "index.js".
        * **Change Username** :- This lits-item on clicking invokes the "#changeUsername"(id) modal that allows the users to change their username.
    * **Message Area**:- This is a 'div' that is inside of a "container" that contains "#messages"(id) and "#inputArea"(id) 'div' inside of it.
    * **#messages**:- This is a 'div' that shows the messages sent and recieved between users and system messages such as "joining or leaving a room by a user".
    * **#inputArea**:- This is a 'div' that has a "text-area" and a "button". The "button" sends the message written by the user in the "text-area"

2. The page also uses "Handlebars" templates. The two templates are:-
    * **#userMessage(id)**:- This templates is describes the messages sent between the users which are visible inside of "#messages"(id) 'div'.
    * **#systemMessage(id)**:- This templates describes the system messages such a "joining" a room inside the "#messages"(id) 'div'.

3. The page uses :-
    * Bootstrap
    * "style.css"(from 'static' folder)
    * FontAwesome for the send button in the "#inputArea"(id) 'div'.


## <ins>index.js</ins>
The file has an event-listener for "DOMContentLoaded". On this event the "socketio" is initialised. The "currentRoom" variable from the local storage is obtained and the user is joined to the room with the obtained value. If the no "currentRoom" exits (i.e. null) then the user is joined to the "general" room.

* function:-
    * join_room() :- makes the user join a room. It emits 'join' event to the server-side sending the name of the room the user wants to join.
    * leave_room() :- makes the user leave a room. It emits 'leave' event to the server-side sending the name of the room the user wants to leave and clears the "#messages"(id) 'div' fro the user. 
    * down() :- scrolls down to the end in the "#messages"(id) 'div'.
    * darkmode() :- changes the style of "index.html".
    * change_update_channel() :- this function changes or updates the channel.

* socketio events:-
    * 'change' :- It is changes old-username to the new one on invoking and creates a system-message which is appended to 
    "#messages"(id) 'div'.
    *  'add_room' :- This event creates a new channel.
    * 'stored_message' :- This event displays the stored messages of a current room when the user join the room.
    * 'user_message' :- This event creates the messages in the "#messages"(id) div.

## <ins>login.html</ins>
This page logs in the user. It has a 'input' and 'button'. If the username already exists then the it flashes "USERNAME EXISTS".

## <ins>login.js</ins>
The file has an event-listener for "DOMContentLoaded". On this event the page waits for an "onclick" event on "#login"(id) button. On "onclick" event we save the key "user_id" with value of "#user_id"(id) input from "login.html" in "localStorage".

## <ins>style.css</ins>
This file contains the CSS applied on "index.html"


        

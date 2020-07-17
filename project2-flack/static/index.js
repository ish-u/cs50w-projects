//getting handlebars template
var messageTemplate = Handlebars.compile(document.querySelector("#messageTemplate").innerHTML);
var systemMessage = Handlebars.compile(document.querySelector("#systemMessage").innerHTML);
addEventListener('DOMContentLoaded', () => {
    document.querySelector("#dropdownUsername").innerHTML = localStorage.getItem("user_id");
    //SockeIO
    var socket = io();    
    socket.on('connect', ()=> {
        socket.send("  Connected   ");
    })
    localStorage.setItem("dark","0");
    var room = localStorage.getItem("currentRoom");
    if(localStorage.getItem("currentRoom") == null)
    {
        localStorage.setItem("currentItem","general");
        room = "general";
    }
    join_room(room);
    //remembering the current channel/room of the user
    down();

    //sending user_message
    document.querySelector('#send_message').onclick = () => {
        socket.emit('user_message', {"room":room,"message":document.querySelector('#message').value,"user":localStorage.getItem("user_id")});
        document.querySelector("#message").value = "";
        document.querySelector("#send_message").disabled = true;
        document.querySelector('#message').style.height = "auto";
    }

    //appending user message
    socket.on('user_message', data => {
        var dark = (localStorage.getItem("dark") == "1") ? true : false;
        if(data["flag"] == 1)
        {
            var align =(localStorage.getItem("user_id") == data["username"]) ? true : false ;
            const message = messageTemplate({right:align,username:data["username"],timestamp:data["time_stamp"],message:data["msg"],darkmode:dark});
            document.querySelector("#messages").innerHTML += message;
        }
        else if(data["flag"] == 0)
        {
            const message = systemMessage({username:data["username"],room:data["room"],message:data["msg"],darkmode:dark});
            document.querySelector("#messages").innerHTML += (message);
        }
        down();

    })

    //displaying stored messages
    socket.on('stored_message', data => {
        var align;
        if (localStorage.getItem("user_id") == data["username"]) {
            align = true;
        }
        else {
            align = false;
        }
        var dark = (localStorage.getItem("dark") == "1") ? true : false;
        const message = messageTemplate({darkmode:dark,right: align, username: data["username"], timestamp: data["time_stamp"], message: data["msg"] });
        document.querySelector("#messages").innerHTML += (message);
        down();
    })

    //adding channels
    document.querySelector("#addChannel").onclick = () => {
        document.querySelectorAll(".channel").forEach(a => {
            if(a.innerHTML == document.querySelector("#newChannel").value){
                alert("ROOM EXISTS");
            }
        });
        console.log("Adding New Room" + document.querySelector("#newChannel").value);
        create_room = document.querySelector("#newChannel").value;
        socket.emit('add_room',{"room":create_room});
        document.querySelector("#newChannel").value = "";
    }

    socket.on('add_room', data => {
        console.log("ROOM ADDED - appening element with id=channelList");
        const a = document.createElement("a");
        a.setAttribute("class","channel dropdown-item");
        a.innerHTML = data;
        document.querySelector("#channelList").appendChild(a); 
        //update channel list
        change_update_channel();
        document.querySelector("#addChannel").disabled = true;    
      
    });

    //changing channels
    change_update_channel();

    //changing and updating channel function
    function change_update_channel(){
        console.log("CHNAGING / UPDATING ROOM");
        document.querySelectorAll(".channel").forEach(a => {
            a.onclick = () =>{
                new_room = a.innerHTML;
                //checking if the user is already in the room 
                if(room != new_room)
                {
                    //if the user is not in the clicked room change the room by first leaving the current room 
                    //and then joining the new room
                    leave_room(room);
                    join_room(new_room);
                    room = new_room;
                    localStorage.setItem("currentRoom",room);
                }
                else
                {
                    console.log("not allowed");
                }
                
            }
        })
    }

    //changing username
    document.querySelector("#change").onclick = () => {
        const old_user_id = localStorage.getItem("user_id");
        localStorage.setItem("user_id",document.querySelector("#changedUsername").value);
        document.querySelector("#dropdownUsername").innerHTML = document.querySelector("#changedUsername").value;
        socket.emit('change',{"user":document.querySelector("#changedUsername").value,"room":room,"old":old_user_id});
        document.querySelector("#changedUsername").value = "";
    }
    socket.on('change', data=> {
        document.querySelectorAll(".username").forEach( h6 => {
            if(data["old"] == h6.innerHTML)
            {
                h6.innerHTML = data["username"];
            }
        })
        var dark = (localStorage.getItem("dark") == "1") ? true : false;
        const message = systemMessage({change:true,username:data["username"],old_username:data["old"],darkmode:dark});
        document.querySelector("#messages").innerHTML += message;
        down();
        document.querySelector("#change").disabled = true;
    })


    //join_room function
    function join_room(room){
        console.log("JOINED ROOM : " + room);
        socket.emit('stored_message',{"room":room});
        socket.emit('join',{"username":localStorage.getItem("user_id"),"room":room});
    }
    
    //leave_room function
    function leave_room(room){
        console.log("LEFT ROOM : " + room);
        socket.emit('leave', {"username":localStorage.getItem("user_id"),"room":room});
        //when the user will leave the room we will clear the message area
        document.querySelector("#messages").innerHTML = "";
    }


    //scroll down function
    function down()
    {
        var messageHeight = document.querySelector("#messages");
        messageHeight.scrollTop = messageHeight.scrollHeight;

    }

    //disabling button in case of no input
    document.querySelector("#changedUsername").onkeyup = () => {
        var newUsername = document.querySelector("#changedUsername").value.length;
        document.querySelector("#change").disabled = (newUsername > 0) ? false : true;
    }

    document.querySelector("#newChannel").onkeyup = () => {
        var newChannel = document.querySelector("#newChannel").value.length;
        document.querySelector("#addChannel").disabled = (newChannel > 0) ? false : true;
    }

    document.querySelector("#message").onkeyup = () => {
        var message = document.querySelector("#message").value.length;
        document.querySelector("#send_message").disabled = (message > 0) ? false : true;
        
    }

    //incresing the textarea height
    var textarea = document.querySelector("#message");
    textarea.addEventListener('input',resize);
    function resize(){
        this.style.height = 'auto';
        this.style.height = textarea.scrollHeight + "px";
    }

    //darkmode
    function darkmode() {
        if (localStorage.getItem("dark") == "1") {
            document.querySelector("body").style.backgroundColor = "black";
            document.querySelector("nav").style.backgroundColor = "#1a237e";
            document.querySelector("#messages").style.backgroundColor = "black";
            document.querySelector("#inputArea").style.backgroundColor = "black";
            document.querySelector("#messages").style.border = "none";
            document.querySelector("#inputArea").style.border = "none";
            document.querySelector("textarea").style.backgroundColor = "#2632384d";
            document.querySelector("textarea").style.color = "white";
            document.querySelector(".systemMessage").style.color = "white";
            document.querySelectorAll(".message").forEach(message => {
                message.style.backgroundColor = "rgb(69, 39, 160)";
            })
            document.querySelectorAll(".systemMessage").forEach(message => {
                message.style.color = "white";
            })
        }
    }

    document.querySelector("#darkmode").onclick = () => {
        localStorage.setItem("dark", "1");
        darkmode();
    }
    
    
});


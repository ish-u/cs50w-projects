document.addEventListener("DOMContentLoaded", () => {
    //adding random playlist details
    document.querySelector(".hero").append(document.querySelector(".hero_details"));
    var checkMobile = window.matchMedia("(max-width: 575px)");
    var episodes_template = Handlebars.compile(document.querySelector("#episodes_template").innerHTML);
    var title_template = Handlebars.compile(document.querySelector("#title_template").innerHTML)
    var slider_template = Handlebars.compile(document.querySelector("#slider_template").innerHTML);
    var token = getCookie('csrftoken');
    var data = new FormData();
    document.querySelectorAll(".thumb").forEach((a) => {
        a.onclick = () => {
            if(checkMobile.matches){
                location.href =  a.dataset.url;
            }
            else{
                document.querySelectorAll(".thumb").forEach(z => {
                    z.style.border = "1px solid white"
                })
                a.style.border = "5px solid white"
                if (a.parentNode.parentNode.childElementCount == 1) {
                    if (document.querySelector("#slider") != null) {
                        var slider = document.querySelector("#slider");
                        slider.remove();
                    }
                    var div = document.createElement("div");
                    div.setAttribute("class", "conatiner-fluid appear");
                    div.id = "slider"
                    div.innerHTML = slider_template({});
                    a.parentNode.parentNode.insertBefore(div, a.parentNode.nextSibling);

                }
                var request = new XMLHttpRequest();
                request.open("POST", "playlist", true);
                request.setRequestHeader('X-CSRFToken', token);
                request.onload = () => {
                    detail = JSON.parse((request.responseText));
                    videos = detail["videos"]
                    playlist = detail["playlist"][0]["fields"]
                    //creating elements for epiodes div
                    const container = document.createElement("div");
                    container.setAttribute("class", "container appear");
                    container.style = "display:flex; overflow-x:scroll; overflow-y:hidden; height:inherit;";
                    for (var i = 0; i < videos.length; i++) {
                        var div = episodes_template({ "video_id": videos[i]["fields"]["video_id"], "thumbnail": videos[i]["fields"]["thumbnail"], "title": videos[i]["fields"]["title"],"number":i,"duration": videos[i]["fields"]["duration"]})
                        container.innerHTML += div;
                    }//setting slider background
                    document.querySelector("#slider").style.backgroundImage = "linear-gradient(to right,rgba(0,0,0,1),rgba(0,0,0,0)),url('" + playlist["thumbnail"] + "')"
                    document.querySelector(".episodes").innerHTML = "";
                    document.querySelector(".episodes").append(container);
                    document.querySelector(".episodes").style.display = "none";
                    document.querySelector(".title").style.display = "none";
                    //creating elements for title div
                    document.querySelector(".title").innerHTML = "";
                    const container2 = document.createElement("div");
                    container2.innerHTML = "";
                    container2.style = "display:block;";
                    container2.classList = "";
                    container2.innerHTML = title_template({"name":playlist["name"],"duration":playlist["duration"],"average_rating":playlist["average_rating"],"date":playlist["date"].substring(0,4)})
                    document.querySelector(".title").append(container2);
                    document.querySelector(".title").style.display = "block";
                    //restting buttons
                    document.querySelector(".title_button").parentElement.classList.add("active");
                    document.querySelector(".episodes_button").parentElement.classList.remove("active");
                    var slider = document.querySelector("#slider");
                    if (slider.style.display != "grid") {
                        slider.style.display = "grid";
                        slider.scrollIntoView({ behavior: "smooth",block:"end" },true);
                        
                    }
                }
                data.append("pk", a.dataset.id);
                request.send(data);
                //slider functions
                var slider = document.querySelector("#slider");
                document.querySelector("#slider_close").onclick = () => {
                    slider.classList += " disappear";
                    slider.addEventListener("animationend", () => {
                        slider.remove();
                    })
                    document.querySelectorAll(".thumb").forEach(z => {
                        z.style.border = "white solid 1px"
                    })
                }
                document.querySelector(".title_button").onclick = () => {
                    document.querySelector(".episodes").style.display = "none";
                    slider.style.backgroundColor = "transparent";
                    document.querySelector(".title").style.display = "block";
                }
                document.querySelector(".episodes_button").onclick = () => {
                    document.querySelector(".title").style.display = "none";
                    document.querySelector(".episodes").style.display = "block";

                }
                return false;
            }
        }
    })

})


//to get that csrf token :)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


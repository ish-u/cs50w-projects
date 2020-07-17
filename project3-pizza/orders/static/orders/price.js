addEventListener("DOMContentLoaded", () => {
    var token = getCookie('csrftoken');
    var data = new FormData();

    //pizza_price request
    document.querySelector("#pizza_form").onchange = () =>{
        var request = new XMLHttpRequest();
        request.open("POST", 'pizza_order/', true);
        request.setRequestHeader('X-CSRFToken', token);
        request.onload = () => {
            if(JSON.parse(request.responseText)["price"] == 0 || document.querySelectorAll('input[name=topping]:checked').length == max_pizza_topping){
                document.querySelectorAll('input[name=topping]:not(:checked)').forEach(a => {
                    a.disabled = true;
                })
            }
            else{
                document.querySelectorAll('input[name=topping]:not(:checked)').forEach(a => {
                    a.disabled = false;
                })
            }
            document.querySelector("#pizza_cart").disabled =  JSON.parse(request.responseText)["price"] == 0 ? true:false;
            document.querySelector("#pizza_price").innerHTML = JSON.parse(request.responseText)["price"];
        }
        data.append("price", "1");
        data.append("size", document.querySelector("#pizza_size").selectedOptions[0].value);
        data.append("type", document.querySelector("#pizza_type").selectedOptions[0].value);
        data.append("topping", document.querySelectorAll('input[name=topping]:checked').length)
        request.send(data);
        return false;
    }
    //sub_price request
    document.querySelector("#sub_form").onchange = () =>{
        var request = new XMLHttpRequest();
        request.open("POST", 'sub_order/', true);
        request.setRequestHeader('X-CSRFToken', token);
        request.onload = () => {
            if(JSON.parse(request.responseText)["price"] == 0){
                document.querySelectorAll('input[name=sub_topping]:not(:checked)').forEach(a => {
                    a.disabled = true;
                })
            }
            else{
                document.querySelectorAll('input[name=sub_topping]:not(:checked)').forEach(a => {
                    a.disabled = false;
                })
                document.querySelector("#extra_cheese").disabled = false;
            }
            document.querySelector("#sub_cart").disabled =  JSON.parse(request.responseText)["price"] == 0 ? true:false;
            if(document.querySelector("#extra_cheese").checked){
                document.querySelector("#sub_price").innerHTML = JSON.parse(request.responseText)["price"] + 0.5;    
            }
            else{
                document.querySelector("#sub_price").innerHTML = JSON.parse(request.responseText)["price"];
            }
        }
        data.append("price", "1");
        data.append("size", document.querySelector("#sub_size").selectedOptions[0].value);
        data.append("name", document.querySelector("#sub_name").selectedOptions[0].value);
        request.send(data);
        return false;
    }
    //pasta_price request
    document.querySelector("#pasta_form").onchange = () =>{
        var request = new XMLHttpRequest();
        request.open("POST", 'pasta_order/', true);
        request.setRequestHeader('X-CSRFToken', token);
        request.onload = () => {
            if(JSON.parse(request.responseText)["price"] == 0){
                document.querySelector("#pasta_cart").disabled = true;
            }
            document.querySelector("#pasta_cart").disabled =  JSON.parse(request.responseText)["price"] == 0 ? true:false;
            document.querySelector("#pasta_price").innerHTML = JSON.parse(request.responseText)["price"];
        }
        data.append("price", "1");
        data.append("name", document.querySelector("#pasta_name").selectedOptions[0].value);
        request.send(data);
        return false;
    }
    //salad_price request
    document.querySelector("#salad_form").onchange = () => {
        var request = new XMLHttpRequest();
        request.open("POST", 'salad_order/', true);
        request.setRequestHeader('X-CSRFToken', token);
        request.onload = () => {
            if(JSON.parse(request.responseText)["price"] == 0){
                document.querySelector("#salad_cart").disabled = true;
            }
            document.querySelector("#salad_cart").disabled =  JSON.parse(request.responseText)["price"] == 0 ? true:false;
            document.querySelector("#salad_price").innerHTML = JSON.parse(request.responseText)["price"];
        }
        data.append("price", "1");
        data.append("name", document.querySelector("#salad_name").selectedOptions[0].value);
        request.send(data);
        return false;
    }

    document.querySelector("#platter_form").onchange = () => {
        var request = new XMLHttpRequest();
        request.open("POST", 'platter_order/', true);
        request.setRequestHeader('X-CSRFToken', token);
        request.onload = () => {
            if(JSON.parse(request.responseText)["price"] == 0){
                document.querySelector("#platter_cart").disabled = true;
            }
            document.querySelector("#platter_cart").disabled =  JSON.parse(request.responseText)["price"] == 0 ? true:false;
            document.querySelector("#platter_price").innerHTML = JSON.parse(request.responseText)["price"];

        }
        data.append("price", "1");
        data.append("size",document.querySelector("#platter_size").selectedOptions[0].value)
        data.append("platter_name", document.querySelector("#platter_name").selectedOptions[0].value);
        request.send(data);
        return false;
    }

    //special pizza request
    document.querySelector("#special_form").onchange = () => {
        var request = new XMLHttpRequest();
        request.open("POST", 'special/', true);
        request.setRequestHeader('X-CSRFToken', token);
        request.onload = () => {
            document.querySelector("#special_price").innerHTML = JSON.parse(request.responseText)["price"]
        }
        data.append("price","1");
        data.append("type",document.querySelector("#special_crust").selectedOptions[0].value)
        data.append("size",document.querySelector("#special_size").selectedOptions[0].value)
        request.send(data);
        return false;
    }

    //reseting forms
    //pizza_form
    document.querySelector("#pizza_close").onclick = () => {
        document.querySelector("#pizza_form").reset();
        document.querySelector("#pizza_price").innerHTML = "0";
        document.querySelector("#pizza_cart").disabled = true;
        document.querySelectorAll('input[name=topping]:not(:checked)').forEach(a => {
            a.disabled = true;
        })
    }
    //pizza_form
    document.querySelector("#sub_close").onclick = () => {
        document.querySelector("#sub_form").reset();
        document.querySelector("#sub_price").innerHTML = "0";
        document.querySelector("#sub_cart").disabled = true;
        document.querySelectorAll('input[name=sub_topping]:not(:checked)').forEach(a => {
            a.disabled = true;
        })
    }
    //pasta_form
    document.querySelector("#pasta_close").onclick = () => {
        document.querySelector("#pasta_form").reset();
        document.querySelector("#pasta_cart").disabled = true; 
        document.querySelector("#pasta_price").innerHTML = "0";  
    }
    //salad_form
    document.querySelector("#salad_close").onclick = () => {
        document.querySelector("#salad_form").reset();
        document.querySelector("#salad_cart").disabled = true; 
        document.querySelector("#salad_price").innerHTML = "0";  
    }
    //platter_form
    document.querySelector("#platter_close").onclick = () => {
        document.querySelector("#platter_form").reset();
        document.querySelector("#platter_cart").disabled = true; 
        document.querySelector("#platter_price").innerHTML = "0";  
    }

});

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



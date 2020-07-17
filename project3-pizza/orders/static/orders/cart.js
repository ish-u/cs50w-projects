document.addEventListener("DOMContentLoaded", () => {

    token = getCookie('csrftoken');

    //delete Pizza from Cart
    document.querySelectorAll(".pizza_close").forEach(a => {
        a.onclick = () => {
            var request = new XMLHttpRequest();
            request.open("POST", 'delete_pizza/', true)
            request.setRequestHeader('X-CSRFToken', token);
            request.onload = () => {
                location.reload();
            }
            var data = new FormData();
            data.append("id",a.value)
            request.send(data);
        }
    })

    //delete Sub from Cart
    document.querySelectorAll(".sub_close").forEach(a => {
        a.onclick = () => {
            var request = new XMLHttpRequest();
            request.open("POST", 'delete_sub/', true)
            request.setRequestHeader('X-CSRFToken', token);
            request.onload = () => {
                location.reload();
            }
            var data = new FormData();
            data.append("id",a.value)
            request.send(data);
        }
    })

    //delete Salad from Cart
    document.querySelectorAll(".salad_close").forEach(a => {
        a.onclick = () => {
            var request = new XMLHttpRequest();
            request.open("POST", 'delete_salad/', true)
            request.setRequestHeader('X-CSRFToken', token);
            request.onload = () => {
                location.reload();
            }
            var data = new FormData();
            data.append("id",a.value)
            request.send(data);
        }
    })

    //delete Pasta from Cart
    document.querySelectorAll(".pasta_close").forEach(a => {
        a.onclick = () => {
            var request = new XMLHttpRequest();
            request.open("POST", 'delete_pasta/', true)
            request.setRequestHeader('X-CSRFToken', token);
            request.onload = () => {
                location.reload();
            }
            var data = new FormData();
            data.append("id",a.value)
            request.send(data);
        }
    })

    //delete Platter from Cart
    document.querySelectorAll(".platter_close").forEach(a => {
        a.onclick = () => {
            var request = new XMLHttpRequest();
            request.open("POST", 'delete_platter/', true)
            request.setRequestHeader('X-CSRFToken', token);
            request.onload = () => {
                location.reload();
            }
            var data = new FormData();
            data.append("id",a.value)
            request.send(data);
        }
    })
})

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

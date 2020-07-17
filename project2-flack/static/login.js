addEventListener("DOMContentLoaded", () => {

    document.querySelector("#login").onclick = () => {
        localStorage.setItem("user_id",document.querySelector("#user_id").value)
        console.log(document.querySelector("#user_id").value)
    }

    document.querySelector("#user_id").onkeyup = () => {
        if(document.querySelector("#user_id").value.length  > 0)
        {
            document.querySelector("#login").disabled = false;
        }
        else
        {
            document.querySelector("#login").disabled = true;
        }
    }

});




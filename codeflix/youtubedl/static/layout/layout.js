document.addEventListener("DOMContentLoaded", () => {
    var checkMobile = window.matchMedia("(max-width: 768px)");
    if(!checkMobile.matches){
        window.onscroll = () =>{
            if(document.body.scrollTop > 30 || document.documentElement.scrollTop > 30)
            {
                document.querySelector("nav").style.backgroundColor = "black";
            }
            else
            {
                document.querySelector("nav").style.backgroundColor = "rgba(20,20,20,0.5)";
            }
        }
    }
    else{
        document.querySelector("nav").style.backgroundColor = "black";
    }

})
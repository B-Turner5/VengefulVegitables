document.addEventListener('DOMContentLoaded', function () {
    var splashIcon = document.querySelector(".splash-icon");
    setTimeout(()=>{
        splashIcon.style.opacity = 1;
    }, 610)

    var splashScreen = document.querySelector(".splash");
    splashScreen.addEventListener('click', ()=>{
        splashScreen.style.opacity = 0;
        setTimeout(()=>{
            splashScreen.classList.add('hidden')
        }, 610)
    })
});
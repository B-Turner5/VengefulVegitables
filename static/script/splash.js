document.addEventListener('DOMContentLoaded', function () {
    var splashContent = document.querySelector(".splash-content");
    var splashScreen = document.querySelector(".splash-screen");

    setTimeout(()=>{
        splashContent.classList.add("grow");
    }, 600)

    splashScreen.addEventListener('click', ()=>{
        splashScreen.style.opacity = 0;
        splashContent.classList.add("slide");
        setTimeout(()=>{
            splashScreen.classList.add('hidden');
        }, 600)
    })
});
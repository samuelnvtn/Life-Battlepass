
let tabs = document.querySelectorAll(".navtext");
        let contents = document.querySelectorAll(".tab-content div");

        tabs.forEach((tab, index) => {
            tab.addEventListener("click", () => {
                contents.forEach((content) => {
                    content.classList.remove("active");
                });
                tabs.forEach((tab) => {
                    tab.classList.remove("active");
                });
                contents[index].classList.add("active");
                tabs[index].classList.add("active");
            });
        });
        
/*
var xp = 0;
var challenge = 50;

function addXP(){
    
    var checkboxes = document.querySelectorAll('input[type=checkbox]');
    xp = 0;

    checkboxes.forEach(function(checkbox){
        if (checkbox.checked) {
            xp += challenge;
        }
    }); 
    //test

    document.getElementById("xpDisplay").innerHTML = xp;
    console.log(xp);

    document.querySelectorAll('input[type=checkbox]').forEach(function(checkbox) {
        checkbox.addEventListener('change', addXP);
    });
}
    */
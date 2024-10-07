
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

    document.getElementById("xpDisplay").innerHTML = xp;
    console.log(xp);

    document.querySelectorAll('input[type=checkbox]').forEach(function(checkbox) {
        checkbox.addEventListener('change', addXP);
    });
}
let tabs = document.querySelectorAll(".navtext");
let contents = document.querySelectorAll(".tab-content > div");

tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
        tabs.forEach((tab) => tab.classList.remove("active"));
        contents.forEach((content) => content.classList.remove("active"));

        tab.classList.add("active");

        let targetId = tab.parentElement.getAttribute("data-target");
        document.getElementById(targetId).classList.add("active");
    });
});

const switcherContainer = document.querySelector('.switcher-container');

let isDown = false;
let startX;
let scrollLeft;

switcherContainer.addEventListener('mousedown', (e) => {
  isDown = true;
  switcherContainer.classList.add('active');
  startX = e.pageX - switcherContainer.offsetLeft;
  scrollLeft = switcherContainer.scrollLeft;
});

switcherContainer.addEventListener('mouseleave', () => {
  isDown = false;
  switcherContainer.classList.remove('active');
});

switcherContainer.addEventListener('mouseup', () => {
  isDown = false;
  switcherContainer.classList.remove('active');
});

switcherContainer.addEventListener('mousemove', (e) => {
  if (!isDown) return; // Stop the function from running if the mouse isn't held down
  e.preventDefault();
  const x = e.pageX - switcherContainer.offsetLeft;
  const walk = (x - startX) * 3; // Scroll-fast multiplier
  switcherContainer.scrollLeft = scrollLeft - walk;
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight') {
     switcherContainer.scrollBy({ left: 300, behavior: 'smooth' }); // Scroll right
  }
  if (e.key === 'ArrowLeft') {
    switcherContainer.scrollBy({ left: -300, behavior: 'smooth' }); // Scroll left
  }
});


document.querySelectorAll('.mark-completed-btn').forEach(button => {
    button.addEventListener('click', function() {
        const taskId = this.dataset.taskId;

        // Send the AJAX request to mark the task as completed
        fetch(`/mark_task_completed/${taskId}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Change the task color to green and disable the button
                const taskCard = this.closest('.task-card');
                taskCard.classList.add('completed'); // Add 'completed' class for green color
                this.disabled = true;
                this.innerHTML = 'Completed'; // Change button text

                // Update the total XP dynamically on the page
                const totalXpElement = document.querySelector('.xptext');
                if (totalXpElement) {
                    totalXpElement.innerHTML = `${data.total_xp} XP`; // Update total XP display
                }

                 // Update the current XP for the operation dynamically
                const operationXpElement = document.querySelector(`.operation-xp[data-operation-id="${data.operation_id}"]`);
                if (operationXpElement) {
                    operationXpElement.innerHTML = `Current XP: ${data.current_xp} / ${data.operation_xp_goal}
                                            `; // Update current XP display
                }

                const operationLevelElement = document.querySelector(`.operation-level[data-operation-id="${data.operation_id}"]`);
                if (operationLevelElement) {
                    operationLevelElement.innerHTML = `Level: ${data.current_level} / ${data.max_level}`;
                }
                if (data.completed) {
                const operationCard = document.querySelector(`.operation-card[data-operation-id="${data.operation_id}"]`);
                if (operationCard) {
                    operationCard.classList.add('comp'); // Přidání žlutého borderu
                }
                }

                const progressBar = document.querySelector(`.progress[data-operation-id="${data.operation_id}"]`);
                if (progressBar) {
                    const progressPercentage = (data.current_xp % 1000) / 10; // Calculate progress percentage
                    progressBar.style.width = `${progressPercentage}%`; // Update the progress bar width


                }


            } else {
                console.error('Error:', data.message);
            }
        })
        .catch(error => console.error('Error:', error));
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
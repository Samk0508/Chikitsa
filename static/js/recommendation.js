document.querySelector(".recommend").addEventListener("click",function(){
    document.querySelector(".popupcontainer").classList.add("active");
});

document.querySelector(".popupcontainer .popup-close-btn").addEventListener("click",function(){
    document.querySelector(".popupcontainer").classList.remove("active");
});

recommend_button = document.getElementById("recommend_button");
recommend_button.addEventListener("click", () => {
    const items = document.querySelectorAll(".item-label");
    var symptoms_list = []
    items.forEach((element) => {
        symptoms_list.push(element.innerText);
    });
    ajax_query(symptoms_list);
});

function ajax_query(array) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/process_data");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onload = function() {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            const diet_list = document.getElementById("diet-list");
            const disease_name = document.getElementById("disease-name");
            const workout_list = document.getElementById("workout-list");
            const remedies_list = document.getElementById("remedies-list");
            const precautions_list = document.getElementById("precautions-list");
            const disease_description = document.getElementById("disease-description");

            disease_name.innerText = response["disease_name"];
            disease_description.innerText = response["disease_description"];
            response["precautions_list"].forEach((item) => {
                var li = document.createElement('li');
                li.textContent = item;
                precautions_list.appendChild(li);
            });
            response["remedies_list"].forEach((item) => {
                var li = document.createElement('li');
                li.textContent = item;
                remedies_list.appendChild(li);
            });
            response["diet_list"].forEach((item) => {
                var li = document.createElement('li');
                li.textContent = item;
                diet_list.appendChild(li);
            });
            response["workout_list"].forEach((item) => {
                var li = document.createElement('li');
                li.textContent = item;
                workout_list.appendChild(li);
            });
        }
    }

    xhr.onerror = function() {
        console.error("Error: ", xhr.statusText);
    }

    xhr.send(JSON.stringify({data: array}))
}

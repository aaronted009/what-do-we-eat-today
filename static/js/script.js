document
    .getElementById("order-form")
    .addEventListener("submit", function (event) {
        event.preventDefault();
        let q = document.getElementById("q").value;
        // Convert selected checkboxes to list
        // cuisineType
        let cuisineType_checkboxes = document.getElementsByName("cuisineType");
        let cuisineType = Array.from(cuisineType_checkboxes)
            .filter((checkbox) => checkbox.checked)
            .map((checkbox) => checkbox.value);
        // mealType
        let mealType = [document.getElementById("mealType").value];
        // diet
        let diet_checkboxes = document.getElementsByName("diet");
        let diet = Array.from(diet_checkboxes)
            .filter((checkbox) => checkbox.checked)
            .map((checkbox) => checkbox.value);
        // health
        let health_checkboxes = document.getElementsByName("health");
        let health = Array.from(health_checkboxes)
            .filter((checkbox) => checkbox.checked)
            .map((checkbox) => checkbox.value);

        let form_data = {
            q: q,
            cuisineType: cuisineType,
            mealType: mealType,
            diet: diet,
            health: health,
        };

        // Send the data to the server
        fetch("/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(form_data),
        })
            .then((response) => response.text())
            .then((data) => {
                console.log(data);
                document.getElementById("order-form").reset(); // Reset the form
            })
            .catch((error) => console.error("Error:", error));
    });

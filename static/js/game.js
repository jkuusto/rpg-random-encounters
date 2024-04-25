function changeBiome(gameId) {
    const select = document.getElementById("biomeSelect");
    const biomeId = select.options[select.selectedIndex].value;
    fetch("/change_biome/" + gameId, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({biome_id: biomeId}),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Server responded with status: ${response.status}`);
        }
        location.reload();
    });
}

// Toggle visibility of encounter tables
function toggleVisibility(buttonId, divId, sessionKey) {
    const button = document.getElementById(buttonId);
    const div = document.getElementById(divId);
    button.onclick = function() {
        if (div.style.display === "none") {
            div.style.display = "block";
            this.textContent = "Hide " + this.textContent;
            sessionStorage.setItem(sessionKey, 'true');
        } else {
            div.style.display = "none";
            this.textContent = this.textContent.replace("Hide ", "");
            sessionStorage.setItem(sessionKey, "false");
        }
    }
}

toggleVisibility("toggleButtonGeneral", "generalEncounters", 'generalEncountersVisible');
toggleVisibility("toggleButtonBiome", "biomeEncounters", 'biomeEncountersVisible');


// Restore visibility setting of encounter tables after page reload
window.onload = function() {
    // get visibility state from session storage
    const generalEncountersVisible = sessionStorage.getItem("generalEncountersVisible");
    const biomeEncountersVisible = sessionStorage.getItem("biomeEncountersVisible");

    // get references to the div elements
    const generalEncounters = document.getElementById("generalEncounters");
    const biomeEncounters = document.getElementById("biomeEncounters");

    // get references to the button elements
    const toggleButtonGeneral = document.getElementById("toggleButtonGeneral");
    const toggleButtonBiome = document.getElementById("toggleButtonBiome");

    if (generalEncountersVisible === "true") {
        generalEncounters.style.display = "block";
        toggleButtonGeneral.textContent = "Hide General Encounters";
    }

    if (biomeEncountersVisible === "true") {
        biomeEncounters.style.display = "block";
        toggleButtonBiome.textContent = "Hide Biome Encounters";
    }
}


// Event listener to edit range buttons
document.querySelectorAll(".range-button").forEach(function(button) {
    button.addEventListener("click", function() {
        const td = this.parentNode;
        const tr = td.parentNode;
        const input = document.createElement("input");
        td.innerHTML = "";
        td.appendChild(input);
        input.type = "text";
        input.placeholder = "New value, e.g. 20";
        input.focus();

        // Event listener to input range field
        input.addEventListener("keydown", function(event) {
            if (event.key === "Enter") {
                event.preventDefault();

                const newValue = event.target.value.trim();
                const id = tr.getAttribute("data-id");
                const tableName = tr.getAttribute("data-table");

                // Send request to server
                fetch("/change_roll_range/" + gameId, {
                    method: 'POST',
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({id: id, roll_range: newValue, table_name: tableName}),
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Server responded with status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.status === "success") {
                    location.reload();
                    }
                })
                .catch(error => {
                    const errorMessage = document.getElementById("errorMessage");
                    errorMessage.textContent = "An error occured while updating the roll range";
                });
            }
        });
    });
});

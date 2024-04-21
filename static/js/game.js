function changeBiome(gameId) {
    var select = document.getElementById("biomeSelect");
    var biomeId = select.options[select.selectedIndex].value;
    fetch("/change_biome/" + gameId, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({biome_id: biomeId}),
    })
    // Update the biome encounters table
    .then(response => response.json())
    .then(table_entries => {
        var table = document.getElementById("biomeEncountersTable");
        // Clear the viewport table
        while (table.rows.length > 1) {
            table.deleteRow(1);
        }
        // Add rows back with updated entries to the table
        for (var i = 0; i < table_entries.length; i++) {
            var row = table.insertRow(-1);
            for (var j = 1; j < table_entries[i].length; j++) {
                var cell = row.insertCell(j - 1);
                cell.innerHTML = table_entries[i][j];
            }
        }
    });
}


// Toggle visibility of encounter tables
function toggleVisibility(buttonId, divId, sessionKey) {
    var button = document.getElementById(buttonId);
    var div = document.getElementById(divId);
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
    var generalEncountersVisible = sessionStorage.getItem("generalEncountersVisible");
    var biomeEncountersVisible = sessionStorage.getItem("biomeEncountersVisible");

    // get references to the div elements
    var generalEncounters = document.getElementById("generalEncounters");
    var biomeEncounters = document.getElementById("biomeEncounters");

    // get references to the button elements
    var toggleButtonGeneral = document.getElementById("toggleButtonGeneral");
    var toggleButtonBiome = document.getElementById("toggleButtonBiome");

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
        var td = this.parentNode;

        var tr = td.parentNode;

        td.innerHTML = '';
        var input = document.createElement("input");
        input.type = "text";
        input.placeholder = "New value, e.g. 20";
        td.appendChild(input);
        input.focus();

        // Event listener to input range field
        input.addEventListener("keydown", function(event) {
            if (event.key === "Enter") {
                event.preventDefault();

                var newValue = event.target.value.trim();
                var id = tr.getAttribute("data-id");
                var tableName = tr.getAttribute("data-table");

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
                    let errorMessage = document.getElementById("errorMessage");
                    errorMessage.textContent = "An error occured while updating the roll range";
                });
            }
        });
    });
});

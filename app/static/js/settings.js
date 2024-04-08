import { html, tr, td, th, a, button, input } from "./modules/lib.js"
import { openWebsocket } from "./modules/websocket.js"

function createTable(data, status) {
    var tbody = document.querySelector("tbody");
    tbody.innerHTML = '';

    let interval = data['interval'];

    let _th = th('1');

    let interval_td = td('interval');
    interval_td.textContent = "interval";

    let _input = input(data['interval'], 'interval', 'number', true);
    let input_td = td();
    input_td.appendChild(_input);

    let edit_button = button('Edit', 'edit-0', 'btn', 'btn-primary', 'btn-sm');
    edit_button.addEventListener('click', function(event) {
        document.getElementById('interval').readOnly = false;
        document.getElementById('edit-0').hidden = true;
        document.getElementById('save-0').removeAttribute('hidden');
    });

    let save_button = button('Save', 'save-0', 'btn', 'btn-primary', 'btn-sm');
    save_button.setAttribute('hidden', 'true');
    save_button.addEventListener('click',save);
    let td_buttons = td();
    td_buttons.appendChild(edit_button);
    td_buttons.appendChild(save_button);

    let _tr = tr('0');
    _tr.appendChild(_th);
    _tr.appendChild(interval_td);
    _tr.appendChild(input_td);
    _tr.appendChild(td_buttons);

    tbody.appendChild(_tr);
}

function fillNtfyData(data) {
    document.getElementById("switchNtfy").checked = data['enabled'];
    document.getElementById("ntfyUrl").value = data['url'];
    document.getElementById("ntfyTopic").value = data['topic'];
    document.getElementById("ntfyPriority").value = data['priority'];

    if(data['username']) {
       document.getElementById("ntfyAuthentication").value = 'Basic auth';
       document.getElementById("ntfyUsername").value = data['username'];
       document.getElementById("ntfyPassword").value = data['password'];
    } else if (data['accesstoken']){
        document.getElementById("ntfyAuthentication").value = 'Access token';
        document.getElementById("ntfyAccessToken").value = data['accesstoken'];
    } else {
        document.getElementById("ntfyAuthentication").value = 'none';
    }

    assignNtfyAuthFields(document.getElementById("ntfyAuthentication").value);
}

function save(event) {
    document.getElementById('interval').readOnly = true;
    document.getElementById('save-0').hidden = true;
    document.getElementById('edit-0').removeAttribute('hidden');

    fetch("/api/settings/interval", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "interval": document.getElementById('interval').value
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById("add").value = "";
        document.getElementById("add").innerHTML = "Track";
        document.getElementById("add").classList.remove("disabled");
        document.getElementById("link").value = "";
        document.getElementById("price").value = "";
        document.getElementById("name").value = "";
        return fetch("/api/settings");
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        load(data);
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

function isInvalidUrl(url) {
    try {
        new URL(url);
        return false;
    } catch (err) {
        return true;
    }
}

function updateNtfy() {

    fetch("/api/notification", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "type": "ntfy",
            "url": document.getElementById("ntfyUrl").value,
            "topic": document.getElementById("ntfyTopic").value,
            "priority": document.getElementById("ntfyPriority").value,
            "username": document.getElementById('ntfyUsername').value,
            "password": document.getElementById('ntfyPassword').value,
            "token": document.getElementById('ntfyAccessToken').value,
            "enabled": document.getElementById("switchNtfy").checked
        })
    });
}

function handleNtfySwitch() {
    let enabled = document.getElementById("switchNtfy").checked;
    for (let element of document.getElementsByName("ntfy")) {
        element.disabled = !enabled;
    }
}

function assignNtfyAuthFields(authMethod) {
    let usernamePassword = document.getElementById("ntfyUsernamePassword");
    let accessToken = document.getElementById("div_ntfyAccessToken");
    if(authMethod === "none") {
        usernamePassword.hidden = true;
        accessToken.hidden = true;
    } else if (authMethod === "Basic auth") {
        usernamePassword.hidden = false;
        accessToken.hidden = true;
    } else if (authMethod === "Access token") {
        usernamePassword.hidden = true;
        accessToken.hidden = false;
    }
}

function addNtfyEventListener() {
    let ntfy = document.getElementById("switchNtfy");
    ntfy.addEventListener("click", function() {
        handleNtfySwitch();
    });

    let ntfyAuth = document.getElementById("ntfyAuthentication");
    ntfyAuth.addEventListener("change", function() {
        assignNtfyAuthFields(this.value);
    });

    let saveButton = document.getElementById("button-save-ntfy");
    saveButton.addEventListener("click", function() {
        let ntfyUrl = document.getElementById("ntfyUrl").value

        // TODO: give feedback if invalid
        if(isInvalidUrl(ntfyUrl)) {
            return;
        }
        updateNtfy();
    });
}

async function loadData() {
    let response = fetch("/api/settings");
    const scrapers = await response;
    return scrapers.json();
}

async function loadNtfy() {
    let response = fetch("/api/notification/ntfy");
    const ntfy = await response;
    return ntfy.json();
}

window.addEventListener('load', async _ => {
    let data = await loadData();
    createTable(data);
    addNtfyEventListener();
    let ntfyData = await loadNtfy();
    fillNtfyData(ntfyData);
    openWebsocket();
});

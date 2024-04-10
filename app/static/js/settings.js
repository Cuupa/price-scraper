import { html, tr, td, th, a, button, input, isEmpty } from "./modules/lib.js";
import { openWebsocket } from "./modules/websocket.js";
import { showSuccessPopup, showErrorPopup } from "./modules/notifications.js";

function createTable(data, status) {
    const tbody = document.querySelector("tbody");
    tbody.innerHTML = '';

    const interval = data['interval'];

    const _th = th('1');

    const interval_td = td('interval');
    interval_td.textContent = "interval";

    const _input = input(data['interval'], 'interval', 'number', true);
    const input_td = td();
    input_td.appendChild(_input);

    const edit_button = button('Edit', 'edit-0', 'btn', 'btn-primary', 'btn-sm');
    edit_button.addEventListener('click', function(event) {
        document.getElementById('interval').readOnly = false;
        document.getElementById('edit-0').hidden = true;
        document.getElementById('save-0').removeAttribute('hidden');
    });

    const save_button = button('Save', 'save-0', 'btn', 'btn-primary', 'btn-sm');
    save_button.setAttribute('hidden', 'true');
    save_button.addEventListener('click',save);
    const td_buttons = td();
    td_buttons.appendChild(edit_button);
    td_buttons.appendChild(save_button);

    const _tr = tr('0');
    _tr.appendChild(_th);
    _tr.appendChild(interval_td);
    _tr.appendChild(input_td);
    _tr.appendChild(td_buttons);

    tbody.appendChild(_tr);
}

function setNtfySwitchOff() {
    document.getElementById("switchNtfy").checked = false;
    document.getElementById("ntfyAuthentication").value = 'none';
    document.getElementById("ntfyPriority").value = '3';
    document.getElementsByName("ntfy").forEach(element => {
        element.disabled = true;
    });
}

function fillNtfyData(data) {
    if(isEmpty(data)) {
        setNtfySwitchOff();
    } else {
        document.getElementById("switchNtfy").checked = data.enabled;
        document.getElementById("ntfyUrl").value = data.url;
        document.getElementById("ntfyTopic").value = data.topic;
        document.getElementById("ntfyPriority").value = data.priority;

        if(data.username) {
           document.getElementById("ntfyAuthentication").value = 'Basic auth';
           document.getElementById("ntfyUsername").value = data.username;
           document.getElementById("ntfyPassword").value = data.password;
        } else if (data.accesstoken){
            document.getElementById("ntfyAuthentication").value = 'Access token';
            document.getElementById("ntfyAccessToken").value = data.accesstoken;
        } else {
            document.getElementById("ntfyAuthentication").value = 'none';
        }
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
            showErrorPopup("Error", "Could not loading settings");
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
            showErrorPopup("Error", "Could not loading settings");
            throw new Error('Network response was not ok');
        }
        showSuccessPopup("Saved", "Your settings have been saved");
        return response.json();
    })
    .then(data => {
        load(data);
    })
    .catch(error => {
        showErrorPopup("Error", "Could not loading settings");
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
    })
    .then(response => {
        if (!response.ok) {
            showErrorPopup("Error", "Could not load ntfy setttings");
            throw new Error('Network response was not ok');
        }
        showSuccessPopup("Saved", "Your settings have been saved");
    });
}

function handleNtfySwitch() {
    const enabled = document.getElementById("switchNtfy").checked;
    document.getElementsByName("ntfy").forEach(element => {
        element.disabled = !enabled;
    });
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
    const ntfy = document.getElementById("switchNtfy");
    ntfy.addEventListener("click", function() {
        handleNtfySwitch();
    });

    const ntfyAuth = document.getElementById("ntfyAuthentication");
    ntfyAuth.addEventListener("change", function() {
        assignNtfyAuthFields(this.value);
    });

    const saveButton = document.getElementById("button-save-ntfy");
    saveButton.addEventListener("click", function() {
        let ntfyUrl = document.getElementById("ntfyUrl").value

        // TODO: give feedback if invalid
        if(isInvalidUrl(ntfyUrl)) {
            return;
        }
        updateNtfy();
    });

    const testButton = document.getElementById("test-ntfy")
    testButton.addEventListener("click", function() {
        const url = document.getElementById("ntfyUrl").value + "/" + document.getElementById("ntfyTopic").value
        const username = document.getElementById('ntfyUsername').value;
        const password = document.getElementById('ntfyPassword').value
        const headers = {'Priority': document.getElementById("ntfyPriority").value};
        const authType = document.getElementById("ntfyAuthentication").value;

        if (authType === "Basic auth") {
            headers["Authorization"] = "Basic " + btoa(username + ":" + password);
        } else if (authType === "Access token") {
            headers["Authorization"] = "Bearer " + document.getElementById('ntfyAccessToken').value
        }

        fetch(url, {
            method: 'POST',
            body: 'Notification working',
            headers: headers
        });
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

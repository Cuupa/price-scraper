import { openWebsocket } from "./modules/websocket.js"

window.addEventListener('load', async _ => {
    let button = document.getElementById('button_profile_save');
    button.addEventListener('click', (event) => {
        let currentPassword = document.getElementById('currentPassword');
        let newPassword = document.getElementById('newPassword');
        let confirmPassword = document.getElementById('confirmPassword');
        let invalid = false;

        if(!currentPassword.value) {
            currentPassword.classList.add('is-invalid');
            invalid = true;
        }

        if(!newPassword.value) {
            newPassword.classList.add('is-invalid');
            invalid = true;
        }

        if(!confirmPassword.value) {
            confirmPassword.classList.add('is-invalid');
            invalid = true;
        }

        if(newPassword.value != confirmPassword.value) {
            invalid = true;
            newPassword.classList.add('is-invalid');
            confirmPassword.classList.add('is-invalid');
        } else {
            invalid = true;
            newPassword.classList.add('is-valid');
            confirmPassword.classList.add('is-valid');
        }

        if(!invalid) {
            fetch("/api/profile/password", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "currentPassword": currentPassword.value,
                    "newPassword": newPassword.value,
                    "confirmPassword": confirmPassword.value
                });
            })
        }
    });
});
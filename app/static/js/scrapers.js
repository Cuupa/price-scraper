import { html, tr, td, th, a, button } from "./modules/lib.js"
import { openWebsocket } from "./modules/websocket.js"

function createTable(data, status) {
    var tbody = document.querySelector("tbody");
    tbody.innerHTML = '';
    for (var i = 0; i < data.length; i++) {
        var cur = data[i];
        let _tr = tr(i);
        let _th = th(i+1);
        let name = td(cur.name);
        let url = td(cur.url);
        _tr.appendChild(_th);
        _tr.appendChild(name);
        _tr.appendChild(url);
        tbody.appendChild(_tr);
    }
}

async function loadData() {
    let response = fetch("/api/scrapers");
    const scrapers = await response;
    return scrapers.json();
}

window.addEventListener('load', async _ => {
    let data = await loadData();
    createTable(data['scrapers']);
    openWebsocket();
});

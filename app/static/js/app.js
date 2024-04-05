import { html, tr, td, th, a, button } from "./modules/lib.js"
import { openWebsocket } from "./modules/websocket.js"

function add(url, xpath_name, xpath_price) {
    fetch("/api/product", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "type": 'item',
            "url": url,
        })
    })
    .then(data => {
        document.getElementById("add").value = "";
        document.getElementById("add").innerHTML = "Track";
        document.getElementById("add").classList.remove("disabled");
        document.getElementById("link").value = "";
    });

    fetch("/api/products")
    .then(result => {
        return result.json();
    })
    .then(data => {
        load(data)
    });
}

function navigateToProduct(event) {
    let currentRow = event.target.closest('tr');
    window.location.href = "/product/" + currentRow.id;
}

 function createTable(data, status) {
    let tbody = document.querySelector("tbody");
    tbody.innerHTML = '';
    for (let i = 0; i < data['products'].length; i++) {
        let current = data['products'][i];
        let _tr = tr(current['id']);
        let _th = th(current['id']);
        _th.addEventListener('click', navigateToProduct);
        _tr.appendChild(_th);

        let name = td(current['name'], 'product-name');
        name.addEventListener('click', navigateToProduct);
        _tr.appendChild(name);

        let currentPrice = td(current['current_price'] + " " + current['currency']);
        currentPrice.addEventListener('click', navigateToProduct);
        _tr.appendChild(currentPrice);

        let lowestPrice = td(current['lowest_price'] + " " + current['currency']);
        lowestPrice.addEventListener('click', navigateToProduct);
        _tr.appendChild(lowestPrice);

        let link = a('a', 'Link', 'btn', 'btn-primary', 'btn-sm');

        let link_td = td();
        link_td.appendChild(link);
        _tr.appendChild(link_td);

        let _delete = button('Delete', 'delete-'+i, 'btn', 'btn-danger', 'btn-sm');
        _delete.addEventListener('click', attemptDelete)
        let delete_td = td();
        delete_td.appendChild(_delete);

        _tr.appendChild(delete_td);
        tbody.appendChild(_tr);
    }
 }

 function attemptDelete(event) {
    let currentRow = event.target.closest('tr');
    let rowId = currentRow.id;
    let productName = currentRow.querySelector('.product-name').textContent;

    Swal.fire({
        title: "Delete Element",
        text: "Delete item '" + productName + "'? This will include all historical data.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Delete"
    }).then((result) => {
        if (result.isConfirmed) {
            fetch('/api/product/' + rowId, {
                method: 'DELETE'
            })
            .then(response => {
                if(response.ok) {
                    let index = currentRow.rowIndex - 1;
                    document.querySelector("tbody").deleteRow(index);
                }
            });
        }
    });
 }

async function loadData() {
    let response = fetch("/api/products");
    const products = await response;
    return products.json();
}

window.addEventListener('load', async _ => {
    let button_add = document.getElementById("add");
    if(button_add) {
        button_add.addEventListener("click", (event) => {
            button_add.classList.add("disabled");
            button_add.innerHTML = 'Tracking...<div class="spinner-grow spinner-grow-sm" role="status"><span class="sr-only">Loading...</span></div>';
            link = document.getElementById("link");
            if(link && link.value != "") {
                add(link.value);
            }
            else {
                button_add.value = "";
                button_add.innerHTML = "Track";
                button_add.classList.remove("disabled");
            }
        });
    }

    let data = await loadData();
    createTable(data);
    openWebsocket();
});

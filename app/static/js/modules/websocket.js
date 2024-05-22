let ws

export function openWebsocket() {
    if( typeof(ws) == 'undefined' || ws.readyState === undefined || ws.readyState > 1) {
        let url = window.location.host + window.location.pathname + "websocket";
        let protocol = window.location.protocol === "http:" ? "ws:" : "wss:";
        let websocketUrl = protocol + "//" + url;
        ws = new WebSocket(websocketUrl);
        ws.addEventListener('open', function(msg) {
        });

        ws.addEventListener('error', function(msg) {
        });

        ws.addEventListener('close', function(msg) {
        });

        ws.addEventListener('message', function(event) {
           console.log(event);
           console.log(event.data);
           let message = JSON.parse(event.data);
           if(message.event == "change") {
              Swal.fire({
                 position: "top-end",
                 icon: "info",
                 title: "Update on product",
                 text: "Price of " + message.product + " has dropped to " + message.price,
                 showConfirmButton: false,
                 timer: 5000
              });
           }
        });
    }
}
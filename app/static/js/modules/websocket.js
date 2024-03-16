let ws

export function openWebsocket() {
    if( typeof(ws) == 'undefined' || ws.readyState === undefined || ws.readyState > 1){
        ws = new WebSocket("ws://localhost:5000/websocket");
        ws.addEventListener('open', function(msg) {
            console.log(msg);
        });

        ws.addEventListener('error', function(msg) {
            console.log(msg);
        });

        ws.addEventListener('close', function(msg) {
            console.log(msg);
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
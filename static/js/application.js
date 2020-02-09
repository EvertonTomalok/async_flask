
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/monitor');
    var numbers_received = [];

    socket.emit('cadastro', 1);

    // socket.on('disconnect', () => {
    //     socket.emit("dis", "Disconectando 1");
    // });

    // var new_socket = io.connect('http://' + document.domain + ':' + location.port + '/test1');

    //receive details from server
    socket.on('monitor', function(msg) {
        console.log("Received number" + msg.paciente);

        $('#log').html("<p>Na espera: " + msg.paciente + "</p>");
    });

});


$(document).ready(function(){

    setInterval(health,15000);
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/monitor');

    function health(){
        socket.emit("health", 1)
    }
});
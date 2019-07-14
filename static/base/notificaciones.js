class Notificador {

    constructor(sonido, selector, cantidadNotificaciones) {
        this.sonidoNotificacion = sonido;
        this.selector = selector;
        this.cantidadNotificaciones = cantidadNotificaciones;
    }

    insertarHtml(html) {
        $("#contenedor-notificaciones").empty()
        $("#contenedor-notificaciones").append(html)
    }

    notificar(cantidadNueva, html) {
        if (this.hayNotificaciones(cantidadNueva)) {
            this.actualizarNotificaciones(cantidadNueva)
            this.insertarHtml(html)
            this.reproducirSonido();
            this.mostrarCantidad(cantidadNueva);
        }
    }

    hayNotificaciones(cantidadNueva) {
        return this.cantidadNotificaciones != cantidadNueva
    }

    actualizarNotificaciones(cantidadNueva) {
        this.cantidadNotificaciones = cantidadNueva
    }

    reproducirSonido() {
    	this.sonidoNotificacion.play()
    }

    mostrarCantidad(cantidad) {
        this.selector.text(cantidad);
        this.selector.addClass("text-info");
    }

    leerNotificaciones() {
        this.cantidadNotificaciones = 0;
        this.vaciarCantidad();
    }

    vaciarCantidad() {
        this.selector.text(0);
        this.selector.removeClass();
    }
}


const XHTTP_LECTOR = new XMLHttpRequest();
const XHTTP_NOTIFICADOR = new XMLHttpRequest();
XHTTP_NOTIFICADOR.onreadystatechange = function() {
        json = JSON.parse(this.responseText);
        let cantidadNotificaciones = json['cantidad'];
        let html = json['notificaciones_html'];
        NOTIFICADOR.notificar(cantidadNotificaciones, html);
    };


setInterval(function() {
	XHTTP_NOTIFICADOR.open("GET", "/cantidadNotificacionesSinLeer");
    XHTTP_NOTIFICADOR.send();
}, 3000);


$("#campana").click(function() {
	XHTTP_LECTOR.open("GET", "/leerNotificaciones");
    XHTTP_LECTOR.send();
    NOTIFICADOR.leerNotificaciones();
});
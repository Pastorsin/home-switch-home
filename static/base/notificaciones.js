class Notificador {

    constructor(sonido, selector) {
        this.seNotifico = false
        this.sonidoNotificacion = sonido
        this.selector = selector
    }

    notificar(cantidadNotificaciones) {
        if ((cantidadNotificaciones > 0) && (!this.seNotifico)) {
            this.sonidoNotificacion.play();
        	this.seNotifico = true
            this.agregarCantidad(cantidadNotificaciones)
        }
    }

    agregarCantidad(cantidad) {
        this.selector.text(cantidad);
        this.selector.addClass("text-info");
    }

    leerNotificaciones() {
        this.vaciarCantidad()
        this.seNotifico = false
    }

    vaciarCantidad() {
        this.selector.text(0);
        this.selector.removeClass();
    }
}


// Inicializaciones

const SONIDO_NOTIFICACION = new Audio(SONIDO_NOTIFICACION_URL)
const SELECTOR_NOTIFICADOR = $('#notificador')
const NOTIFICADOR = new Notificador(SONIDO_NOTIFICACION, SELECTOR_NOTIFICADOR)

const XHTTP_LECTOR = new XMLHttpRequest()
const XHTTP_NOTIFICADOR = new XMLHttpRequest()
XHTTP_NOTIFICADOR.onreadystatechange = function() {
        cantidadNotificaciones = this.responseText
        NOTIFICADOR.notificar(cantidadNotificaciones)
    }


// Eventos

setInterval(function() {
	XHTTP_NOTIFICADOR.open("GET", "/cantidadNotificacionesSinLeer");
    XHTTP_NOTIFICADOR.send();
}, 3000);


$("#campana").click(function() {
	XHTTP_LECTOR.open("GET", "/leerNotificaciones");
    XHTTP_LECTOR.send()
    NOTIFICADOR.leerNotificaciones();
});
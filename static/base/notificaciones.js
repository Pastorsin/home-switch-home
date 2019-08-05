class Notificador {

    constructor(sonido, selector) {
        this.solicitudes = 0;
        this.seNotifico = false;
        this.sonidoNotificacion = sonido;
        this.selector = selector;
    }

    notificar(cantidadNotificaciones) {
        if ((cantidadNotificaciones > 0) && (!this.seNotifico)) {
        	this.seNotifico = true;
            this.reproducirSonido();
            this.incrementarSolicitudes();
            this.agregarCantidad(cantidadNotificaciones);
        }
    }

    reproducirSonido() {
    	if (this.solicitudes != 0) {
    		this.sonidoNotificacion.play()
    	}
    }

    incrementarSolicitudes() {
    	this.solicitudes += 1;
    }

    agregarCantidad(cantidad) {
        this.selector.text(cantidad);
        this.selector.addClass("text-info");
    }

    leerNotificaciones() {
        this.seNotifico = false;
        this.vaciarCantidad();
    }

    vaciarCantidad() {
        this.selector.text(0);
        this.selector.removeClass();
    }
}


// Inicializaciones

const SONIDO_NOTIFICACION = new Audio(SONIDO_NOTIFICACION_URL);
const SELECTOR_NOTIFICADOR = $('#notificador');
const NOTIFICADOR = new Notificador(SONIDO_NOTIFICACION, SELECTOR_NOTIFICADOR);

const XHTTP_LECTOR = new XMLHttpRequest();
const XHTTP_NOTIFICADOR = new XMLHttpRequest();
XHTTP_NOTIFICADOR.onreadystatechange = function() {
        cantidadNotificaciones = this.responseText;
        NOTIFICADOR.notificar(cantidadNotificaciones);
    };


// Eventos

setInterval(function() {
	XHTTP_NOTIFICADOR.open("GET", "/cantidadNotificacionesSinLeer");
    XHTTP_NOTIFICADOR.send();
}, 3000);


$("#campana").click(function() {
	XHTTP_LECTOR.open("GET", "/leerNotificaciones");
    XHTTP_LECTOR.send();
    NOTIFICADOR.leerNotificaciones();
});
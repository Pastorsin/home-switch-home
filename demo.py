import os
import sys
from django.db.utils import IntegrityError

sys.path.append('/is2/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'is2.settings'

import django
django.setup()

from residencias.models import Residencia, Ubicacion
from accounts.models import CustomUser
from adquisiciones.models import CompraDirecta, Subasta, NoDisponible
from datetime import datetime


def eliminar_todo():
    print('\033[33m[!] Limpiando tablas \033[0m')
    Ubicacion.objects.all().delete()
    Residencia.objects.all().delete()
    CustomUser.objects.exclude(username='grupo15').delete()
    CompraDirecta.objects.all().delete()
    Subasta.objects.all().delete()


def crear_usuarios():
    print('\033[33m[!] Creando usuarios \033[0m')

    try:
        # Estándar -> Mauro
        CustomUser.objects.create(
            username='mauromolina@gmail.com',
            password='mauromolina',
            foto='http://as00.epimg.net/img/comunes/fotos/fichas/equipos' +
            '/large/157.png',
            email='mauromolina@gmail.com',
            edad=20
        )

        print('\033[32m')
        print('[+] Usuario estándar creado')

        # Premium -> Andrés
        CustomUser.objects.create(
            username='andressmilla@gmail.com',
            password='andressmilla',
            foto='https://avatars2.githubusercontent.com/u/32437502?s=460&v=4',
            email='andressmilla@gmail.com',
            edad=20,
            es_premium=True
        )

        print('[+] Usuario premium creado')

        # Administrador -> Leonel
        CustomUser.objects.create(
            username='leonelmandarino@gmail.com',
            password='leonelmandarino',
            foto='https://avatars1.githubusercontent.com/u/32437504?s=460&v=4',
            email='leonelmandarino@gmail.com',
            edad=20,
            is_staff=True
        )

        print('[+] Usuario administrador creado')
        print('\033[0m')

    except IntegrityError:
        print('\033[35m[x] ERROR! Usuarios ya creados \033[0m')


def crear_residencias():
    print('\033[33m[!] Creando residencias \033[0m')

    # Terrazas al mar
    alte_brown_438 = Ubicacion.objects.create(pais='Argentina',
                                              provincia='Buenos Aires',
                                              ciudad='Carlos Casares',
                                              calle='Almirante Brown',
                                              numero=438
                                              )
    subasta_terrazas = Subasta.objects.create(precio_actual=9000,
                                              ganador_actual=CustomUser.objects.get(
                                              username='mauromolina@gmail.com')
                                              )
    Residencia.objects.create(nombre='Terrazas al Mar',
                              foto='http://www.gsr.coop/gsr/usuariosFtp/conexion/imagenes69a.jpg',
                              precio_base='9000',
                              descripcion='Hermosa residencia con 4 habitaciones.',
                              ubicacion=alte_brown_438,
                              estado=subasta_terrazas
                              )

    # Villa del sur
    zola_1622 = Ubicacion.objects.create(pais='Argentina',
                                              provincia='Buenos Aires',
                                              ciudad='Quilmes',
                                              calle='Zola',
                                              numero=1622
                                         )
    subasta_villa_del_sur = Subasta.objects.create(precio_actual=9000)
    Residencia.objects.create(nombre='Villa del Sur',
                              foto='https://static.miweb.padigital.es/var/m_d/df/df8/54841/779667-banner-Fotoportada-02.jpg',
                              precio_base='9000',
                              descripcion='Residencia con jardín y espacio para chicos.',
                              ubicacion=zola_1622,
                              estado=subasta_villa_del_sur
                              )

    # Mayor a 6 meses
    calle_123 = Ubicacion.objects.create(pais='Argentina',
                                              provincia='Buenos Aires',
                                              ciudad='Berazategui',
                                              calle='Calle',
                                              numero=123
                                         )
    compra_directa = CompraDirecta.objects.create()
    Residencia.objects.create(nombre='La casa de Mauro',
                              foto='https://www.barcelonacheckin.com/img/stored_images/barcelona/articles/casa-messi.jpg',
                              precio_base='9000',
                              descripcion='Residencia con gran espacio para correr. Lionel Messi estuvo aquí.',
                              ubicacion=calle_123,
                              estado=compra_directa,
                              fecha_publicacion=datetime(2015, 6, 6)
                              )

    # Menor a 6 meses
    calle_124 = Ubicacion.objects.create(pais='Argentina',
                                              provincia='Buenos Aires',
                                              ciudad='Berazategui',
                                              calle='Calle',
                                              numero=124
                                         )
    compra_directa = CompraDirecta.objects.create()
    Residencia.objects.create(nombre='La casa de Rodri',
                              foto='http://wrmx00.epimg.net/radio/imagenes/2017/08/28/nacional/1503951732_747029_1503952706_noticia_normal.jpg',
                              precio_base='9000',
                              descripcion='Residencia con espacio minucioso, ideal para pasar tiempo con familia.',
                              ubicacion=calle_124,
                              estado=compra_directa,
                              fecha_publicacion=datetime(2019, 5, 1)
                              )

    # En espera
    calle_64 = Ubicacion.objects.create(pais='Argentina',
                                        provincia='Buenos Aires',
                                        ciudad='Berazategui',
                                        calle='Calle',
                                        numero=64
                                        )
    no_disponible = NoDisponible.objects.create()
    Residencia.objects.create(nombre='La casa de Hugo',
                              foto='https://www.elprogreso.es/media/elprogreso/images/2018/10/14/2018101415042744345.jpg',
                              precio_base='9000',
                              descripcion='Residencia con apertura al mar.',
                              ubicacion=calle_64,
                              estado=no_disponible,
                              fecha_publicacion=datetime(1998, 12, 3)
                              )


def main():
    eliminar_todo()
    crear_usuarios()
    crear_residencias()


if __name__ == '__main__':
    main()

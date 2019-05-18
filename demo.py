import os
import sys
from django.db.utils import IntegrityError

sys.path.append('/is2/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'is2.settings'


def inicializar():
    import django
    django.setup()


def crear_usuarios():
    from accounts.models import CustomUser

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


def main():
    inicializar()
    crear_usuarios()


if __name__ == '__main__':
    main()

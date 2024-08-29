from django.core.management.base import BaseCommand
from main.services import obtener_propiedades_por_comuna

## Modo de uso en la consola: python manage.py consulta_inmuebles -f nombreDelInmueble_o_algo_de_la_descripcion
# Si existe coincidencia crea un txt con la informacion basica del inmueble

class Command(BaseCommand):
    help = 'Busca todos los inmuebles de una segun filtro busca en su descripcion o nombre'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--f', type=str, nargs='+')

    def handle(self, *args, **kwargs):
        filtro = None
        if 'f' in kwargs.keys() and kwargs['f'] is not None:
            filtro = kwargs['f'][0]

        inmuebles = obtener_propiedades_por_comuna(filtro)

        for inmueble in inmuebles:
            self.stdout.write(f"Nombre: {inmueble.nombre}, Descripción: {inmueble.descripcion}")


    
        # Abrir el archivo en modo escritura
        with open('data/consulta_inmuebles.txt', 'w', encoding='utf-8') as file:
            # Iterar sobre las propiedades y escribirlas en el archivo
            for inmueble in inmuebles:
                linea=f'{inmueble.nombre}\t{inmueble.descripcion}\t{inmueble.comuna.nombre}\n'
                file.write(linea)

        print(f"Propiedades guardadas en data/inmuebles_comuna.txt")






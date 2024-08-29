import os
from django.core.management.base import BaseCommand
from main.services import obtener_propiedades_por_region

#python manage.py consulta_propiedades_por_region -n "Metropolitana" tambien 
#se puede usar sin -n ni fragmento de region y nos da todas las propiedades


class Command(BaseCommand):
    help = 'Consulta propiedades por nombre parcial de la región y guarda los resultados en un archivo'

    def add_arguments(self, parser):
        parser.add_argument(
            '-n', '--nombre_region_parcial',
            type=str,
            nargs='?',
            default=None,
            help='Nombre parcial de la región para consultar (opcional)'
        )

    def handle(self, *args, **kwargs):
        nombre_region_parcial = kwargs.get('nombre_region_parcial')
        
        try:
            # Obtener las propiedades según el filtro proporcionado
            propiedades = obtener_propiedades_por_region(nombre_region_parcial)

            # Asegurar que el directorio 'data' exista
            os.makedirs('data', exist_ok=True)

            # Abrir el archivo en modo escritura
            with open('data/propiedades_por_region.txt', 'w', encoding='utf-8') as file:
                for propiedad in propiedades:
                    linea = (
                        f'Nombre: {propiedad.nombre}\t'
                        f'Descripción: {propiedad.descripcion}\t'
                        f'Comuna: {propiedad.comuna.nombre}\t'
                        f'Región: {propiedad.comuna.region.nombre}\n'
                    )
                    file.write(linea)

            # Mensaje de éxito dependiendo del filtro
            if nombre_region_parcial:
                mensaje = (
                    f'Propiedades de la región que contiene "{nombre_region_parcial}" '
                    f'guardadas en data/propiedades_por_region.txt'
                )
            else:
                mensaje = 'Todas las propiedades guardadas en data/propiedades_por_region.txt'

            self.stdout.write(self.style.SUCCESS(mensaje))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ocurrió un error: {e}'))

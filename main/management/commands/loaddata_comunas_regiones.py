import csv
from django.core.management.base import BaseCommand
from main.models import Comuna, Region

class Command(BaseCommand):
    help = 'Importa comunas y regiones desde un archivo CSV'

    def handle(self, *args, **kwargs):
        with open('data/comunas_regiones_chile.csv', newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Verificar si la región ya existe, si no, crearla
                region, created = Region.objects.get_or_create(
                    cod=row['cod_region'],
                    defaults={'nombre': row['region']}
                )
                
                # Crear la comuna y asociarla a la región
                Comuna.objects.create(
                    cod=row['cod_comuna'],
                    nombre=row['comuna'],
                    region=region
                )

        self.stdout.write(self.style.SUCCESS('Comunas y regiones importadas exitosamente'))

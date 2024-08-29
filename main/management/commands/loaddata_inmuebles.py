from django.core.management.base import BaseCommand
import csv
from django.core.exceptions import ValidationError
from django.db import transaction
from main.models import Inmueble, Comuna
from django.contrib.auth.models import User

# Ruta al archivo CSV
CSV_FILE_PATH = 'data/inmuebles.csv'

class Command(BaseCommand):
    help = 'Importar inmuebles desde un archivo CSV'

    def handle(self, *args, **kwargs):
        with open(CSV_FILE_PATH, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                try:
                    # Obtener la comuna
                    comuna = Comuna.objects.get(cod=row['comuna_cod'])

                    # Obtener el propietario (User) por RUT
                    propietario = User.objects.get(username=row['propietario_rut'])

                    with transaction.atomic():
                        # Crear el inmueble
                        inmueble = Inmueble.objects.create(
                            nombre=row['nombre'],
                            descripcion=row['descripcion'],
                            m2_construidos=int(row['m2_construidos']),
                            m2_totales=int(row['totales']),
                            num_estacionamientos=int(row['num_estacionamientos']),
                            num_habitaciones=int(row['num_habitaciones']),
                            num_baños=int(row['num_banos']),
                            direccion=row['direccion'],
                            precio_mensual_arriendo=int(row['precio_mensual_arriendo']),
                            tipo_de_inmueble=row['tipo_inmueble'],
                            comuna=comuna,
                            propietario=propietario
                        )

                        self.stdout.write(self.style.SUCCESS(f"Inmueble {inmueble.nombre} creado exitosamente."))

                except Comuna.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Error: La comuna con código {row['comuna_cod']} no existe."))
                except User.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Error: El propietario con RUT {row['propietario_rut']} no existe."))
                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f"Error al crear el inmueble {row['nombre']}: {e}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error inesperado al crear el inmueble {row['nombre']}: {e}"))

from django.core.management.base import BaseCommand
import csv
from django.contrib.auth.models import User
from main.models import UserProfile
from django.core.exceptions import ValidationError
from django.db import transaction

class Command(BaseCommand):
    help = 'Importar usuarios desde un archivo CSV'

    def handle(self, *args, **kwargs):
        csv_file_path = 'data/usuarios.csv'

        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                # Validar que las contraseñas coinciden
                if row['password'] != row['pass_confirm']:
                    self.stdout.write(self.style.ERROR(f"Error: Las contraseñas no coinciden para {row['correo']}"))
                    continue

                # Verificar si el usuario ya existe
                if User.objects.filter(username=row['rut']).exists():
                    self.stdout.write(self.style.ERROR(f"Error: El usuario con RUT {row['rut']} ya existe."))
                    continue

                try:
                    with transaction.atomic():
                        # Crear el usuario
                        user = User.objects.create_user(
                            username=row['rut'],
                            first_name=row['nombres'],
                            last_name=row['apellidos'],
                            email=row['correo'],
                            password=row['password']
                        )

                        # Crear el perfil de usuario
                        user_profile = UserProfile.objects.create(
                            user=user,
                            direccion=row['direccion'],
                            telefono_personal=row['telefono'],
                            rol=row['tipo_usuario']
                        )

                        self.stdout.write(self.style.SUCCESS(f"Usuario {user.username} creado exitosamente."))

                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f"Error al crear el usuario {row['correo']}: {e}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error inesperado al crear el usuario {row['correo']}: {e}"))

from django.core.management.base import BaseCommand
from datetime import datetime
from .models import Tramite

class Command(BaseCommand):
    help = 'Rechaza automáticamente los trámites cuya fecha de respuesta coincide con la fecha actual'

    def handle(self, *args, **options):
        print('asasasassaasasasas')
        fecha_actual = datetime.now().date()

        # Filtrar los trámites con fecha de respuesta igual a la fecha actual
        tramites_a_rechazar = Tramite.objects.filter(fecha_respuesta=fecha_actual)

        # Actualizar el estado de los trámites a "rechazado"
        tramites_a_rechazar.update(estado='rechazado')
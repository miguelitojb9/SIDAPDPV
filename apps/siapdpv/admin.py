from django.contrib import admin
from .models import Queja, Demanda, Solicitud, Nota, Documento, Tramite
from ..customUser.models import Organismo, Departamento


class QuejaAdmin(admin.ModelAdmin):
    # Personaliza la visualización y el comportamiento de Queja en el administrador
    pass

class DenunciaAdmin(admin.ModelAdmin):
    # Personaliza la visualización y el comportamiento de Denuncia en el administrador
    pass

class SolicitudAdmin(admin.ModelAdmin):
    # Personaliza la visualización y el comportamiento de Solicitud en el administrador
    pass

class NotaAdmin(admin.ModelAdmin):
    # Personaliza la visualización y el comportamiento de Nota en el administrador
    pass

class DocumentoAdmin(admin.ModelAdmin):
    # Personaliza la visualización y el comportamiento de Documento en el administrador
    pass

class OrganismoAdmin(admin.ModelAdmin):
    # Personaliza la visualización y el comportamiento de Organismo en el administrador
    pass

class DepartamentoAdmin(admin.ModelAdmin):
    # Personaliza la visualización y el comportamiento de Departamento en el administrador
    pass

class TramiteAdmin(admin.ModelAdmin):
    # Personaliza la visualización y el comportamiento de Tramite en el administrador
    pass


admin.site.register(Queja, QuejaAdmin)
admin.site.register(Demanda, DenunciaAdmin)
admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(Nota, NotaAdmin)
admin.site.register(Documento, DocumentoAdmin)
admin.site.register(Organismo, OrganismoAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Tramite, TramiteAdmin)
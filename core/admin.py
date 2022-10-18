from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.admin.utils import quote
from django.contrib.admin.views.main import ChangeList

import core.models



class LogEntryAdmin(admin.ModelAdmin):
    readonly_fields = ('content_type',
        'user',
        'action_time',
        'object_id',
        'object_repr',
        'action_flag',
        'change_message'
    )
    list_display = ('action_flag', 'action_time', 'user', 'change_message', 'object_repr', 'object_id')


    def has_delete_permission(self, request, obj=None):
        return False

    # def get_actions(self, request):
    #     actions = super(LogEntryAdmin, self).get_actions(request)
    #     del actions['delete_selected']
    #     return actions


class ProyectoChangeList(ChangeList):
    def url_for_result(self, result):
        return '/proyectodnd/%d/' % (quote(result.pk))

    def get_model(self):
        return self.model.__name__

class ProyectoModelAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)
    list_display = ('nombre', 'pensum', 'lapso_academico', 'creado', 'update',)
    list_filter = ('pensum',)

    def get_changelist(self, request, **kwargs):
        return ProyectoChangeList

class DocenteModelAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'cedula')
    list_display = ('nombres', 'apellidos', 'cedula', 'email')

class AulaModelAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'numero', 'carrera', 'ubicacion')
    list_display = ('nombre', 'tipo_aula', 'numero', 'ubicacion', 'carrera',)

class MateriaModelAdmin(admin.ModelAdmin):
    search_fields = ('codigo', 'nombre')
    list_display = ('codigo', 'nombre', 'pensum', 'semestre',)

class SeccionModelAdmin(admin.ModelAdmin):
    search_fields = ('numero', 'materia')
    list_display = ('docente', 'numero', 'materia', 'proyecto',)
    list_filter = ('proyecto',)

class CarreraModelAdmin(admin.ModelAdmin):
    search_fields = ('numero', 'materia')
    list_display = ('docente', 'numero', 'materia', 'proyecto',)
    list_filter = ('proyecto',)
    list_filter = ('proyecto',)

class EncuentroModelAdmin(admin.ModelAdmin):
    search_fields = ('seccion__materia__nombre', 'aula__nombre')
    list_display = ('bloque', 'aula', 'seccion', 'tipo', 'activo',)
    list_filter = ('seccion__materia', 'tipo', 'seccion__proyecto')


admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(core.models.Proyecto, ProyectoModelAdmin)
admin.site.register(core.models.Docente, DocenteModelAdmin)
admin.site.register(core.models.Aula, AulaModelAdmin)
admin.site.register(core.models.Materia, MateriaModelAdmin)
admin.site.register(core.models.Seccion, SeccionModelAdmin)
admin.site.register(core.models.Encuentro, EncuentroModelAdmin)


for modelo in dir(core.models):
    if getattr(core.models, modelo).__class__.__name__ == 'ModelBase' and getattr(core.models, modelo).__name__ not in ['User']:
        try:
            admin.site.register(getattr(core.models, modelo))
        except:
            pass
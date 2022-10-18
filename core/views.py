# -*- coding: utf-8 -*-

import datetime
import json
import os
from itertools import groupby

import pdfkit
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.views.generic import TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

from .models import *


class DashboardRedirectView(TemplateView):
    template_name = 'dashboard.html'

    def get(self, *args, pk=None, **kwargs):
        return HttpResponseRedirect('/admin/core/proyecto/')

    def get_context_data(self, *args, **kwargs):
        data = super(DashboardView, self).get_context_data(*args, **kwargs)
        data['lapsos'] =  LapsoAcademico.objects.all()
        if self.request.user.is_superuser:
            data['pensums'] =  Pensum.objects.all()
        else:
            carreras_pks = AsistentesCarrera.objects.filter(asistente=self.request.user).values_list('carrera__pk', flat=True)
            data['pensums'] =  Pensum.objects.filter(carrera__pk__in=carreras_pks)
        return data      

class ProyectoEditDragDropView(TemplateView):
    template_name = 'proyecto_edit_drag_drop.html'

    def get(self, *args, pk=None, **kwargs):
        self.proyecto = Proyecto.objects.filter(pk=pk).first()
        if self.proyecto:
            return super(ProyectoEditDragDropView, self).get(*args, **kwargs)
        return HttpResponse(status=404)
            
    def get_context_data(self, *args, **kwargs):
        data = super(ProyectoEditDragDropView, self).get_context_data(*args, **kwargs)
        data['secciones'] = Seccion.objects.filter(proyecto=self.proyecto)
        data['aulas'] = Aula.objects.filter(carrera=self.proyecto.pensum.carrera).order_by('nombre')
        data['docentes'] = Docente.objects.filter(carrera=self.proyecto.pensum.carrera).order_by('nombres')
        data['tipos_encuentros'] = (
            ('pr', 'Presencial'),
            ('vi', 'Virtual'),
        )        
        data['proyecto'] = self.proyecto.pk
        data['nombre_proyecto'] = self.proyecto.nombre
        data['carrera'] = self.proyecto.pensum.carrera.pk
        data['lapsos'] =  LapsoAcademico.objects.all()
        if self.request.user.is_superuser:
            data['pensums'] =  Pensum.objects.all()
        else:
            carreras_pks = AsistentesCarrera.objects.filter(asistente=self.request.user).values_list('carrera__pk', flat=True)
            data['pensums'] =  Pensum.objects.filter(carrera__pk__in=carreras_pks)
        return data


class ProyectoEditView(TemplateView):
    template_name = 'proyecto_edit.html'

    def get(self, *args, **kwargs):
        if Proyecto.objects.filter(pk=kwargs['pk']).exists():
            self.proyecto = Proyecto.objects.get(pk=kwargs['pk'])
            return super(ProyectoEditView, self).get(*args, **kwargs)
        return HttpResponseRedirect('/')

    def get_context_data(self, *args, **kwargs):
        data = super(ProyectoEditView, self).get_context_data(*args, **kwargs)
        data['proyecto'] = self.proyecto
        data['form_errors'] = self.request.session.pop('form_errors', False)
        data['form_data'] = self.request.session.pop('form_data', False)
        data['mostrar_modal'] = self.request.session.pop('mostrar_modal', False)
        if not data['form_data'] and self.request.session.get('update_form_data', False):
            data['form_data'] = self.request.session.pop('update_form_data', False)
            data['update_action'] = True
        if data['mostrar_modal'] == 'encuentro_create':
            data['seccion_encuentro'] = self.request.session.pop('seccion_encuentro')
            data['encuentros_dias'] = EncuentrosDias.objects.filter(encuentro__seccion__pk=data['seccion_encuentro'])
        data['secciones'] = Seccion.objects.filter(proyecto=self.proyecto)
        data['bloques'] = Bloque.objects.filter()
        data['aulas'] = Aula.objects.all()
        data['dias'] = Dia.objects.all()
        data['tipos_encuentros'] = (
            ('pr', 'Presencial'),
            ('vi', 'Virtual'),
        )
        data['todas_materias_pertinentes'] = Materia.objects.all()
        # @TODO: filtrar docentes por area aqui
        data['todos_docentes_pertinentes'] = Docente.objects.all()
        data['turnos'] = Turno.objects.all()
        data['pensums'] = Pensum.objects.all()
        data['pk_pensum_mas_reciente'] = getattr(Pensum.objects.last(), 'pk', '')
        return data

class ProyectoCreateView(CreateView):
    template_name = 'proyecto_edit.html'
    model = Proyecto
    fields = '__all__'

    def get_success_url(self, *args, **kwargs):
        return '/proyecto/%s/' % self.object.pk  

class SeccionCreateView(CreateView):
    template_name = 'proyecto_edit.html'
    model = Seccion
    fields = '__all__'

    def get_success_url(self, *args, **kwargs):
        return '/proyecto/%s/' % self.object.proyecto.pk

    def form_invalid(self, form, **kwargs):
        self.request.session['mostrar_modal'] = 'seccion_create'
        self.request.session['form_errors'] = dict(form.errors)
        self.request.session['form_data'] = dict(form.data)
        return HttpResponseRedirect('/proyecto/%s/' % dict(form.data)['proyecto'][0])

class ConfirmacionEliminacionSeccionView(TemplateView):
    template_name = 'seccion_confirm_delete.html'

class SeccionDeleteView(View):
    model = Seccion

    def get(self, *args, **kwargs):
        if 'pk' in kwargs and self.model.objects.filter(pk=kwargs['pk']).exists():
            self.object = self.model.objects.get(pk=kwargs['pk'])
            proyecto = self.object.proyecto.pk
            self.object.delete()
            return HttpResponseRedirect('/proyecto/%s/' % proyecto  ) 
        return HttpResponseRedirect('/')

class SeccionUpdateView(UpdateView):
    model = Seccion
    fields = '__all__'

    def get(self, *args, **kwargs):
        def is_serializable(x):
            try:
                json.dumps(x)
                return True
            except:
                return False        

        if 'pk' in kwargs and self.model.objects.filter(pk=kwargs['pk']).exists():
            seccion = self.model.objects.get(pk=kwargs['pk'])
            self.request.session['update_form_data'] = {key:[value] for key, value in seccion.__dict__.items() if is_serializable(value)}
            self.request.session['mostrar_modal'] = 'seccion_create'
            return HttpResponseRedirect('/proyecto/%s/' % seccion.proyecto.pk  ) 
        return HttpResponseRedirect('/')

    def get_success_url(self, *args, **kwargs):
        return '/proyecto/%s/' % self.object.proyecto.pk


class EncuentroCreateView(CreateView):
    template_name = 'proyecto_edit.html'
    model = Encuentro
    fields = '__all__'

    def get_success_url(self, *args, **kwargs):
        self.request.session['mostrar_modal'] = 'encuentro_create'
        self.request.session['seccion_encuentro'] = self.object.seccion.pk
        return '/proyecto/%s/' % self.object.seccion.proyecto.pk

    def form_valid(self, form, **kwargs):
        res = super(EncuentroCreateView, self).form_valid(form, **kwargs)
        EncuentrosDias.objects.create(encuentro=self.object, dia=Dia.objects.get(pk=form.data['dia'][0]))
        return res


    def form_invalid(self, form, **kwargs):
        seccion = Seccion.objects.get(pk=dict(form.data)['seccion'][0])
        self.request.session['mostrar_modal'] = 'encuentro_create'
        self.request.session['seccion_encuentro'] = seccion.pk
        self.request.session['form_errors'] = dict(form.errors)
        self.request.session['form_data'] = dict(form.data)
        return HttpResponseRedirect('/proyecto/%s/' % seccion.proyecto.pk)

class SeccionEncuentrosListView(TemplateView):
    template_name = 'proyecto_edit.html'

    def get(self, *args, **kwargs):
        self.request.session['mostrar_modal'] = 'encuentro_create'
        self.request.session['seccion_encuentro'] = self.request.GET.get('seccion')
        return HttpResponseRedirect('/proyecto/%s/' % self.request.GET.get('seccion'))





# class EncuentroUpdateView(UpdateView):
#     model = Seccion
#     fields = '__all__'

#     def get(self, *args, **kwargs):
#         def is_serializable(x):
#             try:
#                 json.dumps(x)
#                 return True
#             except:
#                 return False        

#         if 'pk' in kwargs and self.model.objects.filter(pk=kwargs['pk']).exists():
#             seccion = self.model.objects.get(pk=kwargs['pk'])
#             self.request.session['update_form_data'] = {key:[value] for key, value in seccion.__dict__.items() if is_serializable(value)}
#             return HttpResponseRedirect('/proyecto/%s/' % seccion.proyecto.pk  ) 
#         return HttpResponseRedirect('/')

#     def get_success_url(self, *args, **kwargs):
#         return '/proyecto/%s/' % self.object.proyecto.pk           


@method_decorator(csrf_exempt, name='dispatch')
class EncuentrosAPIUpdateView(View):
    def post(self, request, *args, **kwargs):
        obj = EncuentrosDias.objects.get(pk=request.POST['pk'])
        if 'docente' in request.POST:
            obj.encuentro.seccion.docente = Docente.objects.get(pk=request.POST['docente'])
            obj.encuentro.aula = Aula.objects.get(pk=request.POST['aula'])
            obj.encuentro.tipo = request.POST['tipo']
            obj.encuentro.seccion.cupo = request.POST['cupo']
            obj.encuentro.seccion.save()
            obj.encuentro.save()
        else:
            hora_inicio, minutos_inicio, segundos_inicio = map(int, request.POST['hora_inicio'].split(':'))
            dia = Dia.objects.get(pk=request.POST['dia'])
            bloque = Bloque.objects.get(hora_inicio=datetime.time(hour=hora_inicio, minute=minutos_inicio, second=segundos_inicio))
            obj.encuentro.bloque = bloque
            obj.encuentro.save()
            obj.dia = dia
            obj.encuentro.aula = Aula.objects.get(pk=request.POST['aula'])
            obj.encuentro.save()
            obj.save()
        return HttpResponse()


class EncuentrosAPIListView(View):

    def get(self, request, *args, **kwargs):
        # @TODO: validar que el usuario logueado tenga permiso a acceder a los datos del proyecto
        filtros = {}
        if 'proyecto' in request.GET:
            filtros['encuentro__seccion__proyecto__pk'] = request.GET['proyecto']
        if 'aula' in request.GET:
            filtros['encuentro__aula'] = request.GET['aula']
        objetos = EncuentrosDias.objects.filter(**filtros).all()
        objetos = sorted(objetos, key=lambda x: (x.encuentro.bloque.hora_inicio, x.dia.dia))
        datos = [
            {
                "pk": x.encuentro.pk,
                "encuentro_dia_pk": x.pk,
                "tipo": x.encuentro.tipo,
                "numero_bloques": x.encuentro.numero_bloques,
                "dia": x.dia.get_dia_display(),
                "dia_pk": x.dia.dia,
                "seccion": {
                    "pk": x.encuentro.seccion.pk,
                    "numero": x.encuentro.seccion.numero,
                    "docente": x.encuentro.seccion.docente.nombres,
                    "docente_nombre_apellido": x.encuentro.seccion.docente.nombre_apellido,
                    "docente_pk": x.encuentro.seccion.docente.pk,
                    "cupo": x.encuentro.seccion.cupo,
                    "materia": {
                        "pk": x.encuentro.seccion.materia.pk,
                        "codigo": x.encuentro.seccion.materia.codigo,
                        "nombre": x.encuentro.seccion.materia.nombre,
                        "pensum": x.encuentro.seccion.materia.pensum.nombre,
                    },
                },
                "aula": {
                    "pk": x.encuentro.aula.pk,
                    "numero": x.encuentro.aula.numero,
                    "nombre": x.encuentro.aula.nombre,
                    "tipo": x.encuentro.aula.tipo_aula.modalidad,
                    "ubicacion": x.encuentro.aula.ubicacion.nombre,
                },
                "bloque": {
                    "pk": x.encuentro.bloque.pk,
                    "hora_inicio": str(x.encuentro.bloque.hora_inicio),
                    "esquema_bloque": {
                        "pk": x.encuentro.bloque.esquema_bloque.pk,
                        "duracion": str(x.encuentro.bloque.esquema_bloque.duracion),
                        # "tipo_encuentro": x.encuentro.bloque.esquema_bloque.tipo_encuentro,
                        "carrera": {
                            "pk": x.encuentro.bloque.esquema_bloque.carrera.pk,
                            "nombre": x.encuentro.bloque.esquema_bloque.carrera.nombre,
                        },
                    },
                },


            }
            for x in objetos
        ]
        datos = json.dumps(datos, indent=2)
        return HttpResponse(datos, content_type='application/json')

class AulasAPIListView(View):

    def get(self, request, *args, **kwargs):
        # @TODO: validar que el usuario logueado tenga permiso a acceder a los datos
        filtros = {}
        if 'carrera' in request.GET:
            filtros['carrera'] = request.GET['carrera']
        objetos = Aula.objects.filter(**filtros).order_by('numero')
        datos = {
                x.pk: {
                    "pk": x.pk,
                    "numero": x.numero,
                    "nombre": x.nombre,
                    "tipo": x.tipo_aula.modalidad,
                    "ubicacion": x.ubicacion.nombre,
                }
                for x in objetos
        }
        datos = json.dumps(datos, indent=2)
        return HttpResponse(datos, content_type='application/json')        

class BloquesAPIListView(View):

    def get(self, request, *args, **kwargs):
        # @TODO: validar que el usuario logueado tenga permiso a acceder a los datos
        filtros = {}
        if 'carrera' in request.GET:
            objetos = Bloque.objects.filter(esquema_bloque__carrera=request.GET['carrera']).order_by('hora_inicio').all()
            datos = [
                {
                    "pk": x.pk,
                    "hora_inicio": str(x.hora_inicio),
                    "representacion": str(x),
                    "turno": x.turno.nombre,
                }
                for x in objetos
            ]
            datos = json.dumps(datos, indent=2)
            return HttpResponse(datos, content_type='application/json')
        return HttpResponseBadRequest()

class DiasAPIListView(View):

    def get(self, request, *args, **kwargs):
        # @TODO: validar que el usuario logueado tenga permiso a acceder a los datos
        filtros = {}
        if 'carrera' in request.GET:
            objetos = Dia.objects.filter(esquema_dia__carrera=request.GET['carrera']).all()
            datos = [
                {
                    "pk": x.pk,
                    "numero": x.dia,
                    "dia": str(x),
                }
                for x in objetos
            ]
            datos = json.dumps(datos, indent=2)
            return HttpResponse(datos, content_type='application/json')
        return HttpResponseBadRequest()


def group_by(object_list, key=None, sort_by=None):
    object_list = sorted(object_list, key=key)
    data = {}
    for key, group in groupby(object_list, key):
        if sort_by is None:
            data[key] = list(group)
        else:
            data[key] = sorted(list(group), key=sort_by)
        print("Objects of:", key, "Number:", len(list(group)))
    return data  


class ReporteSemestresView(TemplateView):
    template_name = 'reporte_por_semestres.html'



    def generar_html_reporte2(self):
        proyecto = Proyecto.objects.get(id=self.kwargs.get('proyecto_id'))
        secciones = Seccion.objects.filter(proyecto=proyecto).all()
        semestres_ordenados = sorted(set(secciones.values_list('materia__semestre', flat=True)))
        secciones_agrupadas_por_semestre = group_by(secciones, key=lambda x: x.materia.semestre)

        html = '''<html> <head> <meta charset="utf-8"> <title></title>
<style>

table.horario td, th{
    border:  1px solid black !important;
    outline: 1px solid black !important;
    width: auto !important;
    height:.4cm !important;
    min-height: 10px !important;
    padding: 3px;
    margin:1px;
    background: #ffffff !important;
  }

  table.horario td {
    height: 100px !important;

  }

  table.header {
    width: 100%;
  }

    @media print {
      .nueva-pagina {
        page-break-before: always;
      }
    }

    .horario th:nth-child(1) {
        width: 1% !important;

    }
    .horario td:nth-child(1) {
        width: 1% !important;

    }    


</style>
</head> <body>'''


        pages_header = """<table class="header">
    <tr>
        <td><img style="width:200px;height:90px;display:inline-block;" src="{base_dir}/core/static/img/logo_ais.jpg"></td>
        <td>
<strong>{institucion}</strong><br>
<strong>{area}</strong><br>
<strong>Programa: Ingeniería en Informática</strong><br>
<strong>Lapso Académico: {lapso}</strong><br>
<strong>Comisión de Horarios Académicos</strong><br>
        </td>

    </tr>

</table>
<hr>
<center><h3>Resúmen de Horarios Semanales<br>{semestre}° Semestre</h3></center>"""



        es_primera_pagina_reporte = True
        for semestre in semestres_ordenados:
            if not es_primera_pagina_reporte:
                html += '<div class="nueva-pagina"></div>'
            es_primera_pagina_reporte = False
            html += pages_header.format(
                base_dir=settings.BASE_DIR,
                semestre=semestre,
                lapso='2019-2',
                area='Área de Ingeniería de Sistémas',
                institucion='Universidad Nacional Experimental Rómulo Gallegos'
             )
            html += '<table class="horario"> <thead><th>Sección</th>'
            secciones_de_semestre = secciones_agrupadas_por_semestre[semestre]
            # secciones_de_semestre_agrupado_por_num_seccion_ord_por_nom_mat = group_by(secciones_de_semestre, key=lambda x: x.numero, sort_by=lambda x: x.materia.nombre)
            secciones_de_semestre_agrupado_por_num_seccion = group_by(secciones_de_semestre, key=lambda x: x.numero)
            secciones_de_semestre_ord_por_num_seccion = sorted(secciones_de_semestre_agrupado_por_num_seccion.keys())


            # secciones_agrupadas_por_materia_ord_por_num_seccion = group_by(secciones_de_semestre, key=lambda x: x.materia.pk, sort_by=lambda x: x.numero)
            materias_semestre_ordenadas = Materia.objects.filter(semestre=semestre, pensum__carrera=proyecto.pensum.carrera).order_by('nombre')
            
            secciones_agrupadas_por_materia_y_num_seccion = group_by(secciones_de_semestre, key=lambda x: (x.materia.pk, x.numero))

            for materia in materias_semestre_ordenadas:
                html += '<th>%s</th>' % materia.nombre
            html += '</thead><tbody>'

            cont_secciones = 0
            for num_seccion in secciones_de_semestre_ord_por_num_seccion:
                if cont_secciones > 5:
                    html += '</tbody></table>'
                    html += '<div class="nueva-pagina"></div>'
                    html += pages_header.format(
                        base_dir=settings.BASE_DIR,
                        semestre=semestre,
                        lapso=proyecto.lapso_academico,
                        area='Área de Ingeniería de Sistemas',
                        institucion=proyecto.pensum.carrera.institucion
                     )
                    html += '<table class="horario"> <thead><th>Sección</th>'
                    for materia in materias_semestre_ordenadas:
                        html += '<th>%s</th>' % materia.nombre
                    html += '</thead><tbody>'
                    cont_secciones = 1
                else:
                    cont_secciones += 1
                html += '<tr><td><center><strong>%s</strong></center></td>' % num_seccion
                for materia in materias_semestre_ordenadas:
                    seccion_objetivo = secciones_agrupadas_por_materia_y_num_seccion.get((materia.pk, num_seccion), None)
                    if not seccion_objetivo:
                        html += '<td></td>'
                    else:
                        html += '<td>%s</td>' % seccion_objetivo[0].representacion_texto_encuentros()
                html += '</tr>'

            html += '</tbody></table>'
        html += '</body> </html>'
        return html


    def render_to_response(self, *args, **kwargs):
        # res = super(ReporteSemestresView, self).render_to_response(*args, **kwargs)
        res = super(ReporteSemestresView, self).render_to_response(*args, **kwargs)
        # pdfkit.from_string(res.rendered_content, 'reporte.pdf')
        options = {
            'page-size':'Letter',
            'orientation': 'Portrait',
            'encoding':'utf-8', 
            'margin-top':'3cm',
            'margin-bottom':'2cm',
            'margin-left':'2cm',
            'margin-right':'2cm',
        }        
        html_reporte = self.generar_html_reporte2()
        pdfkit.from_string(html_reporte, 'reporte.pdf', options=options)
        with open('reporte.pdf', 'rb') as fil:
            response = HttpResponse(fil.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        os.remove('reporte.pdf')
        # return HttpResponse(html_reporte)
        return response    



@method_decorator(csrf_exempt, name='dispatch')
class ReporteAulaActualView(View):
    def post(self, request, *args, **kwargs):
        html_tabla = request.POST['html_tabla']
        request.session['html_tabla'] = html_tabla
        return HttpResponse()

    def get(self, request, *args, **kwargs):
        # response = HttpResponse(fil.read(), content_type='application/pdf')
        if request.session.get('html_tabla'):
            # response = HttpResponse(request.session['html_tabla'])

            html = """<html>
<head>
  <title></title>
  <meta charset="utf-8">
  <style>

    table.tabla-encuentros td, th{
        border:  1px solid grey !important;
        outline: 1px solid grey !important;
        width:.auto !important;
        height:.4cm !important;
        min-height: 10px !important;
        padding: 3px;
        margin: 0px;
        background: #ffffff !important;
      }

    table.tabla-encuentros td, th {
        width: 11%;
    }

    .tabla-encuentros th:nth-child(1) {
        width: 2% !important;

    }
    .tabla-encuentros td:nth-child(1), .tabla-encuentros td:nth-child(2) {
        width: 1% !important;

    }


    table.header {
    width: 100%;
    }

    @media print {
      .nueva-pagina {
        page-break-before: always;
      }
    }


  </style>
</head>
<body>"""
            pages_header = """<table class="header">
    <tr>
        <td><img style="width:200px;height:90px;display:inline-block;" src="{base_dir}/core/static/img/logo_ais.jpg"></td>
        <td>
<strong>{institucion}</strong><br>
<strong>{area}</strong><br>
<strong>Programa: Ingeniería en Informática</strong><br>
<strong>Lapso Académico: {lapso}</strong><br>
<strong>Comisión de Horarios Académicos</strong><br>
        </td>

    </tr>

</table>
<hr>
<strong>Aula: {aula} ({tipo_aula})</strong> Area de Ingenieria de Sistemas / Area de Ingenieria de Sistemas"""

            options = {
                'page-size':'Letter',
                'orientation': 'Portrait',
                'encoding':'utf-8', 
                'margin-top':'3cm',
                'margin-bottom':'2cm',
                'margin-left':'1cm',
                'margin-right':'1cm',
            }   
            # html = html.format(body=request.session['html_tabla'])
            proyecto = Proyecto.objects.get(pk=kwargs.pop('proyecto_id'))
            aula = Aula.objects.get(pk=kwargs.pop('aula_id'))
            html += pages_header.format(
                base_dir=settings.BASE_DIR,
                lapso=proyecto.lapso_academico,
                area='Área de Ingeniería de Sistemas',
                institucion=proyecto.pensum.carrera.institucion,
                aula=aula.nombre,
                tipo_aula=aula.tipo_aula,
            )
            html += request.session['html_tabla'] + '</body></html>'
            pdfkit.from_string(html, 'reporte.pdf', options=options)
            with open('reporte.pdf', 'rb') as fil:
                response = HttpResponse(fil.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'inline;filename=some_file.pdf'
            os.remove('reporte.pdf')
            # return HttpResponse(html)
            return response  
        return HttpResponseBadRequest()

class EncuentroDeleteView(View):
    model = EncuentrosDias

    def get(self, *args, **kwargs):
        if 'pk' in kwargs and self.model.objects.filter(pk=kwargs['pk']).exists():
            self.object = self.model.objects.get(pk=kwargs['pk'])
            self.object.delete()
        return HttpResponse()

class DumpProyectoCSVView(View):

    def get(self, *args, **kwargs):
        proyecto = Proyecto.objects.get(pk=kwargs.pop('pk'))
        csv_text = 'asignatura;carrera;seccion;codigo;dia;horaInicio;horaCulminación;aula;cupos;profesor\n'
        encuentros_dias = EncuentrosDias.objects.filter(encuentro__seccion__proyecto=proyecto)
        for enc_dia in encuentros_dias:
            #Deporte;601;1;DP0001;Viernes;10:10;11:40;Dep;25;
            csv_text += ';'.join([
                enc_dia.encuentro.seccion.materia.nombre,
                enc_dia.encuentro.seccion.materia.pensum.carrera.nombre,
                str(enc_dia.encuentro.seccion.numero),
                enc_dia.dia.get_dia_display(),
                enc_dia.encuentro.bloque.hora_inicio.strftime('%H:%M'),
                str(enc_dia.encuentro.hora_salida)[:5],
                str(enc_dia.encuentro.seccion.cupo),
                enc_dia.encuentro.seccion.docente.nombre_apellido,
            ])
            csv_text += '\n'
        filename = 'pyDoxa Horario %s generado %s' % (proyecto.nombre, datetime.datetime.now())
        response = HttpResponse(csv_text, content_type='application/csv')
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        return response


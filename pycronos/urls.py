"""pycronos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.auth_logout, name='logout'),
    path('proyecto/', login_required(ProyectoCreateView.as_view()), name='dashboard'),
    # path('proyecto/<int:pk>/', login_required(ProyectoEditView.as_view()), name='editar_proyecto'),
    path('proyecto/<int:pk>/', login_required(ProyectoEditDragDropView.as_view()), name='editar_proyecto'),
    path('seccion/', login_required(SeccionCreateView.as_view()), name='crear_seccion'),
    path('encuentro/', login_required(EncuentroCreateView.as_view()), name='crear_encuentro'),
    path('encuentro/<int:pk>/delete/', login_required(EncuentroDeleteView.as_view()), name='encuentro_delete'),
    path('seccion-encuentros/', login_required(SeccionEncuentrosListView.as_view()), name='seccion_encuentros_list'),
    # path('seccion/<int:pk>/delete/', login_required(ConfirmacionEliminacionSeccionView.as_view()), name='eliminar_seccion'),
    path('seccion/<int:pk>/delete/', login_required(SeccionDeleteView.as_view()), name='eliminar_seccion'),
    path('seccion/<int:pk>/update/', login_required(SeccionUpdateView.as_view()), name='actualizar_seccion'),
    # path('', login_required(DashboardView.as_view()), name='project-edit'),
    path('', login_required(DashboardRedirectView.as_view()), name='project-edit'),
    path('proyectodnd/<int:pk>/', login_required(ProyectoEditDragDropView.as_view()), name='editar_proyecto_dnd'),
    path('api/encuentros/', EncuentrosAPIListView.as_view(), name='api_encuentros_list'),
    path('api/bloques/', BloquesAPIListView.as_view(), name='api_bloques_list'),
    path('api/aulas/', AulasAPIListView.as_view(), name='api_aulas_list'),
    path('api/dias/', DiasAPIListView.as_view(), name='api_dias_list'),
    path('api/encuentros/update/', EncuentrosAPIUpdateView.as_view(), name='api_encuentros_update'),
    path('reporte/semestres/<int:proyecto_id>/', ReporteSemestresView.as_view(), name='reporte_por_semestres'),
    path('reporte/aula/<int:proyecto_id>/<int:aula_id>/', ReporteAulaActualView.as_view(), name='reporte_aula_actual'),
    path('dump/proyecto/<int:pk>/csv/', login_required(DumpProyectoCSVView.as_view()), name='dump_proyecto'),
]

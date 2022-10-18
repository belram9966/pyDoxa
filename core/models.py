import datetime

from django.db import models
from django.contrib.auth.models import User

def to_timedelta(time_obj):
	return datetime.timedelta(hours=time_obj.hour, minutes=time_obj.minute, seconds=time_obj.second)

class Area(models.Model):
	nombre = models.CharField(max_length=100)
	creado = models.DateField(auto_now_add=True)
	actualizado = models.DateField(auto_now=True)
	# usuario = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.nombre	

class Aula(models.Model):
	nombre = models.CharField(max_length=60, blank=True, null=True)
	tipo_aula = models.ForeignKey('TipoAula', on_delete=models.CASCADE)
	numero = models.IntegerField()
	ubicacion = models.ForeignKey('UbicacionAula', on_delete=models.CASCADE)
	carrera = models.ForeignKey('Carrera', blank=True, null=True, on_delete=models.CASCADE)
	# proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE)

	creado = models.DateTimeField(auto_now_add=True)
	actualizado = models.DateTimeField(auto_now=True)

	class Meta:
		# @TODO validar esto en el front
		unique_together = (
			('ubicacion', 'numero'),
			('carrera', 'nombre'),
		)


	def __str__(self):
		return self.nombre	

class Institucion(models.Model):
	nombre = models.CharField(max_length=150)

	def __str__(self):
		return self.nombre	

class Carrera(models.Model):
	nombre = models.CharField(max_length=60)
	codigo = models.CharField(max_length=5)
	institucion = models.ForeignKey('Institucion', blank=True, null=True, on_delete=models.CASCADE)

	def __str__(self):
		return self.nombre	

class Pensum(models.Model):
	nombre = models.CharField(max_length=60)
	fecha = models.DateField()
	# regimen = models.CharField(max_length=10)
	carrera = models.ForeignKey('Carrera', on_delete=models.CASCADE)

	def __str__(self):
		return "%s - %s - %s" % (self.nombre, self.carrera, self.fecha)	

class AsistentesCarrera(models.Model):
	asistente = models.ForeignKey(User, on_delete=models.CASCADE)
	carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)

	def __str__(self):
		return "%s %s(%s)" % (self.asistente.first_name, self.asistente.last_name, self.carrera)		

class LapsoAcademico(models.Model):
	lapso = models.CharField(max_length=30)
	carrera = models.ForeignKey('Carrera', on_delete=models.CASCADE)

	def __str__(self):
		return self.lapso

class Proyecto(models.Model):
	nombre = models.CharField(max_length=60)

	# usuario = models.ForeignKey(User, on_delete=models.CASCADE)

	pensum = models.ForeignKey('Pensum', on_delete=models.CASCADE)

	lapso_academico = models.ForeignKey(LapsoAcademico, on_delete=models.CASCADE)
	fecha = models.DateField(auto_now_add=True)
	# fecha_memo = models.DateField(blank=True, null=True)
	observaciones = models.TextField(blank=True, null=True)
	creado = models.DateTimeField(auto_now_add=True)
	update = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.nombre


class Materia(models.Model):
	codigo = models.CharField(max_length=10)	
	nombre = models.CharField(max_length=60)	
	# avr = models.CharField(max_length=60)
	# @TODO: averiguar para que son estos campos
	# u_c = models.IntegerField()	
	# h_s = models.IntegerField()
	pensum = models.ForeignKey('Pensum', on_delete=models.CASCADE)	
	# @TODO: averiguar como se usa este campo
	# nivel = models.IntegerField()
	# departamento = models.ForeignKey('Departamento', on_delete=models.CASCADE)
	semestre = models.IntegerField()

	def __str__(self):
		return '%s(%s)' % (self.nombre, self.codigo)

# class Horas(models.Model):
# 	hora = models.IntegerField()

# 	def __str__(self):
# 		return str(self.hora)	

# class Minutos(models.Model):
# 	minutos = models.IntegerField(default=0)

# 	def __str__(self):
# 		return str(self.minutos)	

# class BloqueHorario(models.Model):
# 	hora_inicio = models.ForeignKey('Horas', related_name='hora_inicio_bloque', on_delete=models.CASCADE)
# 	minutos_inicio = models.ForeignKey('Minutos', related_name='minutos_inicio_bloque', on_delete=models.CASCADE)
# 	hora_fin = models.ForeignKey('Horas', on_delete=models.CASCADE)
# 	minutos_fin = models.ForeignKey('Minutos', on_delete=models.CASCADE)

# 	def __str__(self):
# 		return "%s:%s - %s:%s" % (self.hora_inicio, self.minutos_inicio, self.hora_fin, self.minutos_fin)

# class Horario(models.Model):
# 	creado = models.DateTimeField(auto_now_add=True)
# 	actualizado = models.DateTimeField(auto_now=True)

class Seccion(models.Model):
	# aula = models.ForeignKey('Aula', on_delete=models.CASCADE)
	docente = models.ForeignKey('Docente', on_delete=models.CASCADE)
	# @TODO: verificar el cambio de este campo
	numero = models.IntegerField()
	materia = models.ForeignKey('Materia', on_delete=models.CASCADE)
	proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE)
	cupo = models.IntegerField()
	# turno = models.ForeignKey('Turno', on_delete=models.CASCADE)
	# bloque = models.ForeignKey('BloqueHorario', on_delete=models.CASCADE)
	# hora_inicio = models.ForeignKey('Horas', related_name='hora_inicio_bloque', on_delete=models.CASCADE)
	# minutos_inicio = models.ForeignKey('Minutos', related_name='minutos_inicio_bloque', on_delete=models.CASCADE)
	# hora_inicio = models.IntegerField()
	# minutos_inicio = models.IntegerField()
	# hora_fin = models.ForeignKey('Horas', on_delete=models.CASCADE)
	# minutos_fin = models.ForeignKey('Minutos', on_delete=models.CASCADE)
	# hora_fin = models.IntegerField()
	# minutos_fin = models.IntegerField()		
	creado = models.DateTimeField(auto_now_add=True)
	actualizado = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "Seccion %s - %s" % (self.numero, self.materia)

	def get_cantidad_encuentros(self):
		return EncuentrosDias.objects.filter(encuentro__seccion=self).count()

	def encuentros_dias(self):
		return EncuentrosDias.objects.filter(encuentro__seccion=self).order_by('dia__dia')

	def representacion_texto_encuentros(self):
		texto = ''
		formato = "{dia} : {ubicacion}<br>Aula: {aula} / {bloque}<br>Cupo: {cupo}<br>"
		for enc_dia in self.encuentros_dias():
			tex_tmp = formato.format(
				dia=enc_dia.dia.get_dia_display(),
				ubicacion=enc_dia.encuentro.aula.ubicacion.nombre,
				aula=enc_dia.encuentro.aula.nombre,
				bloque=enc_dia.encuentro.representar_inicio_fin(),
				cupo=enc_dia.encuentro.seccion.cupo,
			)
			texto += tex_tmp
		return texto


class Docente(models.Model):
	cedula = models.IntegerField()
	nombres = models.CharField(max_length=60)
	apellidos = models.CharField(max_length=60)
	carrera = models.ForeignKey('Carrera', on_delete=models.CASCADE)
	# telf_movil = models.CharField(max_length=20, blank=True, null=True)
	# telf_casa = models.CharField(max_length=20, blank=True, null=True)
	email = models.CharField(max_length=100, blank=True, null=True)
	estado = models.ForeignKey('Estado', on_delete=models.CASCADE)
	municipio = models.ForeignKey('Municipio', on_delete=models.CASCADE, related_name='estado_docente')
	direccion = models.TextField(blank=True, null=True)
	creado = models.DateTimeField(auto_now_add=True)
	actualizado = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '%s %s CI: %s' % (self.nombres, self.apellidos, self.cedula)

	@property
	def nombre_apellido(self):
		nom = self.nombres.split(' ')[0]
		if self.apellidos:
			nom += ' ' + self.apellidos.split(' ')[0]
		return nom

class TelefonoDocente(models.Model):
	docente = models.ForeignKey('Docente', on_delete=models.CASCADE)
	telefono = models.CharField(max_length=15)
	tipo = models.CharField(max_length=2, choices=(
		('ce', 'Celular'),
		('ca', 'Casa'),
	), default='ce')
	
	def __str__(self):
		return self.telefono

# class DocentesSecciones(models.Model):
# 	docente = models.ForeignKey('Docente', on_delete=models.CASCADE)
# 	seccion = models.ForeignKey('Seccion', on_delete=models.CASCADE)



# class Direccion(models.Model):
# 	nombre = models.CharField(max_length=30)
# 	carrera = models.ForeignKey('Carrera', on_delete=models.CASCADE)

# class Departamento(models.Model):
# 	nombre = models.CharField(max_length=30)
# 	direccion = models.ForeignKey('Direccion', on_delete=models.CASCADE)
# 	docente = models.ForeignKey('Docente', on_delete=models.CASCADE)
# 	avr = models.CharField(max_length=12)

# 	def __str__(self):
# 		return self.nombre

# class Materia(models.Model):
# 	codigo = models.CharField(max_length=10)	
# 	nombre = models.CharField(max_length=60)	
# 	avr = models.CharField(max_length=60)
# 	# @TODO: averiguar para que son estos campos
# 	u_c = models.IntegerField()	
# 	h_s = models.IntegerField()
# 	pensum = models.ForeignKey('Pensum', on_delete=models.CASCADE)	
# 	# @TODO: averiguar como se usa este campo
# 	nivel = models.IntegerField()
# 	departamento = models.ForeignKey('Departamento', on_delete=models.CASCADE)

# 	def __str__(self):
# 		return '%s(%s)' % (self.nombre, self.codigo)		

class Turno(models.Model):
	nombre = models.CharField(max_length=60)

	def __str__(self):
		return self.nombre	

# class Seccion(models.Model):
# 	aula = models.ForeignKey('Aula', on_delete=models.CASCADE)
# 	# @TODO: verificar el cambio de este campo
# 	numero = models.IntegerField()
# 	materia = models.ForeignKey('Materia', on_delete=models.CASCADE)
# 	proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE)
# 	cupo = models.IntegerField()
# 	turno = models.ForeignKey('Turno', on_delete=models.CASCADE)
# 	# @TODO: consultar este cambio de haber agregado este campo aqui
# 	bloque = models.ForeignKey('Bloque', on_delete=models.CASCADE)
# 	creado = models.DateTimeField(auto_now_add=True)
# 	actualizado = models.DateTimeField(auto_now=True)

# 	def __str__(self):
# 		return "Seccion %s - %s" % (self.numero, self.materia)

class TipoAula(models.Model):
	nombre = models.CharField(max_length=60)
	descripcion = models.TextField(blank=True, null=True)
	modalidad = models.CharField(max_length=2, choices=(
		('pr', 'Presencial'),
		('vi', 'Virtual'),
	), default='pr')

	def __str__(self):
		return self.nombre	

class TipoEncuentro(models.Model):
	nombre = models.CharField(max_length=60)
	descripcion = models.TextField(blank=True, null=True)
	modalidad = models.CharField(max_length=2, choices=(
		('pr', 'Presencial'),
		('vi', 'Virtual'),
	), default='pr')

	def __str__(self):
		return self.nombre	

class Encuentro(models.Model):
	bloque = models.ForeignKey('Bloque', on_delete=models.CASCADE)
	numero_bloques = models.IntegerField(default=1)
	aula = models.ForeignKey('Aula', on_delete=models.CASCADE)
	seccion = models.ForeignKey('Seccion', on_delete=models.CASCADE)
	# dia = models.ForeignKey('Dia', on_delete=models.CASCADE)
	tipo = models.CharField(max_length=2, choices=(
		('pr', 'Presencial'),
		('vi', 'Virtual'),
	), default='pr')
	activo = models.BooleanField(default=True)
	creado = models.DateTimeField(auto_now_add=True)
	actualizado = models.DateTimeField(auto_now=True)

	def representar_inicio_fin(self):
		hora_salida = to_timedelta(self.bloque.hora_inicio) + (to_timedelta(self.bloque.esquema_bloque.duracion) * self.numero_bloques)
		hora_inicio = ':'.join([str(x).zfill(2) for x in str(self.bloque.hora_inicio).split(':')[:2]])
		hora_salida = ':'.join([str(x).zfill(2) for x in str(hora_salida).split(':')[:2]])
		return '%s - %s' % (hora_inicio, hora_salida)	

	@property
	def hora_salida(self):
		return to_timedelta(self.bloque.hora_inicio) + (to_timedelta(self.bloque.esquema_bloque.duracion) * self.numero_bloques)

	def __str__(self):
		return "%s - %s - %s" % (str(self.bloque), self.seccion, self.seccion.proyecto)

class EncuentrosDias(models.Model):
	encuentro = models.ForeignKey('Encuentro', on_delete=models.CASCADE)
	dia = models.ForeignKey('Dia', on_delete=models.CASCADE)

	def __str__(self):
		return '%s: %s' % (self.dia, self.encuentro)


class Estado(models.Model):
	nombre = models.CharField(max_length=100)

	def __str__(self):
		return self.nombre	

class Municipio(models.Model):
	nombre = models.CharField(max_length=100)

	def __str__(self):
		return self.nombre	

# class Docente(models.Model):
# 	cedula = models.IntegerField()
# 	nombres = models.CharField(max_length=60)
# 	apellidos = models.CharField(max_length=60)
# 	carrera = models.ForeignKey('Carrera', on_delete=models.CASCADE)
# 	telf_movil = models.CharField(max_length=20, blank=True, null=True)
# 	telf_casa = models.CharField(max_length=20, blank=True, null=True)
# 	email = models.CharField(max_length=100, blank=True, null=True)
# 	estado = models.ForeignKey('Estado', on_delete=models.CASCADE)
# 	municipio = models.ForeignKey('Estado', on_delete=models.CASCADE, related_name='estado_docente')
# 	direccion = models.TextField(blank=True, null=True)
# 	creado = models.DateTimeField(auto_now_add=True)
# 	actualizado = models.DateTimeField(auto_now=True)

# 	def __str__(self):
# 		return '%s %s CI: %s' % (self.nombres, self.apellidos, self.cedula)

# class DocentesSecciones(models.Model):
# 	docente = models.ForeignKey('Docente', on_delete=models.CASCADE)
# 	seccion = models.ForeignKey('Seccion', on_delete=models.CASCADE)

# class Asistencia(models.Model):
# 	proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE)
# 	encuentros_seccion = models.ForeignKey('EncuentrosSeccion', on_delete=models.CASCADE)
# 	docente = models.ForeignKey('Docente', on_delete=models.CASCADE)
# 	asistio = models.BooleanField(default=False)
# 	fecha = models.DateField()

class UbicacionAula(models.Model):
	nombre = models.CharField(max_length=60)
	descripcion = models.TextField(blank=True, null=True)
	area = models.ForeignKey('Area', blank=True, null=True, on_delete=models.CASCADE)

	def __str__(self):
		return self.nombre	

# # @TODO: entender el uso de esta tabla
# class EsquemaDia(models.Model):
# 	nombre = models.CharField(max_length=60)

class EsquemaBloque(models.Model):
	duracion = models.TimeField()
	esquema_dia = models.ForeignKey('EsquemaDia', on_delete=models.CASCADE)
	tipo_encuentro = models.ForeignKey('TipoEncuentro', on_delete=models.CASCADE)
	carrera = models.ForeignKey('Carrera', on_delete=models.CASCADE)
	creado = models.DateTimeField(auto_now_add=True)
	actualizado = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "%s: %s" % (self.carrera, self.duracion)

class RestriccionesBloques(models.Model):
	carrera = models.ForeignKey('Carrera', on_delete=models.CASCADE)
	inicio_rango_hora = models.TimeField(blank=True, null=True)
	fin_rango_hora = models.TimeField(blank=True, null=True)
	creado = models.DateTimeField(auto_now_add=True)
	actualizado = models.DateTimeField(auto_now=True)	

class EsquemaDia(models.Model):
	nombre = models.CharField(max_length=30)
	carrera = models.ForeignKey('Carrera', on_delete=models.CASCADE)
	tipo_encuentro = models.ForeignKey('TipoEncuentro', on_delete=models.CASCADE)
	activo = models.BooleanField(default=True)
	creado = models.DateTimeField(auto_now_add=True)
	actualizado = models.DateTimeField(auto_now=True)


class Dia(models.Model):
	dia = models.CharField(max_length=3, choices=(
		('1', 'Lunes'),
		('2', 'Martes'),
		('3', 'Miercoles'),
		('4', 'Jueves'),
		('5', 'Viernes'),
		('6', 'Sabado'),
		('7', 'Domingo'),
	))
	esquema_dia = models.ForeignKey('EsquemaDia', models.CASCADE)

	def __str__(self):
		return self.get_dia_display()	
	

# class Aula(models.Model):
# 	nombre = models.CharField(max_length=60)
# 	tipo_aula = models.ForeignKey('TipoAula', on_delete=models.CASCADE)
# 	ubicacion = models.ForeignKey('UbicacionAula', on_delete=models.CASCADE)
# 	proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE)
# 	esquema_dia = models.ForeignKey('EsquemaDia', on_delete=models.CASCADE)
# 	esquema_hora = models.ForeignKey('EsquemaHora', on_delete=models.CASCADE)
# 	creado = models.DateTimeField(auto_now_add=True)
# 	actualizado = models.DateTimeField(auto_now=True)

# 	def __str__(self):
# 		return '%s - %s - %s' % (self.nombre, self.tipo_aula, self.ubicacion)

# # @TODO: entender el uso de esta tabla
# class Dia(models.Model):
# 	numero = models.IntegerField(null=True)
# 	nombre = models.CharField(max_length=12)
# 	esquema_dia = models.ForeignKey('EsquemaDia', on_delete=models.CASCADE)

# class Hora(models.Model):
# 	numero = models.IntegerField(null=True)
# 	inicio = models.TimeField(null=True)
# 	fin = models.TimeField(null=True)
# 	esquema_hora = models.ForeignKey('EsquemaHora', on_delete=models.CASCADE)

# 	def __str__(self):
# 		return '%s - %s' % (self.inicio, self.fin)

# class HorasTurnos(models.Model):
# 	hora = models.ForeignKey('Hora', on_delete=models.CASCADE)
# 	turno = models.ForeignKey('Turno', on_delete=models.CASCADE)


class Bloque(models.Model):
	hora_inicio = models.TimeField()
	# hora_salida = models.TimeField()
	esquema_bloque = models.ForeignKey('EsquemaBloque', on_delete=models.CASCADE)
	turno = models.ForeignKey('Turno', on_delete=models.CASCADE)
	activo = models.BooleanField(default=True)
	# encuentros_seccion = models.ForeignKey('EncuentrosSeccion', on_delete=models.CASCADE)
	creado = models.DateTimeField(auto_now_add=True)
	actualizado = models.DateTimeField(auto_now=True)

	def representar_inicio_fin(self):
		hora_salida = to_timedelta(self.hora_inicio) + to_timedelta(self.esquema_bloque.duracion)
		hora_inicio = ':'.join([str(x).zfill(2) for x in str(self.hora_inicio).split(':')[:2]])
		hora_salida = ':'.join([str(x).zfill(2) for x in str(hora_salida).split(':')[:2]])
		return '%s - %s' % (hora_inicio, hora_salida)		

	def __str__(self):
		return self.representar_inicio_fin()


# class Ficha(models.Model):
# 	docente = models.ForeignKey('Docente', on_delete=models.CASCADE)
# 	ingreso = models.TimeField()
# 	contrato = models.CharField(max_length=50)
# 	categoria = models.CharField(max_length=50)
# 	dedicacion = models.CharField(max_length=50)
# 	observacion = models.TextField()
# 	estatus = models.BooleanField(default=True)
# 	creado = models.DateTimeField(auto_now_add=True)
# 	actualizado = models.DateTimeField(auto_now=True)





# --------------




# @TODO: entener el uso de esta tabla

# CREATE TABLE `v_bloques_group` (
# `EncuentrosSeccion_id_exist` int(11)
# ,`Aula_id` int(11)
# ,`Aula_nombre` varchar(60)
# ,`Dia_numero` tinyint(4)
# ,`Dia_nombre` varchar(12)
# ,`Hora_numero_inicio` tinyint(4)
# ,`Hora_inicio` time
# ,`Hora_numero_fin` tinyint(4)
# ,`Hora_fin` time
# );

# @TODO: entener el uso de esta tabla

# CREATE TABLE `v_encuentros_seccions` (
# `Carrera_id` int(11)
# ,`Carrera_nombre` varchar(60)
# ,`Carrera_codigo` varchar(5)
# ,`Area_id` int(11)
# ,`Proyecto_id` int(11)
# ,`Seccion_id` int(11)
# ,`Seccion_nombre` varchar(6)
# ,`Seccion_cupo` int(3)
# ,`Materia_id` int(11)
# ,`Materia_nombre` varchar(60)
# ,`Materia_avr` varchar(12)
# ,`Materia_codigo` varchar(10)
# ,`Materia_nivel` tinyint(2)
# ,`Pensum_id` int(11)
# ,`Direccion_id` int(11)
# ,`Direccion_nombre` varchar(30)
# ,`Departamento_id` int(11)
# ,`Departamento_nombre` varchar(30)
# ,`Turno_id` int(11)
# ,`Turno_nombre` varchar(60)
# ,`EncuentrosSeccion_id` int(11)
# ,`Encuentro_cant_horas` tinyint(4)
# ,`Encuentro_tipo_aula_id` int(11)
# ,`TipoAula_nombre` varchar(60)
# ,`Encuentro_modalidad` int(11)
# );


# @TODO: entener el uso de esta tabla

# CREATE TABLE `v_resumen` (
# `Carrera_id` int(11)
# ,`Carrera_nombre` varchar(60)
# ,`Carrera_codigo` varchar(5)
# ,`Area_id` int(11)
# ,`Proyecto_id` int(11)
# ,`Seccion_id` int(11)
# ,`Seccion_nombre` varchar(6)
# ,`Seccion_cupo` int(3)
# ,`Materia_id` int(11)
# ,`Materia_nombre` varchar(60)
# ,`Materia_avr` varchar(12)
# ,`Materia_codigo` varchar(10)
# ,`Materia_nivel` tinyint(2)
# ,`Pensum_id` int(11)
# ,`Direccion_id` int(11)
# ,`Direccion_nombre` varchar(30)
# ,`Departamento_id` int(11)
# ,`Departamento_nombre` varchar(30)
# ,`Turno_id` int(11)
# ,`Turno_nombre` varchar(60)
# ,`EncuentrosSeccion_id` int(11)
# ,`Encuentro_cant_horas` tinyint(4)
# ,`Encuentro_tipo_aula_id` int(11)
# ,`TipoAula_nombre` varchar(60)
# ,`Encuentro_modalidad` int(11)
# ,`EncuentrosSeccion_id_exist` int(11)
# ,`Aula_id` int(11)
# ,`Aula_nombre` varchar(60)
# ,`Dia_numero` tinyint(4)
# ,`Dia_nombre` varchar(12)
# ,`Hora_numero_inicio` tinyint(4)
# ,`Hora_inicio` time
# ,`Hora_numero_fin` tinyint(4)
# ,`Hora_fin` time
# );
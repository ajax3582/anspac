from google.appengine.ext import ndb

class Grado(ndb.Model):
	nombre = ndb.StringProperty()#1B,2B,3B,1A,2A
	llave = ndb.IntegerProperty()#key
	
class Asistente(ndb.Model):
	nombre = ndb.StringProperty()
	app = ndb.StringProperty()
	apm = ndb.StringProperty()
	cumple = ndb.StringProperty()
	telefono = ndb.StringProperty()
	celular = ndb.StringProperty()
	correo = ndb.StringProperty()
	grado = ndb.IntegerProperty()#llave del grado
	date = ndb.DateTimeProperty(auto_now_add=True)#para desplegar primero las ultimas que se pusieron
	tipo = ndb.StringProperty()#Para saber cuando son gubernamentales para el reporte mensual
	llave = ndb.IntegerProperty()#key

class Cursos(ndb.Model):
	tipo = ndb.StringProperty()#Humana,Moral,HyM
	nivel = ndb.StringProperty()#Basico,Avanzado
	llave = ndb.IntegerProperty()#key
	
class Animadora(ndb.Model):
	nombre = ndb.StringProperty()
	app = ndb.StringProperty()
	apm = ndb.StringProperty()
	cumple = ndb.StringProperty()
	telefono = ndb.StringProperty()
	celular = ndb.StringProperty()
	correo = ndb.StringProperty()
	year = ndb.StringProperty()#Ano en que ingreso
	desdoblada = ndb.StringProperty()#si o no
	coordinadora = ndb.StringProperty()#si o no
	date = ndb.DateTimeProperty(auto_now_add=True)#para desplegar primero las ultimas que se pusieron
	tipo = ndb.StringProperty()#Para saber cuando son gubernamentales para el reporte mensual
	llave = ndb.IntegerProperty()#key

class Unidad(ndb.Model):
	nombre = ndb.StringProperty()
	codigo = ndb.StringProperty()
	direccion = ndb.StringProperty()
	animadora = ndb.IntegerProperty(repeated=True)#Llave de las animadoras que pertenecen a la unidad
	asistente = ndb.IntegerProperty(repeated=True)#Llave de las asistentes que pertenecen a la unidad
	telefono = ndb.StringProperty()
	dia = ndb.StringProperty()
	hora = ndb.StringProperty()
	tipo = ndb.StringProperty()#parroquias, gobierno, etc, se sacara de UnidadTipo
	ciudad = ndb.StringProperty()#Chihuahua,Guerrero,etc
	virgen = ndb.StringProperty()#Si o no
	cursos = ndb.IntegerProperty()#llave del curso que tiene
	parroco = ndb.StringProperty()#nombre del parroco
	total = ndb.IntegerProperty(repeated=True)#total de asistencias por mes que hubo
	date = ndb.DateProperty(auto_now_add=True)
	llave = ndb.IntegerProperty()#key

class Evento(ndb.Model):
	nombre = ndb.StringProperty()#Nombre del evento
	fecha = ndb.StringProperty()
	llave = ndb.IntegerProperty()#key

class EAni(ndb.Model):
	evento = ndb.IntegerProperty()#Llave del evento
	ani = ndb.IntegerProperty()#Llave de animadora que asistio
	asistio = ndb.StringProperty()#si o no
	observaciones = ndb.StringProperty()	

class Llamadas(ndb.Model):
	unidad = ndb.IntegerProperty()#llave de la unidad
	coordinadora = ndb.IntegerProperty()#llave de las animadoras
	telefono = ndb.StringProperty()
	celular = ndb.StringProperty()
	observaciones = ndb.StringProperty()
	tipo = ndb.StringProperty()
	llave = ndb.IntegerProperty()#key
"""
class Grupo(ndb.Model):#todavia nose como hacerlo
	unidad = ndb.StructuredProperty(Unidad)
	coordinadora = ndb.StructuredProperty(Animadora)
	telefono = ndb.StringProperty()
	celular = ndb.StringProperty()
	direccion = ndb.StringProperty()
	dia = ndb.StringProperty()
	hora = ndb.StringProperty()
	llave = ndb.IntegerProperty()#key
"""	
class Semanas(ndb.Model):
	s1 = ndb.StringProperty()
	s2 = ndb.StringProperty()
	s3 = ndb.StringProperty()
	s4 = ndb.StringProperty()
	ss = ndb.StringProperty()
	mes = ndb.StringProperty()

class Meses(ndb.Model):
	unidad = ndb.IntegerProperty()#llave de la unidad en la que esta
	asistente = ndb.IntegerProperty()#llave de la asistente a la que pertenece 
	semanas = ndb.StructuredProperty(Semanas, repeated=True)

class UnidadTipo(ndb.Model):
	tipo = ndb.StringProperty()

class Reporte(ndb.Model):
	asisBasico = ndb.IntegerProperty()
	asisAvanzado = ndb.IntegerProperty()
	asisDesdoblada = ndb.IntegerProperty()
	asisGobierno = ndb.IntegerProperty()
	aniBasico = ndb.IntegerProperty()
	aniAvanzado = ndb.IntegerProperty()
	aniDesdoblada = ndb.IntegerProperty()
	aniGobierno = ndb.IntegerProperty()
	uBasicoEmpresa = ndb.IntegerProperty()
	uBasicoComunidad = ndb.IntegerProperty()
	uBasicoGobierno = ndb.IntegerProperty()
	uAvanzadoEmpresa = ndb.IntegerProperty()
	uAvanzadoComunidad = ndb.IntegerProperty()
	uAvanzadoGobierno = ndb.IntegerProperty()
	uDesdobladaEmpresa = ndb.IntegerProperty()
	uDesdobladaComunidad = ndb.IntegerProperty()
	uDesdobladaGobierno = ndb.IntegerProperty()
	uForaneas = ndb.IntegerProperty()
	
class ReporteMensual(ndb.Model):
	reporte = ndb.StructuredProperty(Reporte)
	mes = ndb.StringProperty()

class UsuariosModel(ndb.Model):
	usuario = ndb.UserProperty()
	grado = ndb.IntegerProperty()
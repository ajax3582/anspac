from google.appengine.ext import ndb

class Grado(ndb.Model):
	nombre = ndb.StringProperty(required=True)#key
	
class Asistente(ndb.Model):
	nombre = ndb.StringProperty()
	app = ndb.StringProperty()
	apm = ndb.StringProperty()
	cumple = ndb.StringProperty()
	telefono = ndb.StringProperty()
	celular = ndb.StringProperty()
	correo = ndb.StringProperty()
	grado = ndb.StructuredProperty(Grado)
	#unidad = ndb.IntegerProperty()
	llave = ndb.IntegerProperty()#key

class Cursos(ndb.Model):
	tipo = ndb.StringProperty()
	nivel = ndb.StringProperty()
	llave = ndb.IntegerProperty()#key
	
class Animadora(ndb.Model):
	nombre = ndb.StringProperty()
	app = ndb.StringProperty()
	apm = ndb.StringProperty()
	cumple = ndb.StringProperty()
	telefono = ndb.StringProperty()
	celular = ndb.StringProperty()
	correo = ndb.StringProperty()
	#unidad = ndb.IntegerProperty(repeated=True)#Llave de las unidades a las que pertenece
	year = ndb.StringProperty()#Ano en que ingreso
	desdoblada = ndb.StringProperty()#si o no
	coordinadora = ndb.StringProperty()#si o no
	llave = ndb.IntegerProperty()#key

class Unidad(ndb.Model):
	nombre = ndb.StringProperty()
	codigo = ndb.IntegerProperty()#key
	direccion = ndb.StringProperty()
	animadora = ndb.IntegerProperty(repeated=True)#Llave de las animadoras que pertenecen a la unidad
	asistente = ndb.IntegerProperty(repeated=True)#Llave de las asistentes que pertenecen a la unidad
	telefono = ndb.StringProperty()
	dia = ndb.StringProperty()
	hora = ndb.StringProperty()
	#nivel = ndb.StringProperty()
	#tipo = ndb.StringProperty()
	cursos = ndb.IntegerProperty()#llave del curso que tiene

class Evento(ndb.Model):
	unidad = ndb.IntegerProperty()#llave de la unidad
	nombre = ndb.IntegerProperty()#llave de la animadora
	asistio = ndb.StringProperty()#si o no
	observaciones = ndb.StringProperty()
	fecha = ndb.StringProperty()
	llave = ndb.IntegerProperty()#key

class Llamadas(ndb.Model):
	unidad = ndb.IntegerProperty()#llave de la unidad
	coordinadora = ndb.IntegerProperty()#llave de las animadoras
	telefono = ndb.StringProperty()
	celular = ndb.StringProperty()
	observaciones = ndb.StringProperty()
	llave = ndb.IntegerProperty()#key

class Grupo(ndb.Model):
	unidad = ndb.StructuredProperty(Unidad)
	coordinadora = ndb.StructuredProperty(Animadora)
	telefono = ndb.StringProperty()
	celular = ndb.StringProperty()
	direccion = ndb.StringProperty()
	dia = ndb.StringProperty()
	hora = ndb.StringProperty()
	llave = ndb.IntegerProperty()#key

class Semanas(ndb.Model):
	s1 = ndb.StringProperty()
	s2 = ndb.StringProperty()
	s3 = ndb.StringProperty()
	s4 = ndb.StringProperty()
	ss = ndb.StringProperty()
	unidad = ndb.IntegerProperty()#llave de la unidad en la que esta
	asistente = ndb.IntegerProperty()#llave de la asistente a la que pertenece 
	llave = ndb.IntegerProperty()
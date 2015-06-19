from google.appengine.ext import ndb

class Asistente(ndb.Model):
	nombre = ndb.StringProperty()
	cumple = ndb.StringProperty()
	telefono = ndb.StringProperty()
	celular = ndb.StringProperty()
	correo = ndb.StringProperty()
	grado = ndb.StringProperty()
class Grado(ndb.Model):
	nombre = ndb.StringProperty()
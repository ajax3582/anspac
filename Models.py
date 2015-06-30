from google.appengine.ext import ndb

class Grado(ndb.Model):
	nombre = ndb.StringProperty(required=True)
class Asistente(ndb.Model):
	nombre = ndb.StringProperty()
	app = ndb.StringProperty()
	apm = ndb.StringProperty()
	cumple = ndb.StringProperty()
	telefono = ndb.StringProperty()
	celular = ndb.StringProperty()
	correo = ndb.StringProperty()
	grado = ndb.StringProperty()
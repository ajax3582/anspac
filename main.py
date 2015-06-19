from render import Renderer
import webapp2
from Models import *

class MainHandler(Renderer):
    def get(self):
		self.render("index.html")

class AsistenteH(Renderer):
    def get(self):
		self.render("asistente.html")

class PruebaHP(Renderer):
	def get(self):
		grados = Grado.query().order(Grado.nombre)
		self.render("prueba.html",grados=grados)
	def post(self):
		a = Asistente()
		a.nombre = self.request.get('nombre')
		a.cumple = self.request.get('cumple')
		a.telefono = self.request.get('telefono')
		a.celular = self.request.get('celular')
		a.correo = self.request.get('correo')
		a.grado = self.request.get('grado')
		a.put()
		self.redirect('/asistente')

class GradoH(Renderer):
	def get(self):
		grados = Grado.query().order(Grado.nombre)
		self.render("grado.html", grados=grados)
	def post(self):
		name = self.request.get('nombre')
		grados = Grado.query(Grado.nombre == name).get()
		if not grados: 
			g = Grado()
			g.nombre = self.request.get('nombre')
			g.put()
			self.redirect('/asistente')
		else:
			self.redirect('/grado')
	
		
class GradoHP(Renderer):
	def get(self):
		#grados = Grado.query(Grado.nombre==nombreGrado).get()
		self.render("modificarg.html")
	def post(self, nombreGrado):
		name = self.request.get('nombre')
		grados = Grado.query(Grado.nombre == name).get()
		if not grados:
			grado = Grado.query(Grado.nombre == nombreGrado).get()
			grado.nombre = self.request.get('nombre')
			grado.put()
			self.redirect('/grado')
		else:
			self.redirect('/asistente')
		
class GradoD(Renderer):
	def get(self, nombreGrado):
		grados = Grado.query(Grado.nombre == nombreGrado).get()
		grados.key.delete()
		self.redirect('/asistente')
		
class CrearCafe(Renderer):
	def get(self):
		self.render("prueba.html")

	def post(self):
		nuevoCafe = Cafe()
		nuevoCafe.nombre = self.request.get('nombre')
		nuevoCafe.descripcion = self.request.get('descripcion')
#		nuevoCafe.precio = self.request.get('precio')
		nuevoCafe.tipoDeCafe = self.request.get('tipoDeCafe')
		nuevoCafe.put()
		self.redirect('/nuevoCafe')

class CafeController(Renderer):
	def get(self, nombreCafe):
		cafes = Cafe.query(nombre=nombreCafe).get()
		self.render("cafe.html", cafes=cafes)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/asistente', AsistenteH),
	('/creara',PruebaHP),
	('/prueba',PruebaHP),
	('/crearg',GradoH),
	('/modificarg/asistente', AsistenteH),
	('/modificarg',GradoHP),
	('/eliminarg/(.*)',GradoD),
	('/grado',GradoH)
], debug=True)

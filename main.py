from render import Renderer
import webapp2
from Models import *

class MainHandler(Renderer):
    def get(self):
		self.render("index.html")

class AsistenteH(Renderer):
    def get(self):
		asis = Asistente.query().order(Asistente.app)
		self.render("asistente.html",asis=asis)
		
class AsistenteHP(Renderer):
	def get(self, a):
		a = int(a)
		asis = Asistente.query(Asistente.llave==a).get()
		grados = Grado.query().order(Grado.nombre)
		self.render("modificara.html",asis=asis,grados=grados)
	def post(self, a):#put
		a = int(a)
		asis = Asistente.query(Asistente.llave==a).get()
		asis.nombre = self.request.get('nombre')
		asis.app = self.request.get('app')
		asis.apm = self.request.get('apm')
		asis.cumple = self.request.get('cumple')
		asis.telefono = self.request.get('telefono')
		asis.celular = self.request.get('celular')
		asis.correo = self.request.get('correo')
		g = Grado.query(Grado.nombre == self.request.get('grado')).get()
		asis.grado = g
		asis.put()
		self.redirect('/asistente')
		
class PruebaHP(Renderer):
	def get(self):
		asis = Asistente.query().order(Asistente.nombre)
		grados = Grado.query().order(Grado.nombre)
		self.render("prueba.html",grados=grados,asis=asis)
	def post(self):#post
		a = Asistente()
		a.nombre = self.request.get('nombre')
		a.app = self.request.get('app')
		a.apm = self.request.get('apm')
		a.cumple = self.request.get('cumple')
		a.telefono = self.request.get('telefono')
		a.celular = self.request.get('celular')
		a.correo = self.request.get('correo')
		g = Grado.query(Grado.nombre == self.request.get('grado')).get()
		a.grado = g
		x = 0
		a_key = a.put()
		a.llave = a_key.id()
		a.put()
		self.redirect('/asistente')
				
class AsistenteD(Renderer):
	def get(self, x):
		x = int(x)
		unidad = Unidad.query().order(Unidad.codigo)
		for u in unidad:
			y = 0
			while y < len(u.asistente):
				a = u.asistente[y]
				if x == a:
					u.asistente.remove(a)
					u.put()
				y = y + 1
		asis = Asistente.query(Asistente.llave == x).get()
		asis.key.delete()
		semanas = Semanas.query(Semanas.asistente == x).get()
		semanas.key.delete()
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
			g.id = self.request.get('nombre')
			g.put()
			self.redirect('/asistente')
		else:
			self.redirect('/grado')
	
		
class GradoHP(Renderer):
	def get(self, nombreGrado):
		grados = Grado.query(Grado.nombre==nombreGrado).get()
		#grados = Grado()
		self.render("modificarg.html", grado=grados)
	def post(self, nombreGrado):#put
		name = self.request.get('nombre')
		grados = Grado.query(Grado.nombre == name).get()
		if not grados:
			grado = Grado.query(Grado.nombre == nombreGrado).get()
			grado.nombre = self.request.get('nombre')
			grado.id = self.request.get('nombre')
			grado.put()
			asis = Asistente.query()
			for a in asis:
				if(a.grado.nombre == nombreGrado):
					a.grado.nombre = self.request.get('nombre')
					a.put()
			self.redirect('/asistente')
		else:
			self.redirect('/modificarg/' + nombreGrado, nombreGrado)
		
class GradoD(Renderer):
	def get(self, nombreGrado):
		grados = Grado.query(Grado.nombre == nombreGrado).get()
		grados.key.delete()
		asis = Asistente.query()
		for a in asis:
			if(a.grado.nombre == nombreGrado):
				a.grado.nombre = "Sin grado"
				a.put()
		self.redirect('/asistente')

class CursoH(Renderer):
	def get(self):
		cursos = Cursos.query().order(Cursos.tipo, Cursos.nivel)
		self.render("curso.html",cursos=cursos)
	def post(self):#post
		curso = Cursos()
		cursos = Cursos.query().order(Cursos.tipo)
		curso.tipo = self.request.get('tipo')
		curso.nivel = self.request.get('nivel')
		var1 = curso.put()
		curso.llave = var1.id()
		curso.put()
		self.redirect('/curso')

class CursoHP(Renderer):
	def get(self,cursoK):
		cursoK = int(cursoK)
		curso = Cursos.query(Cursos.llave==cursoK).get()
		self.render("modificarc.html",curso=curso)
	def post(self,cursoK):#put
		cursoK = int(cursoK)
		curso = Cursos.query(Cursos.llave==cursoK).get()
		curso.tipo = self.request.get('tipo')
		curso.nivel = self.request.get('nivel')
		curso.put()
		self.redirect('/curso')

class CursoHD(Renderer):
	def get(self,k):
		k = int(k)
		curso = Cursos.query(Cursos.llave==k).get()
		curso.key.delete()
		self.redirect('/curso')

class AnimadoraH(Renderer):
	def get(self):
		ani = Animadora.query().order(Animadora.app)
		self.render("animadora.html",ani=ani)

class AnimadoraHP(Renderer):
	def get(self):
		unidad = Unidad.query().order(Unidad.nombre)
		self.render("crearan.html",unidad=unidad)
	def post(self):#post
		a = Animadora()
		a.nombre = self.request.get('nombre')
		a.app = self.request.get('app')
		a.apm = self.request.get('apm')
		a.cumple = self.request.get('cumple')
		a.telefono = self.request.get('telefono')
		a.celular = self.request.get('celular')
		a.correo = self.request.get('correo')
		a.year = self.request.get('year')
		a.desdoblada = self.request.get('desdoblada')
		a.coordinadora = self.request.get('coordinadora')
		k = a.put()
		a.llave = k.id()
		a.put()
		self.redirect('/animadora')

class AnimadoraHpu(Renderer):
	def get(self,k):
		k = int(k)
		an = Animadora.query(Animadora.llave==k).get()
		unidad = Unidad.query().order(Unidad.nombre)
		self.render("modificaran.html",an=an,unidad=unidad)
	def post(self,k):#put
		k = int(k)
		a = Animadora.query(Animadora.llave==k).get()
		a.nombre = self.request.get('nombre')
		a.app = self.request.get('app')
		a.apm = self.request.get('apm')
		a.cumple = self.request.get('cumple')
		a.telefono = self.request.get('telefono')
		a.celular = self.request.get('celular')
		a.correo = self.request.get('correo')
		uni = self.request.get('unidad')
		if uni != '':
			uni = int(uni)
			a.unidad = uni
		a.year = self.request.get('year')
		a.desdoblada = self.request.get('desdoblada')
		a.coordinadora = self.request.get('coordinadora')
		a.put()
		self.redirect('/animadora')
		
class AnimadoraD(Renderer):
	def get(self,k):
		k = int(k)
		a = Animadora.query(Animadora.llave==k).get()
		a.key.delete()
		unidad = Unidad.query().order(Unidad.codigo)
		for u in unidad:
			y = 0
			while y < len(u.asistente):
				a = u.asistente[y]
				if k == a:
					u.asistente.remove(a)
					u.put()
				y = y + 1
		semanas = Semanas.query(Semanas.asistente == k).get()
		semanas.key.delete()
		self.redirect('/animadora')
		
class UnidadH(Renderer):
	def get(self):
		unidad = Unidad.query().order(Unidad.nombre)
		ani = Animadora.query().order(-Animadora.coordinadora)
		curso = Cursos.query().order(Cursos.llave)
		self.render("unidad.html",unidad=unidad,curso=curso,ani=ani)

class UnidadHP(Renderer):
	def get(self):
		curso = Cursos.query().order(Cursos.nivel, Cursos.tipo)
		ani = Animadora.query().order(Animadora.app)
		self.render("crearu.html",curso=curso,ani=ani)
	def post(self):#post
		u = Unidad()
		codigo = int(self.request.get('codigo'))
		u.nombre = self.request.get('nombre')
		u.codigo = codigo
		u.direccion = self.request.get('direccion')
		u.telefono = self.request.get('telefono')
		u.dia = self.request.get('dia')
		u.hora = self.request.get('hora')
		curso = self.request.get('curso')
		curso = int(curso)
		u.cursos = curso
		animadora = self.request.get('animadora1')
		if animadora != '':
			a = int(self.request.get('animadora1'))
			u.animadora.append(a)
			UnidadHP.altaSemana(self,codigo,a)
		animadora = self.request.get('animadora2')
		if animadora != '':
			a = int(self.request.get('animadora2'))
			u.animadora.append(a)
			UnidadHP.altaSemana(self,codigo,a)
		animadora = self.request.get('animadora3')
		if animadora != '':
			a = int(self.request.get('animadora3'))
			u.animadora.append(a)
			UnidadHP.altaSemana(self,codigo,a)
		u.put()
		self.redirect('/unidad')
	def altaSemana(self,codigo,asis):
		s = Semanas()
		s.asistente = asis
		s.unidad = codigo
		s.s1 = "0"
		s.s2 = "0"
		s.s3 = "0"
		s.s4 = "0"
		s.ss = "0"
		k = s.put()
		s.llave = k.id()
		s.put()
		return

class UnidadHpu(Renderer):
	def get(self,codigo):
		codigo = int(codigo)
		unidad = Unidad.query(Unidad.codigo==codigo).get()
		curso = Cursos.query().order(Cursos.nivel, Cursos.tipo)
		ani = Animadora.query().order(Animadora.app)
		asistente = Asistente.query().order(Asistente.app)
		self.render("modificaru.html",unidad=unidad,curso=curso,ani=ani,asistente=asistente)
	def post(self,codigo):#put
		codigo = int(codigo)
		u = Unidad.query(Unidad.codigo==codigo).get()
		codigo = self.request.get('codigo')
		u.nombre = self.request.get('nombre')
		if codigo != '':
			codigo = int(codigo)
			u.codigo = codigo
		u.direccion = self.request.get('direccion')
		u.telefono = self.request.get('telefono')
		u.dia = self.request.get('dia')
		u.hora = self.request.get('hora')
		curso = self.request.get('curso')
		if curso != '':
			curso = int(curso)
			u.cursos = curso
		x = len(u.animadora)
		if x < 5:
			animadora = self.request.get('animadora1')
			if animadora != '':
				a = int(self.request.get('animadora1'))
				u.animadora.append(a)
				UnidadHpu.altaSemana(self,codigo,a)
				x = x+1
			animadora = self.request.get('animadora2')
			if (animadora != '') and (x < 5):
				a = int(self.request.get('animadora2'))
				u.animadora.append(a)
				UnidadHpu.altaSemana(self,codigo,a)
				x = x+1
			animadora = self.request.get('animadora3')
			if (animadora != '') and (x < 5):
				a = int(self.request.get('animadora3'))
				u.animadora.append(a)
				UnidadHpu.altaSemana(self,codigo,a)
				x = x+1
		all = self.request.get_all('a')
		x = len(u.asistente)
		for a in all:
			if x < 20:
				a = int(a)
				u.asistente.append(a)
				UnidadHpu.altaSemana(self,codigo,a)
				x = x+1
		u.put()
		self.redirect('/unidad')	
	def altaSemana(self,codigo,asis):
		s = Semanas()
		s.asistente = asis
		s.unidad = codigo
		s.s1 = "0"
		s.s2 = "0"
		s.s3 = "0"
		s.s4 = "0"
		s.ss = "0"
		k = s.put()
		s.llave = k.id()
		s.put()
		return
		
class UnidadHe(Renderer):
	def get(self,codigo,num):
		codigo = int(codigo)
		num = int(num)
		unidad = Unidad.query(Unidad.codigo==codigo).get()
		x = unidad.animadora[num]
		unidad.animadora.remove(x)
		unidad.put()
		s = Semanas.query(Semanas.unidad==codigo,Semanas.asistente==x).get()
		s.key.delete()
		self.redirect('/unidad')
	
class UnidadD(Renderer):
	def get(self,codigo):
		codigo = int(codigo)
		u = Unidad.query(Unidad.codigo==codigo).get()
		u.key.delete()
		self.redirect('/unidad')

class UnidadAsis(Renderer):
	def get(self,codigo,num):
		codigo = int(codigo)
		num = int(num)
		u = Unidad.query(Unidad.codigo==codigo).get()
		x = u.asistente[num]
		u.asistente.remove(x)
		u.put()
		s = Semanas.query(Semanas.unidad==codigo,Semanas.asistente==x).get()
		s.key.delete()
		self.redirect('/unidad')
		
		
class LlamadasH(Renderer):
	def get(self):
		llamadas = Llamadas.query()
		unidad = Unidad.query().order(Unidad.nombre)
		ani = Animadora.query()
		self.render("llamadas.html",llamadas=llamadas,unidad=unidad,ani=ani)

class LlamadasHP(Renderer):
	def get(self):
		unidad = Unidad.query()
		ani = Animadora.query()
		self.render("crearl.html",unidad=unidad,ani=ani)
	def post(self):
		l = Llamadas()
		x = int(self.request.get('nombre'))
		l.unidad = x
		x = int(self.request.get('coordinadora'))
		l.coordinadora = x
		l.telefono = self.request.get('telefono')
		l.celular = self.request.get('celular')
		l.observaciones = self.request.get('observaciones')
		x = l.put()
		l.llave = x.id()
		l.put()
		self.redirect('/llamadas')

class LlamadasHpu(Renderer):
	def get(self,k):
		k = int(k)
		l = Llamadas.query(Llamadas.llave==k).get()
		unidad = Unidad.query()
		ani = Animadora.query()
		self.render("modificarl.html",unidad=unidad,l=l,ani=ani)
	def post(self,k):
		k = int(k)
		l = Llamadas.query(Llamadas.llave==k).get()
		u = self.request.get('unidad')
		if u != '':
			u = int(u)
			l.unidad = u
		u = self.request.get('coordinadora')
		if u != '':
			u = int(u)
			l.coordinadora = u
		l.telefono = self.request.get('telefono')
		l.celular = self.request.get('celular')
		l.observaciones = self.request.get('observaciones')
		l.put()
		self.redirect('/llamadas')
		
class LlamadasD(Renderer):
	def get(self,k):
		k = int(k)
		l = Llamadas.query(Llamadas.llave==k).get()
		l.key.delete()
		self.redirect('/llamadas')

class EventoH(Renderer):
	def get(self):
		unidad = Unidad.query().order(Unidad.nombre)
		eventos = Evento.query().order(Evento.fecha)
		ani = Animadora.query()
		self.render("eventos.html",eventos=eventos,ani=ani,unidad=unidad)
		
class EventoHP(Renderer):
	def get(self):
		unidad = Unidad.query().order(Unidad.nombre)
		ani = Animadora.query()
		self.render("creare.html",ani=ani,unidad=unidad)
	def post(self):
		e = Evento()
		x = int(self.request.get('unidad'))
		e.unidad = x
		x = int(self.request.get('nombre'))
		e.nombre = x
		e.asistio = self.request.get('asistio')
		e.observaciones = self.request.get('observaciones')
		e.fecha = self.request.get('fecha')
		x = e.put()
		e.llave = x.id()
		e.put()
		self.redirect('/eventos')
		
class EventoHpu(Renderer):
	def get(self,k):
		k = int(k)
		e = Evento.query(Evento.llave == k).get() 
		unidad = Unidad.query().order(Unidad.nombre)
		ani = Animadora.query()
		self.render("modificare.html",e=e,ani=ani,unidad=unidad)
	def post(self,k):
		k = int(k)
		e = Evento.query(Evento.llave == k).get()
		x = self.request.get('unidad')
		if x != '':
			x = int(x)
			e.unidad = x
		x = self.request.get('nombre')
		if x != '':
			x = int(x)
			e.nombre = x
		x = self.request.get('asistio')
		if x != '':
			e.asistio = x
		e.observaciones = self.request.get('observaciones')
		e.fecha = self.request.get('fecha')
		e.put()
		self.redirect('/eventos')

class SemanasH(Renderer):
	def get(self,codigo):
		codigo = int(codigo)
		u = Unidad.query(Unidad.codigo == codigo).get()
		se = Semanas.query(Semanas.unidad == codigo)
		asis = Asistente.query().order(Asistente.app)
		ani = Animadora.query().order(-Animadora.coordinadora)
		self.render("semanas.html",u=u,se=se,asis=asis,ani=ani)
	def post(self,codigo):
		codigo = int(codigo)
		all = self.request.get_all('a')
		s1 = self.request.get('s1')
		s2 = self.request.get('s2')
		s3 = self.request.get('s3')
		s4 = self.request.get('s4')
		ss = self.request.get('ss')
		for a in all:
			a = int(a)
			se = Semanas.query(Semanas.unidad == codigo, Semanas.asistente == a).get()
			if se:
				if s1 != '':
					se.s1 = s1
				if s2 != '':
					se.s2 = s2
				if s3 != '':
					se.s3 = s3
				if s4 != '':
					se.s4 = s4
				if ss != '':
					se.ss = ss
				se.put()
		self.redirect('/semanas/' + str(codigo))
		
class EventoD(Renderer):
	def get(self,k):
		k = int(k)
		e = Evento.query(Evento.llave == k).get() 
		e.key.delete()
		self.redirect('/eventos')
		
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
	('/modificarg/(.*)',GradoHP),
	('/eliminarg/(.*)',GradoD),
	('/grado',GradoH),
	('/modificara/(.*)',AsistenteHP),
	('/eliminara/(.*)',AsistenteD),
	('/curso', CursoH),
	('/crearc', CursoH),
	('/modificarc/(.*)',CursoHP),
	('/cursoD/(.*)',CursoHD),
	('/animadora',AnimadoraH),
	('/crearan',AnimadoraHP),
	('/modificaran/(.*)',AnimadoraHpu),
	('/eliminaran/(.*)',AnimadoraD),
	('/unidad',UnidadH),
	('/crearu',UnidadHP),
	('/modificaru/(.*)',UnidadHpu),
	('/eliminarani/(.*)/(.*)',UnidadHe),
	('/eliminaru/(.*)',UnidadD),
	('/asisq/(.*)/(.*)',UnidadAsis),
	('/semanas/(.*)',SemanasH),
	('/modificars/(.*)',SemanasH),
	('/llamadas',LlamadasH),
	('/crearl',LlamadasHP),
	('/modificarl/(.*)',LlamadasHpu),
	('/eliminarl/(.*)',LlamadasD),
	('/eventos',EventoH),
	('/creare',EventoHP),
	('/modificare/(.*)',EventoHpu),
	('/eliminare/(.*)',EventoD)
], debug=True)

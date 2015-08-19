from render import Renderer
import webapp2
from Models import *
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class Check(Renderer):
	def asis(self):
		user = users.get_current_user()
		if user:
			u = UsuariosModel.query(UsuariosModel.usuario==user).get()
			if u:
				if u.grado == 1:
					self.redirect('/new')
				else:
					return
			else:
				self.redirect('/login')
		else:
			self.redirect('/new2')
			
class ControlH2(Renderer):
	def get(self):
		user = "None"
		logout =""
		greeting = ((users.create_login_url('/login')))
		self.render("index2.html",greeting = greeting, user=user, logout = logout)
			
class ControlH(Renderer):
	def get(self):
		user = users.get_current_user()
		u = UsuariosModel.query(UsuariosModel.usuario==user).get()
		logout = ('%s' %(users.create_logout_url('/logout')))
		self.render("nuevos.html", logout=logout, user = user)
		
class MainHandler(Renderer):
    def get(self):
		user = users.get_current_user()
		if user:
			u = UsuariosModel.query(UsuariosModel.usuario==user).get()
			if u:
				if u.grado == 1:
					logout = ('%s' %(users.create_logout_url('/logout')))
					self.render("nuevos.html", logout=logout, user = user)
				else:
					greeting = ('Bienvenido, %s! <a href="%s">sign out</a>' %(user.nickname(), users.create_logout_url('/logout')))
					logout = ('%s' %(users.create_logout_url('/logout')))
					self.render("index.html",greeting = greeting, user=user, logout = logout)
		else:
			user = "None"
			logout =""
			greeting = ((users.create_login_url('/login')))
			self.render("index2.html",greeting = greeting, user=user, logout = logout)
			
class Login(Renderer):
	def get(self):
		user = users.get_current_user()
		u = UsuariosModel.query(UsuariosModel.usuario==user).get()
		if u:
			if u.grado == 1:
				logout = ('%s' %(users.create_logout_url('/logout')))
				self.render("nuevos.html", logout=logout, user = user)
			else:
				greeting = ('Bienvenido, %s! (<a href="%s">sign out</a>' %(user.nickname(), users.create_logout_url('/logout')))
				logout = ('%s' %(users.create_logout_url('/logout')))
				self.render("index.html", user=user, greeting = greeting, logout = logout )
		else:
			u = UsuariosModel()
			u.usuario = user
			u.grado = 1
			u.put()
			logout = ('%s' %(users.create_logout_url('/logout')))
			self.render("nuevos.html", logout = logout, user = user)
			
class Logout(Renderer):
	def get(self):
		user = "None"
		greeting = ((users.create_login_url('/login')))
		self.render("index2.html", user=user,greeting=greeting)
#----------------------------------------Grado----------------------------------------------------#
class GradoH(Renderer):
	def get(self):
		user = users.get_current_user()
		if user:
			u = UsuariosModel.query(UsuariosModel.usuario==user).get()
			if u:
				if u.grado == 1:
					self.redirect('/new')
		else:
			self.redirect('/new2')
		grado = Grado.query().order(Grado.nombre)
		self.render("grado.html",grado=grado,user=user)
	def post(self):
		g = Grado()
		g.nombre = self.request.get('nombre')
		k = g.put()
		g.llave = k.id()
		g.put()
		self.redirect('/grado')

class GradoHP(Renderer):
	def get(self,nombre):
		g = Grado.query(Grado.nombre==nombre).get()
		self.render("/gmodificar.html",g=g)
	def post(self,nombre):
		nnombre = self.request.get('nnombre')
		g = Grado.query(Grado.nombre==nombre).get()
		g.nombre = nnombre
		g.put()
		self.redirect('/grado')

class GradoD(Renderer):
	def get(self,nombre):
		g = Grado.query(Grado.nombre==nombre).get()
		asis = Asistente.query(Asistente.grado==g.llave)
		for a in asis:
			a.grado = 0
			a.put()
		g.key.delete()
		self.redirect('/grado')
#---------------------------------------/Grado----------------------------------------------------#
#--------------------------------------Asistente--------------------------------------------------#
class AsistenteH(Renderer):
	def get(self):
		user = users.get_current_user()
		if user:
			u = UsuariosModel.query(UsuariosModel.usuario==user).get()
			if u:
				if u.grado == 1:
					self.redirect('/new')
		else:
			self.redirect('/new2')
		grados = Grado.query().order(Grado.nombre)
		asis = Asistente.query().order(-Asistente.date)
		unidad = Unidad.query().order(Unidad.nombre)
		self.render("asistente.html",grados=grados,asis=asis,unidad=unidad,user=user)

class AsistenteHPO(Renderer):
	def get(self):
		grados = Grado.query().order(Grado.nombre)
		unidad = Unidad.query().order(Unidad.nombre)
		self.render("asisagregar.html",grados=grados,unidad=unidad)
	def post(self):
		a = Asistente()
		a.nombre = self.request.get('nombre')
		a.app = self.request.get('app')
		a.apm = self.request.get('apm')
		a.cumple = self.request.get('cumple')
		a.telefono = self.request.get('telefono')
		a.celular = self.request.get('celular')
		a.correo = self.request.get('correo')
		g = int(self.request.get('grado'))
		a.grado = g
		a_key = a.put()
		a.llave = a_key.id()
		if self.request.get('unidad') != '':
			unidad = int(self.request.get('unidad'))
			m = MesesAsis()
			MesesAsis.asis(m,unidad,a_key.id())
			u = Unidad.query(Unidad.llave==unidad).get()
			u.asistente.append(k.id())
		a.put()
		self.redirect('/asistente')

class AsistenteHP(Renderer):
	def get(self,llave):
		llave = int(llave)
		asis = Asistente.query(Asistente.llave==llave).get()
		grados = Grado.query().order(Grado.nombre)
		unidad = Unidad.query().order(Unidad.nombre)
		self.render("asismodificar.html",asis=asis,grados=grados,unidad=unidad)
	def post(self,llave):
		llave = int(llave)
		a = Asistente.query(Asistente.llave==llave).get()
		a.nombre = self.request.get('nombre')
		a.app = self.request.get('app')
		a.apm = self.request.get('apm')
		a.cumple = self.request.get('cumple')
		a.telefono = self.request.get('telefono')
		a.celular = self.request.get('celular')
		a.correo = self.request.get('correo')
		if self.request.get('grado') != '':
			g = int(self.request.get('grado'))
			a.grado = g
		a.put()
		self.redirect('/asistente')
		
class AsistenteD(Renderer):
	def get(self,llave):
		llave = int(llave)
		asis = Asistente.query(Asistente.llave==llave).get()
		meses = Meses.query(Meses.asistente==llave).get()
		if meses:
			meses.key.delete()
		unidad = Unidad.query().order(Unidad.nombre)
		for uni in unidad:
			y = 0
			while y < len(uni.asistente):
				a = uni.asistente[y]
				if llave == a:
					uni.asistente.remove(a)
					uni.put()
				y = y + 1
		asis.key.delete()
		self.redirect('/asistente')
#-------------------------------------/Asistente--------------------------------------------------#
#--------------------------------------Animadora--------------------------------------------------#
class AnimadoraH(Renderer):
	def get(self):
		user = users.get_current_user()
		if user:
			u = UsuariosModel.query(UsuariosModel.usuario==user).get()
			if u:
				if u.grado == 1:
					self.redirect('/new')
		else:
			self.redirect('/new2')
		ani = Animadora.query().order(-Animadora.date)
		unidad = Unidad.query().order(Unidad.nombre)
		self.render("animadora.html",ani=ani,unidad=unidad,user=user)
		
class AnimadoraHPO(Renderer):
	def get(self):
		unidad = Unidad.query().order(Unidad.nombre)
		self.render("aniagregar.html",unidad=unidad)
	def post(self):
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
		if self.request.get('unidad') != '':
			unidad = int(self.request.get('unidad'))
			m = MesesAsis()
			MesesAsis.asis(m,unidad,k.id())
			u = Unidad.query(Unidad.llave==unidad).get()
			u.animadora.append(k.id())
			if a.coordinadora == "si":
				l = Llamadas()
				l.unidad = unidad
				l.coordinadora = k.id()
				l.telefono = an.telefono
				l.celular = an.celular
				l.observaciones = ''
				l.tipo = u.tipo
				kk = l.put()
				l.llave = kk.id()
				l.put()
		a.llave = k.id()
		a.put()
		self.redirect('/animadora')
	
class AnimadoraHP(Renderer):
	def get(self,llave):
		llave = int(llave)
		ani = Animadora.query(Animadora.llave==llave).get()
		self.render("animodificar.html",ani=ani)
	def post(self,llave):
		llave = int(llave)
		a = Animadora.query(Animadora.llave==llave).get()
		coordinadora = a.coordinadora
		tel = a.telefono
		cel = a.celular
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
		if coordinadora == "si" and a.coordinadora == "si":
			if tel != a.telefono:
				ll = Llamadas.query(Llamadas.coordinadora==llave)
				for l in ll:
					l.telefono = a.telefono
					l.put()
			if cel != a.celular:
				ll = Llamadas.query(Llamadas.coordinadora==llave)
				for l in ll:
					l.celular = a.celular
					l.put()
		"""if self.request.get('unidad') != '':
			unidad = int(self.request.get('unidad'))
			m = MesesAsis()
			MesesAsis(m,unidad,k.id())
			u = Unidad.query(Unidad.llave==unidad).get()
			u.animadora.append(k.id())"""
		if coordinadora == "si" and a.coordinadora == "no":
			ll = Llamadas.query(Llamadas.coordinadora==llave)
			for l in ll:
				l.key.delete()
		self.redirect('/animadora')

class AnimadoraD(Renderer):
	def get(self,llave):
		llave = int(llave)
		ani = Animadora.query(Animadora.llave==llave).get()
		meses = Meses.query(Meses.asistente==llave).get()
		if meses:
			meses.key.delete()
		llamada = Llamadas.query(Llamadas.coordinadora==llave)
		if llamada:
			for l in llamada:
				l.key.delete()
		unidad = Unidad.query().order(Unidad.nombre)
		for uni in unidad:
			y = 0
			while y < len(uni.animadora):
				a = uni.animadora[y]
				if llave == a:
					uni.animadora.remove(a)
					uni.put()
				y = y + 1
		ani.key.delete()
		self.redirect('/animadora')		
#-------------------------------------/Animadora--------------------------------------------------#
#---------------------------------------Cursos----------------------------------------------------#
class CursosH(Renderer):
	def get(self):
		user = users.get_current_user()
		if user:
			u = UsuariosModel.query(UsuariosModel.usuario==user).get()
			if u:
				if u.grado == 1:
					self.redirect('/new')
		else:
			self.redirect('/new2')
		cursos = Cursos.query().order(Cursos.tipo)
		self.render("curso.html",cursos=cursos,user=user)
	def post(self):
		curso = Cursos()
		curso.tipo = self.request.get('tipo')
		curso.nivel = self.request.get('nivel')
		var1 = curso.put()
		curso.llave = var1.id()
		curso.put()
		self.redirect('/curso')
		
class CursosHP(Renderer):
	def get(self,cursoK):
		cursoK = int(cursoK)
		curso = Cursos.query(Cursos.llave==cursoK).get()
		self.render("cmodificar.html",curso=curso)
	def post(self,cursoK):
		cursoK = int(cursoK)
		curso = Cursos.query(Cursos.llave==cursoK).get()
		curso.tipo = self.request.get('tipo')
		curso.nivel = self.request.get('nivel')
		curso.put()
		self.redirect('/curso')
		
class CursoD(Renderer):
	def get(self,cursok):
		#cursoK = int(cursoK)
		curso = Cursos.query(Cursos.llave==int(cursok)).get()
		curso.key.delete()
		self.redirect('/curso')
#--------------------------------------/Cursos----------------------------------------------------#
#---------------------------------------Unidad----------------------------------------------------#
class UnidadH(Renderer):
	def get(self):
		user = users.get_current_user()
		if user:
			u = UsuariosModel.query(UsuariosModel.usuario==user).get()
			if u:
				if u.grado == 1:
					self.redirect('/new')
		else:
			self.redirect('/new2')
		unidad = Unidad.query().order(Unidad.tipo)
		ani = Animadora.query().order(-Animadora.coordinadora)
		curso = Cursos.query()
		tipos = UnidadTipo.query().order(UnidadTipo.tipo)
		x1 = "Unidades"
		self.render('unidad.html',unidad=unidad,ani=ani,curso=curso,tipos=tipos,x=x1,user=user)

class UnidadDir(Renderer):
	def get(self):
		user = users.get_current_user()
		if user:
			u = UsuariosModel.query(UsuariosModel.usuario==user).get()
			if u:
				if u.grado == 1:
					self.redirect('/new')
		else:
			self.redirect('/new2')
		unidad = Unidad.query().order(Unidad.tipo)
		ani = Animadora.query(Animadora.coordinadora=="si")
		curso = Cursos.query()
		x1 = "Directorio"
		self.render('unidadir.html',unidad=unidad,ani=ani,curso=curso,x=x1,user=user)

class UnidadHT(Renderer):
	def get(self, tipo):
		user = users.get_current_user()
		if user:
			u = UsuariosModel.query(UsuariosModel.usuario==user).get()
			if u:
				if u.grado == 1:
					self.redirect('/new')
		else:
			self.redirect('/new2')
		unidad = Unidad.query(Unidad.tipo==tipo).order(Unidad.nombre)
		ani = Animadora.query().order(-Animadora.coordinadora)
		curso = Cursos.query()
		tipos = UnidadTipo.query().order(UnidadTipo.tipo)
		x1 = tipo
		self.render('unidad.html',unidad=unidad,ani=ani,curso=curso,tipos=tipos,x=x1,user=user)
		
class UnidadHPO(Renderer):
	def get(self):
		curso = Cursos.query().order(Cursos.tipo)
		tipo = UnidadTipo.query().order(UnidadTipo.tipo)
		ani = Animadora.query(Animadora.coordinadora=="si").order(Animadora.app)
		self.render('ucrear.html',curso=curso,tipo=tipo,ani=ani)
	def post(self):#post
		u = Unidad()
		u.nombre = self.request.get('nombre')
		u.codigo = self.request.get('codigo')
		u.direccion = self.request.get('direccion')
		u.telefono = self.request.get('telefono')
		u.dia = self.request.get('dia')
		u.hora = self.request.get('hora')
		curso = self.request.get('curso')
		curso = int(curso)
		t = self.request.get('tipo')
		if t == '':
			t = self.request.get('tipo2')
			if t != '':
				ut = UnidadTipo()
				ut.tipo = t
				ut.put()
		u.tipo = t
		u.cursos = curso
		u.ciudad = self.request.get('ciudad')
		virgen = self.request.get('virgen')
		u.virgen = virgen
		parroco = self.request.get('parroco')
		if u.tipo != "Parroquia":
			parroco = "NA"
		u.parroco = parroco
		animadora = self.request.get('animadora1')#esta seria la coordinadora
		x = u.put()
		u.llave = x.id()
		if animadora != '':
			a = int(self.request.get('animadora1'))
			u.animadora.append(a)
			m = MesesAsis()
			MesesAsis.asis(m,u.llave,a)
			an = Animadora.query(Animadora.llave==a).get()
			l = Llamadas()
			l.unidad = u.llave
			l.coordinadora = a
			l.telefono = an.telefono
			l.celular = an.celular
			l.observaciones = ''
			l.tipo = u.tipo
			kk = l.put()
			l.llave = kk.id()
			l.put()
			an.tipo = u.tipo
			an.put()
		u.total = [0,0,0,0,0,0,0,0,0,0]
		u.put()
		self.redirect('/unidad')

class UnidadHP(Renderer):
	def get(self,llave):
		llave = int(llave)
		unidad = Unidad.query(Unidad.llave==llave).get()
		asis = Asistente.query().order(Asistente.app)
		ani = Animadora.query().order(Animadora.app)
		curso = Cursos.query().order(Cursos.tipo)
		tipo = UnidadTipo.query()
		self.render("umodificar.html",unidad=unidad,ani=ani,asis=asis,curso=curso,tipo=tipo)
	def post(self,llave):
		llave = int(llave)
		u = Unidad.query(Unidad.llave==llave).get()
		u.nombre = self.request.get('nombre')
		u.codigo = self.request.get('codigo')
		u.direccion = self.request.get('direccion')
		u.telefono = self.request.get('telefono')
		u.dia = self.request.get('dia')
		u.hora = self.request.get('hora')
		u.ciudad = self.request.get('ciudad')
		if u.tipo == "Parroquia":
			u.parroco = self.request.get('parroco')
			if self.request.get('virgen') != '':
				u.virgen = self.request.get('virgen')
		curso = self.request.get('curso')
		if curso != '':
			curso = int(curso)
			u.cursos = curso
		t = self.request.get('tipo')
		if t != '':
			u.tipo = t
		u.ciudad = self.request.get('ciudad')
		u.put()
		self.redirect('/unidad')
class UnidadD(Renderer):
	def get(self,llave):
		llave = int(llave)
		m = Meses.query(Meses.unidad==llave)
		if m:
			for me in m:
				me.key.delete()
		l = Llamadas.query(Llamadas.unidad==llave)
		if l:
			for ll in l:
				ll.key.delete()
		u = Unidad.query(Unidad.llave==llave).get()
		for x in u.asistente:
			a = Asistente.query(Asistente.llave==x).get()
			a.tipo = "NA"
			a.put()
		for x in u.animadora:
			a = Animadora.query(Animadora.llave==x).get()
			a.tipo = "NA"
			a.put()
		u.key.delete()
		self.redirect('/unidad')
		
class UnidadAasis(Renderer):
	def get(self,llave):
		user = users.get_current_user()
		if user:
			u = UsuariosModel.query(UsuariosModel.usuario==user).get()
			if u:
				if u.grado == 1:
					self.redirect('/new')
		else:
			self.redirect('/new2')
		llave = int(llave)
		u = Unidad.query(Unidad.llave==llave).get()
		grados = Grado.query().order(Grado.nombre)
		self.render("asisagregar.html",u=u,grados=grados,user=user)
	def post(self,llave):
		llave = int(llave)
		a = Asistente()
		a.nombre = self.request.get('nombre')
		a.app = self.request.get('app')
		a.apm = self.request.get('apm')
		a.cumple = self.request.get('cumple')
		a.telefono = self.request.get('telefono')
		a.celular = self.request.get('celular')
		a.correo = self.request.get('correo')
		g = int(self.request.get('grado'))
		a.grado = g
		k = a.put()
		a.llave = k.id()
		m = MesesAsis()
		MesesAsis.asis(m,llave,a.llave)
		u = Unidad.query(Unidad.llave==llave).get()
		u.asistente.append(a.llave)
		u.put()
		a.tipo = u.tipo
		a.put()
		self.redirect('/uagregarasis/' + str(llave) )

class UnidadAasisD(Renderer):	
	def get(self,llave,asis):
		llave = int(llave)
		asis = int(asis)
		u = Unidad.query(Unidad.llave==llave).get()
		u.asistente.remove(asis)
		u.put()
		a = Asistente.query(Asistente.llave==asis).get()
		a.tipo = "NA"
		a.put()
		m = Meses.query(Meses.unidad==llave,Meses.asistente==asis).get()
		m.key.delete()
		self.redirect('/umodificar/' + str(llave))
		
class UnidadAani(Renderer):
	def get(self,llave):
		user = users.get_current_user()
		if user:
			u = UsuariosModel.query(UsuariosModel.usuario==user).get()
			if u:
				if u.grado == 1:
					self.redirect('/new')
		else:
			self.redirect('/new2')
		llave = int(llave)
		u = Unidad.query(Unidad.llave==llave).get()
		self.render("aniagregar.html",u=u,user=user)
	def post(self,llave):
		llave = int(llave)
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
		m = MesesAsis()
		MesesAsis.asis(m,llave,a.llave)
		u = Unidad.query(Unidad.llave==llave).get()
		u.animadora.append(a.llave)
		u.put()
		if a.coordinadora == "si":
			l = Llamadas()
			l.unidad = llave
			l.coordinadora = k.id()
			l.telefono = a.telefono
			l.celular = a.celular
			l.observaciones = ''
			l.tipo = u.tipo
			kk = l.put()
			l.llave = kk.id()
			l.put()
		a.tipo = u.tipo
		a.put()
		self.redirect('/uagregarani/' + str(llave) )

class UnidadAaniD(Renderer):	
	def get(self,llave,asis):
		llave = int(llave)
		asis = int(asis)
		u = Unidad.query(Unidad.llave==llave).get()
		u.animadora.remove(asis)
		u.put()
		a = Animadora.query(Animadora.llave==asis).get()
		a.tipo = "NA"
		a.put()
		if a.coordinadora=="si":
			l = Llamadas.query(Llamadas.unidad==llave,Llamadas.coordinadora==asis).get()
			l.key.delete()
		m = Meses.query(Meses.unidad==llave,Meses.asistente==asis).get()
		m.key.delete()
		self.redirect('/umodificar/' + str(llave))
#--------------------------------------/Unidad----------------------------------------------------#
#--------------------------------------Llamadas---------------------------------------------------#
class LlamadasH(Renderer):
	def get(self):
		user = users.get_current_user()
		if user:
			u = UsuariosModel.query(UsuariosModel.usuario==user).get()
			if u:
				if u.grado == 1:
					self.redirect('/new')
		else:
			self.redirect('/new2')
		llamadas = Llamadas.query(Llamadas.tipo=="Parroquia")
		unidad = Unidad.query(Unidad.tipo=="Parroquia").order(Unidad.nombre)
		ani = Animadora.query().order(Animadora.app)
		tipos = UnidadTipo.query().order(Unidad.tipo)
		x = "Parroquia"
		self.render("llamadas.html",ani=ani,llamadas=llamadas,unidad=unidad,tipos=tipos,x=x,user=user)
		
class LlamadasHT(Renderer):
	def get(self,tipo):
		user = users.get_current_user()
		if user:
			u = UsuariosModel.query(UsuariosModel.usuario==user).get()
			if u:
				if u.grado == 1:
					self.redirect('/new')
		else:
			self.redirect('/new2')
		llamadas = Llamadas.query(Llamadas.tipo==tipo)
		unidad = Unidad.query(Unidad.tipo==tipo).order(Unidad.nombre)
		ani = Animadora.query().order(Animadora.app)
		tipos = UnidadTipo.query().order(Unidad.tipo)
		x = tipo
		self.render("llamadas.html",ani=ani,llamadas=llamadas,unidad=unidad,tipos=tipos,x=x)
#-------------------------------------/Llamadas---------------------------------------------------#
#---------------------------------------Eventos---------------------------------------------------#
class EventosH(Renderer):
	def get(self):
		user = users.get_current_user()
		if user:
			u = UsuariosModel.query(UsuariosModel.usuario==user).get()
			if u:
				if u.grado == 1:
					self.redirect('/new')
		else:
			self.redirect('/new2')
		eventos = Evento.query().order(Evento.nombre)
		self.render("eventos.html",eventos=eventos,user=user)
	
class EventosAsis(Renderer):
	def get(self):
		user = users.get_current_user()
		if user:
			u = UsuariosModel.query(UsuariosModel.usuario==user).get()
			if u:
				if u.grado == 1:
					self.redirect('/new')
		else:
			self.redirect('/new2')
		unidad = Unidad.query().order(Unidad.tipo)
		ani = Animadora.query().order(Animadora.coordinadora,Animadora.app)
		self.render("easis.html",unidad=unidad,ani=ani)
		
class EventosHPO(Renderer):
	def get(self):
		user = users.get_current_user()
		if user:
			u = UsuariosModel.query(UsuariosModel.usuario==user).get()
			if u:
				if u.grado == 1:
					self.redirect('/new')
		else:
			self.redirect('/new2')
		unidad = Unidad.query().order(Unidad.tipo)
		ani = Animadora.query().order(Animadora.coordinadora,Animadora.app)
		self.render("ecrear.html",unidad=unidad,ani=ani)
	def post(self):
		eve = Evento()
		eve.nombre = self.request.get('nombre')
		eve.fecha = self.request.get('fecha')
		k = eve.put()
		eve.llave = k.id()
		eve.put()
		all = self.request.get_all('a')
		ani = Animadora.query()
		for a in ani:
			e = EAni()
			e.evento = k.id()
			e.ani = a.llave
			if a.llave in all:
				e.asistio = 'si'
			else:
				e.asistio = 'no'
			e.observaciones = self.request.get(str(a.llave))
			e.put()
		self.redirect('/eventos')
#--------------------------------------/Eventos---------------------------------------------------#
#----------------------------------------Meses----------------------------------------------------#
class MesesAsis(Renderer):
	def asis(self,unidad,a):
		meses = Meses()
		meses.unidad = unidad
		meses.asistente = a
		meses.semanas = [Semanas(s1='0',s2='0',s3='0',s4='0',ss='0'),
						 Semanas(s1='0',s2='0',s3='0',s4='0',ss='0'),
						 Semanas(s1='0',s2='0',s3='0',s4='0',ss='0'),
						 Semanas(s1='0',s2='0',s3='0',s4='0',ss='0'),
						 Semanas(s1='0',s2='0',s3='0',s4='0',ss='0'),
						 Semanas(s1='0',s2='0',s3='0',s4='0',ss='0'),
						 Semanas(s1='0',s2='0',s3='0',s4='0',ss='0'),
						 Semanas(s1='0',s2='0',s3='0',s4='0',ss='0'),
						 Semanas(s1='0',s2='0',s3='0',s4='0',ss='0'),
						 Semanas(s1='0',s2='0',s3='0',s4='0',ss='0')]
		meses.put()
		return
#---------------------------------------/Meses----------------------------------------------------#
#---------------------------------------Semanas---------------------------------------------------#
class SemanasH(Renderer):
	def get(self,llave):
		user = users.get_current_user()
		if user:
			u = UsuariosModel.query(UsuariosModel.usuario==user).get()
			if u:
				if u.grado == 1:
					self.redirect('/new')
		else:
			self.redirect('/new2')
		llave = int(llave)
		x = 0
		mes = "Enero"
		meses = Meses.query(Meses.unidad==llave)
		unidad = Unidad.query(Unidad.llave==llave).get()
		asis = Asistente.query().order(Asistente.app)
		ani = Animadora.query().order(Animadora.app)
		self.render("semanas.html",meses=meses,u=unidad,asis=asis,ani=ani,xx=x,mes=mes,user=user)

class SemanasHM(Renderer):
	def get(self,llave,xx):
		user = users.get_current_user()
		if user:
			u = UsuariosModel.query(UsuariosModel.usuario==user).get()
			if u:
				if u.grado == 1:
					self.redirect('/new')
		else:
			self.redirect('/new2')
		seleccion = {0:"Enero", 1:"Febrero", 2:"Marzo", 3:"Abril", 4:"Mayo", 5:"Junio", 6:"Septiembre", 7:"Octubre", 8:"Noviembre", 9:"Diciembre"}
		llave = int(llave)
		xx = int(xx)
		mes = seleccion[xx]
		meses = Meses.query(Meses.unidad==llave)
		unidad = Unidad.query(Unidad.llave==llave).get()
		asis = Asistente.query().order(Asistente.app)
		ani = Animadora.query().order(Animadora.app)
		self.render("semanas.html",meses=meses,u=unidad,asis=asis,ani=ani,xx=xx,mes=mes,user=user)
	def post(self,llave,xx):
		llave = int(llave)
		xx = int(xx)
		all = self.request.get_all('a')
		s1 = self.request.get('s1')
		s2 = self.request.get('s2')
		s3 = self.request.get('s3')
		s4 = self.request.get('s4')
		ss = self.request.get('ss')
		total = self.request.get('totales')
		for a in all:
			a = int(a)
			se = Meses.query(Meses.unidad == llave, Meses.asistente == a).get()
			if se:
				if s1 != '':
					se.semanas[xx].s1 = s1
				if s2 != '':
					se.semanas[xx].s2 = s2
				if s3 != '':
					se.semanas[xx].s3 = s3
				if s4 != '':
					se.semanas[xx].s4 = s4
				if ss != '':
					se.semanas[xx].ss = ss
				se.put()
		if total != '':
			u = Unidad.query(Unidad.llave==llave).get()
			u.total[xx] = int(total)
			u.put()
		self.redirect('/semanass/' + str(llave) + '/' + str(xx))
		
#--------------------------------------/Semanas---------------------------------------------------#	
#---------------------------------------Reporte---------------------------------------------------#		
class ReporteH(Renderer):
	def get(self):
		"""user = users.get_current_user()
		if user:
			u = UsuariosModel.query(UsuariosModel.usuario==user).get()
			if u:
				if u.grado == 1:
					self.redirect('/new')
		else:
			self.redirect('/new2')"""
		u = Unidad.query(Unidad.tipo == 'Gobierno')
		r = ReporteMensual()
		r.reporte.uBasicoGobierno = len(u)
		r.put()
#--------------------------------------/Reporte---------------------------------------------------#	
app = webapp2.WSGIApplication([
    ('/', MainHandler),
	('/grado',GradoH),#get,post
	('/grado/(.*)',GradoHP),#put
	('/geliminar/(.*)',GradoD),#delete
	('/asistente',AsistenteH),#get
	('/asisagregar',AsistenteHPO),#post
	('/asismodificar/(.*)',AsistenteHP),#put
	('/asiseliminar/(.*)',AsistenteD),#delete
	('/animadora',AnimadoraH),#get
	('/aniagregar',AnimadoraHPO),#post
	('/animodificar/(.*)',AnimadoraHP),#put
	('/anieliminar/(.*)',AnimadoraD),#delete
	('/curso',CursosH),#get
	('/cagregar',CursosH),#post
	('/cmodificar/(.*)',CursosHP),#put
	('/celiminar/(.*)',CursoD),#delete
	('/unidad',UnidadH),#get
	('/unidad/(.*)',UnidadHT),
	('/unidaddirectorio',UnidadDir),
	('/uagregar',UnidadHPO),#post
	('/umodificar/(.*)',UnidadHP),#put
	('/ueliminar/(.*)',UnidadD),#delete
	('/uagregarasis/(.*)',UnidadAasis),
	('/uagregarani/(.*)',UnidadAani),
	('/uasisd/(.*)/(.*)',UnidadAasisD),
	('/uanid/(.*)/(.*)',UnidadAaniD),
	('/llamadas',LlamadasH),
	('/llamadas/(.*)',LlamadasHT),
	('/eventos',EventosH),
	('/ecrear',EventosHPO),
	('/easistencia',EventosAsis),
	('/semanas/(.*)',SemanasH),
	('/semanass/(.*)/(.*)',SemanasHM),
	('/reporte',ReporteH),
	('/login',Login),
	('/logout',Logout),
	('/new',ControlH),
	('/new2',ControlH2)
], debug=True)

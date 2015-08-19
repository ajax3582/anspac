from render import Renderer
import webapp2
from Models import *
from google.appengine.api import users

class Cron(Handler):
	def get(self):
		u = Unidad.query(Unidad.tipo == 'Gobierno')
		r = ReporteMensual()
		r.reporte.uBasicoGobierno = len(u)
		r.put()
		return
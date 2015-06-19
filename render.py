import webapp2
import os
import jinja2

#---------------------------< JINJA2 ENVIRONMENT >------------------------------------------
template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

#------------------------------< GLOBAL METHODS >--------------------------------------
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)
############<<<<MAIN HANDLER FOR RENDERING CALLED--[ Renderer ]-- >>>#########
class Renderer(webapp2.RequestHandler):
    def write(self, *a, **params):
        self.response.out.write(*a, **params)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **params):
        self.write(self.render_str(template, **params))

    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(factory=jinja2_factory)
#############################################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#						HERE STARTS THE REAL SHEET
#____________________________________________________________________________________________

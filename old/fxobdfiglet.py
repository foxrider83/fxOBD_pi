'''
Asciimatics classes for fxOBD
'''
import datetime
import time
from asciimatics.effects import Print
from asciimatics.renderers import BarChart, FigletText, DynamicRenderer
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError

class FigletClock(DynamicRenderer):
    '''
    Classe a mettre dans un fichier a part ifxasciimatics.py.
    Creer les attributs width et height en fonction des messages.
    Faire une selection de messages
    '''
    #Essai en passant le message en parametre - ko.
    #def __init__(self, DynamicRenderer, message):
    #    msg = message    
    
    def _render_now(self):
        message = time.strftime("%A %d %B %Y %H:%M:%S")
        renderer = FigletText(message, font= u'term')
        #renderer = FigletText(msg, font= u'term')
        #renderer2 = RotatedDuplicate(self._width,self._height, renderer)
        return renderer.rendered_text
    #end _render_now

class FigletSpeed(DynamicRenderer):
    '''
    Classe permettant un affichage dynamique de la vitesse
    '''
    def _render_now(self):
        #Aller chercher la vitesse dans l'objet OBD.    
        message = "80"
        renderer = FigletText(message, font = u'lcd')
        return renderer.rendered_text
    #end _render_now

class FigletRPM(DynamicRenderer):
    '''
    Classe permettant un affichage dynamique de la vitesse
    '''
    def _render_now(self):
        #Aller chercher la vitesse dans l'objet OBD.    
        message = "30"
        renderer = FigletText(message, font = u'lcd')
        return renderer.rendered_text
    #end _render_now

class FigletExtTemp(DynamicRenderer):
    '''
    Classe permettant un affichage dynamique de la temperature exterieure
    '''
    def _render_now(self):
        no_op = 0
    #end _render_now

class FigletEngTemp(DynamicRenderer):
    '''
    Classe permettant un affichage dynamique de la temperature moteur
    '''
    def _render_now(self):
        no_op = 0
    #end _render_now


#TODO : Fonction a debugger. Ne prends pas les parametres.
class FigletVar(DynamicRenderer):
    '''
    Dynamic render for Var
    '''
    def __init__(self, height, width, variable):
        _width = width
        _height = height
        print(height)
        
    def _render_now(variable):
        #Get the variable from OBD object read in the file
        renderer = FigletText( variable, font = u'lcd')
        return renderer.rendered_text
    #end _render_now
    

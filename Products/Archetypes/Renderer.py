import sys
#from Products.Archetypes.interfaces.layer import ILayer
from Products.generator.renderer import renderer as BaseRenderer
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Acquisition import ImplicitAcquisitionWrapper

_marker = []

class ArchetypesRenderer(BaseRenderer):
    # XXX it says it's implementing layer but it doesn't implement the required
    # methods!
    #__implements__ = ILayer
    
    security = ClassSecurityInfo()
    # XXX FIXME more security
    
    def setupContext(self, field_name, mode, widget, instance, field, \
                     accessor, **kwargs):

        # look for the context in the stack
        frame = sys._getframe()
        context = _marker
        while context is _marker and frame is not None:
            context = frame.f_locals.get('econtext', _marker)
            frame = frame.f_back
        if context is _marker:
            raise RuntimeError, 'Context not found'
        
        # for editing of multiple AT-based content at once we might want to 
        # prefix the field-name.
        if 'fieldprefix' in kwargs:
            field_name = '%s%s' % (kwargs['fieldprefix'], field_name)

        widget = ImplicitAcquisitionWrapper(widget, instance)
        field = ImplicitAcquisitionWrapper(field, instance)
        context.setLocal('here', instance)
        context.setLocal('fieldName', field_name)
        context.setLocal('accessor', accessor)
        context.setLocal('widget', widget)
        context.setLocal('field', field)
        context.setLocal('mode', mode)

        if kwargs:
            for k,v in kwargs.items():
                context.setLocal(k, v)

        del frame
        return context

InitializeClass(ArchetypesRenderer)

renderer = ArchetypesRenderer()
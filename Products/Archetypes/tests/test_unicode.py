import unittest

# that trigger zope import
from test_classgen import Dummy


from Products.Archetypes.Field import *
from Products.PortalTransforms.MimeTypesRegistry import MimeTypesRegistry
from Products.Archetypes.BaseUnit import BaseUnit
from Products.PortalTransforms.data import datastream
instance = Dummy()

class FakeTransformer:
    def __init__(self, expected):
        self.expected = expected
        
    def convertTo(self, target_mimetype, orig, data=None, object=None, **kwargs):
        assert orig == self.expected
        if data is None:
            data = datastream('test')
        data.setData(orig)
        return data
    
class UnicodeStringFieldTest( unittest.TestCase ):
    
    def test_set(self):
        f = StringField('test')
        f.set(instance, 'h\xc3\xa9h\xc3\xa9h\xc3\xa9')
        self.failUnlessEqual(f.get(instance), 'h\xc3\xa9h\xc3\xa9h\xc3\xa9')
        self.failUnlessEqual(f.get(instance, encoding="ISO-8859-1"), 'h�h�h�')
        f.set(instance, 'h�h�h�', encoding='ISO-8859-1')
        self.failUnlessEqual(f.get(instance), 'h\xc3\xa9h\xc3\xa9h\xc3\xa9')
        self.failUnlessEqual(f.get(instance, encoding="ISO-8859-1"), 'h�h�h�')
        f.set(instance, u'h�h�h�')
        self.failUnlessEqual(f.get(instance), 'h\xc3\xa9h\xc3\xa9h\xc3\xa9')
        self.failUnlessEqual(f.get(instance, encoding="ISO-8859-1"), 'h�h�h�')
            
class UnicodeLinesFieldTest( unittest.TestCase ):
    
    def test_set1(self):
        f = LinesField('test')
        f.set(instance, 'h\xc3\xa9h\xc3\xa9h\xc3\xa9')
        self.failUnlessEqual(f.get(instance), ['h\xc3\xa9h\xc3\xa9h\xc3\xa9'])
        self.failUnlessEqual(f.get(instance, encoding="ISO-8859-1"), ['h�h�h�'])
        f.set(instance, 'h�h�h�', encoding='ISO-8859-1')
        self.failUnlessEqual(f.get(instance), ['h\xc3\xa9h\xc3\xa9h\xc3\xa9'])
        self.failUnlessEqual(f.get(instance, encoding="ISO-8859-1"), ['h�h�h�'])
        f.set(instance, u'h�h�h�')
        self.failUnlessEqual(f.get(instance), ['h\xc3\xa9h\xc3\xa9h\xc3\xa9'])
        self.failUnlessEqual(f.get(instance, encoding="ISO-8859-1"), ['h�h�h�'])

    def test_set2(self):
        f = LinesField('test')
        f.set(instance, ['h\xc3\xa9h\xc3\xa9h\xc3\xa9'])
        self.failUnlessEqual(f.get(instance), ['h\xc3\xa9h\xc3\xa9h\xc3\xa9'])
        self.failUnlessEqual(f.get(instance, encoding="ISO-8859-1"), ['h�h�h�'])
        f.set(instance, ['h�h�h�'], encoding='ISO-8859-1')
        self.failUnlessEqual(f.get(instance), ['h\xc3\xa9h\xc3\xa9h\xc3\xa9'])
        self.failUnlessEqual(f.get(instance, encoding="ISO-8859-1"), ['h�h�h�'])
        f.set(instance, [u'h�h�h�'])
        self.failUnlessEqual(f.get(instance), ['h\xc3\xa9h\xc3\xa9h\xc3\xa9'])
        self.failUnlessEqual(f.get(instance, encoding="ISO-8859-1"), ['h�h�h�'])
            
class UnicodeTextFieldTest( unittest.TestCase ):
    
    def test_set(self):
        f = TextField('test')
        f.set(instance, 'h\xc3\xa9h\xc3\xa9h\xc3\xa9', mimetype='text/plain')
        self.failUnlessEqual(f.getRaw(instance), 'h\xc3\xa9h\xc3\xa9h\xc3\xa9')
        self.failUnlessEqual(f.getRaw(instance, encoding="ISO-8859-1"), 'h�h�h�')
        f.set(instance, 'h�h�h�', encoding='ISO-8859-1', mimetype='text/plain')
        self.failUnlessEqual(f.getRaw(instance), 'h\xc3\xa9h\xc3\xa9h\xc3\xa9')
        self.failUnlessEqual(f.getRaw(instance, encoding="ISO-8859-1"), 'h�h�h�')
        f.set(instance, u'h�h�h�', mimetype='text/plain')
        self.failUnlessEqual(f.getRaw(instance), 'h\xc3\xa9h\xc3\xa9h\xc3\xa9')
        self.failUnlessEqual(f.getRaw(instance, encoding="ISO-8859-1"), 'h�h�h�')
            

class UnicodeBaseUnitTest(unittest.TestCase):
    def setUp(self):
        self.bu = BaseUnit('test', 'h�h�h�', instance, mimetype='text/plain', encoding='ISO-8859-1')
        
    def test_store(self):
        self.failUnless(type(self.bu.raw is type(u'')))
        
    def test_getRaw(self):
        self.failUnlessEqual(self.bu.getRaw(), 'h\xc3\xa9h\xc3\xa9h\xc3\xa9')
        self.failUnlessEqual(self.bu.getRaw('ISO-8859-1'), 'h�h�h�')
        
    def test_transform(self):
        instance = Dummy()
        instance.portal_transforms = FakeTransformer('h�h�h�')
        transformed = self.bu.transform(instance, 'text/plain')
        self.failUnlessEqual(transformed, 'h\xc3\xa9h\xc3\xa9h\xc3\xa9')
        
    
def test_suite():
    return unittest.TestSuite([unittest.makeSuite(UnicodeStringFieldTest),
                               unittest.makeSuite(UnicodeLinesFieldTest),
                               unittest.makeSuite(UnicodeTextFieldTest),
                               unittest.makeSuite(UnicodeBaseUnitTest),
                               ])

if __name__=='__main__':
    unittest.main(defaultTest='test_suite')
# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import alsoProvides
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from plone.supermodel import directives

class IDokuPraevention(model.Schema):

    directives.fieldset('blaettern', 
                        label=u'Doku-Prävention',
                        fields=('vorgaenger', 'nachfolger'),
                       )

    vorgaenger = schema.TextLine(
              title=u"Vorgänger",
              description=u"Bitte tragen Sie den Webcode des Vorgängerdokuments ein.",
              required = False,
              )

    nachfolger = schema.TextLine(
              title=u"Nachfolger",
              description=u"Bitte tragen Sie den Webcode des Nachfolgerdokuments ein.",
              required = False,
              )

alsoProvides(IDokuPraevention,IFormFieldProvider)

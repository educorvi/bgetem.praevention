# -*- coding: utf-8 -*-
from five import grok
import random
from time import strftime, localtime
from DateTime import DateTime
from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder, IContextAwareDefaultFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from Products.CMFCore.utils import getToolByName
from bgetem.praevention import MessageFactory as _
from Products.ATContentTypes.interfaces import IATImage

from plone.directives import form as directivesform
from plone.formwidget.multifile import MultiFileFieldWidget
from z3c.form.browser.checkbox import CheckBoxFieldWidget

from plone.supermodel import directives

from collective.z3cform.datagridfield import DictRow, DataGridFieldFactory


@grok.provider(IContextAwareDefaultFactory)
def genWebcode(context):
    aktuell=unicode(DateTime()).split(' ')[0]
    neujahr='%s/01/01' %str(DateTime()).split(' ')[0][:4]
    konstante=unicode(aktuell[2:4])
    zufallszahl=unicode(random.randint(100000, 999999))
    code=konstante+zufallszahl
    pcat=getToolByName(context,'portal_catalog')
    results = pcat(Webcode=code, created={"query":[neujahr,aktuell],"range":"minmax"})
    while results:
        zufallszahl=unicode(random.randint(100000, 999999))
        code=konstante+zufallszahl
        results = pcat(Webcode=code, created={"query":[neujahr,aktuell],"range":"minmax"})
    return code

class ILink(form.Schema):

    title = schema.TextLine(title = u"Titel des Links")
    url = schema.URI(title = u"URL des Links")

class IDokuPraevention(form.Schema, IImageScaleTraversable):
    """
    Artikeltyp zur Erfassung von Dokumentationen im Bereich Praevention der BG ETEM.
    """

    directives.fieldset('doku_details',
                        label=u'gut zu wissen',
                        fields=('details',),
                       )

    directives.fieldset('doku_zusatzinfos',
                        label=u'weiss nicht jeder',
                        fields=('zusatzinfos',),
                       )

    directives.fieldset('doku_bilder',
                        label=u'Bilder',
                        fields=('titelbilder', 'bilder','nachrichtenbild','bildtitel'),
                       )

    directives.fieldset('doku_dateien_links',
                        label=u'Dateien/Links',
                        fields=('dateien','links'),
                       )

    ueberschrift = schema.TextLine(title=u"Überschrift",
                   description=u"Hier können Sie dem Dokument eine Überschrift geben und damit den Title überschrieben.",
                   required = False,)

    haupttext = RichText(
                title=u"wichtig zu wissen",
                description=u"(grundlegende Informationen zum Thema - Haupttext)",
                required = True,
                )

    details = RichText(
              title=u"gut zu wissen",
              description=u"(detaillierte Informationen ergänzend zu den Grundlagen)",
              required = False,
              )

    zusatzinfos = RichText(
              title=u"weiss nicht jeder",
              description=u"(Interessantes und Wissenswertes, ergänzend zu den Grundlagen und Details)",
              required = False,
              )

    titelbilder = RelationList(title=u"Titelbilder",
                           description=u"(Anzeige im Kopf der Seite)",
                           default=[],
                           value_type=RelationChoice(title=_(u"Titelbilder"),
                                                     source=ObjPathSourceBinder()),
                           required=False,)

    bilder = RelationList(
              title=u"Illustration",
              description=u"(Bilder zur Anzeige unterhalb der Inhaltstexte)",
              value_type=RelationChoice(title=u"Bilder", 
                                        source=ObjPathSourceBinder()),
              required=False,
              )

    webcode = schema.TextLine(
              title=u"Webcode",
              description=u"Der Webcode für diesen Artikel wird automatisch errechnet und angezeigt. Sie\
                          können diesen Webcode bei Bedarf jedoch jederzeit überschreiben.",
              required = True,
              defaultFactory = genWebcode,
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

    weiterlesen = RelationList(title=u"Dokumente zum Weiterlesen",
                           description=u"Bitte wählen Sie hier Dokumente aus, die Sie dem Benutzer zum\
                                   Weiterlesen empfehlen.",
                           default=[],
                           value_type=RelationChoice(title=_(u"Weiterlesen"),
                                                     source=ObjPathSourceBinder()),
                           required=False,)

    nachrichtenbild = RelationChoice(
        title=u"Vorschaubild",
        description=u"(Anzeige in Verweisboxen oder Ordneransichten)",
        source=ObjPathSourceBinder(),
        required=False,
        )

    bildtitel = schema.TextLine(
              title=u"Titel des Vorschaubildes",
              required = False,
              )

    directivesform.widget(dateien=MultiFileFieldWidget)
    dateien = schema.List(title = u'Ihre Dateien für dieses Dokument',
                             value_type=NamedBlobFile(),
                             required = False,)

    form.widget(links=DataGridFieldFactory)
    links = schema.List(title = u'Ihre Links für dieses Dokument',
                        value_type=DictRow(title=u"Link", schema=ILink),
                        required = False,)


class DokuPraevention(Container):
    grok.implements(IDokuPraevention)

    def getWebcode(self):
        """Emulate a Archetypes Accessor"""
        return self.webcode

class SampleView(grok.View):
    """ sample view class """

    grok.context(IDokuPraevention)
    grok.require('zope2.View')

    # grok.name('view')
    # Add view methods here

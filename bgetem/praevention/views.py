from zope.interface import Interface
import transaction
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from uvc.api import api
from bgetem.praevention.doku_praevention import IDokuPraevention

api.templatedir('templates')

class RunView(api.View):
    api.context(Interface)

    def render(self):
        pcat = getToolByName(self.context, 'portal_catalog')
        brains = pcat()
        print len(brains)
        for i in brains:
            if not i.portal_type in ['PloneGlossaryDefinition', 'Document']:
                if hasattr(i.getObject(), 'refwebcodes'):
                    print i.Title
                    delattr(i.getObject(), 'refwebcodes')
                    transaction.commit()

class FolderViewView(api.View):
    api.context(Interface)

    def render(self):
        pcat = getToolByName(self.context, 'portal_catalog')
        brains = pcat(portal_type='Folder')
        for i in brains:
            obj = i.getObject()
            if obj.layout != 'contentboxview':
                print obj.title
                print obj.absolute_url()

class MyTestView(api.Page):
    api.context(Interface)

    def update(self):
        pcat = getToolByName(self.context, 'portal_catalog')
        brains = pcat(portal_type='PloneGlossaryDefinition', sort_on='sortable_title', sort_order='ascending')
        objectlist = []
        for i in brains:
            entry = {}
            myobj = i.getObject()
            url = myobj.absolute_url()
            entry['url'] = myobj.Title()
            myfield = myobj.getField('refwebcodes')
            mywebcodes = myfield.get(myobj)
            entrylist = []
            for i in mywebcodes:
                 newbrains = pcat(Webcode=i, review_state="published")
                 if newbrains:
                     entrylist.append(i)
            if not entrylist:
                suchbegriff = myobj.Title().replace('(','')
                suchbegriff = suchbegriff.replace(')','')
                suchbegriff = suchbegriff.split(' ')
                brains = pcat.searchResults(portal_type=["Folder", "bgetem.praevention.dokupraevention" ], SearchableText=suchbegriff)
                for i in brains:
                    obj = i.getObject()
                    entrylist.append(obj.webcode)
            myfield.set(myobj, entrylist)
            transaction.commit()
            entry['codes'] = entrylist
            objectlist.append(entry)
        self.objectlist = objectlist

class FAQTestView(api.Page):
    api.context(Interface)

    def update(self):
        pcat = getToolByName(self.context, 'portal_catalog')
        brains = pcat(portal_type='Document', path="/praevention/oft-gestellte-fragen", sort_on='sortable_title', sort_order='ascending')
        objectlist = []
        for i in brains:
            entry = {}
            myobj = i.getObject()
            url = myobj.absolute_url()
            entry['url'] = myobj.Title()
            mywebcodes = myobj.refwebcodes
            if not mywebcodes:
                mywebcodes = []
            entrylist = []
            for i in mywebcodes:
                 newbrains = pcat(Webcode=i, review_state="published")
                 if newbrains:
                     entrylist.append(i)
            myobj.refwebcodes = entrylist
            transaction.commit()
            entry['codes'] = entrylist
            objectlist.append(entry)
        self.objectlist = objectlist

class MyDownload(api.View):
    api.context(IDokuPraevention)

    def render(self):
        index = int(self.request.get('docindex'))
        datei = self.context.dateien[index]
        filename = datei.filename
        contenttype = datei.contentType
        RESPONSE = self.request.response
        RESPONSE.setHeader('content-type', contenttype)
        RESPONSE.setHeader('content-disposition', 'attachment; filename=%s' %filename)
        return datei.data

class PraevDocView(api.Page):
    api.context(IDokuPraevention)

    def splitContentBoxes(self, refs, size=3):
        if not refs:
            return []
        seq = []
        for i in refs:
            box = {}
            if i.to_object:
                signalcolor = self.getColor(i.to_object)
                box['title'] = i.to_object.title
                box['boxclass'] = 'col-xs-12 col-md-4 panel panel-primary panel-siguv %s' %signalcolor
                box['titleclass'] = signalcolor
                box['imgurl'] = ''
                box['imgcaption'] = ''
                if hasattr(i.to_object, 'nachrichtenbild'):
                    if i.to_object.nachrichtenbild:
                        bild = i.to_object.nachrichtenbild.to_object
                        try:
                            box['imgurl'] = '<img src="%s/@@download/image/%s" width="%s">' % (bild.absolute_url(),
                                                                                       bild.image.filename, "100%")
                        except:
                            box['imgurl'] = bild.tag(width="100%", height="100%")
                    try:
                        box['imgcaption'] = i.to_object.bildtitel
                    except:
                        box['imgcaption'] = i.to_object.title
                if hasattr(i.to_object, 'newsimage'):
                    if i.to_object.newsimage:
                        bild = i.to_object.newsimage.to_object
                        box['imgurl'] = '<img src="%s/@@download/image/%s" width="%s">' % (bild.absolute_url(),
                                                                                   bild.image.filename, "100%")
                    #box['imgcaption'] = i.to_object.bildtitel
                    box['imgcaption'] = ''
                box['url'] = i.to_object.absolute_url()
                box['desc'] = i.to_object.Description
                seq.append(box)
        return [seq[i:i+size] for i  in range(0, len(seq), size)]


    def splitImages(self, bilder, size=6):
        if not bilder:
            return []
        seq = []
        for i in bilder:
            image = {}
            if i.to_object:
                image['id'] = i.to_object.UID()
                image['url'] = i.to_object.absolute_url()
                image['tag'] = '<img src="%s/@@download/image/%s" width="%s">' % (i.to_object.absolute_url(),
                                                                                             i.to_object.image.filename, "120px")
                image['title'] = i.to_object.title
                image['desc'] = i.to_object.Description
                seq.append(image)
        return (seq, [seq[i:i+size] for i  in range(0, len(seq), size)])

    def getModale(self, bilder):
        if not bilder:
            return []
        seq = []
        for i in bilder:
            image = {}
            if i.to_object:
                image['id'] = i.to_object.UID()
                image['url'] = i.to_object.absolute_url()
                image['tag'] = '<img src="%s/@@download/image/%s" width="%s">' % (i.to_object.absolute_url(),
                                                                                  i.to_object.image.filename, "100%")
                image['title'] = i.to_object.title
                image['desc'] = i.to_object.Description
                seq.append(image)
        return seq

    def createDateien(self, dateien):
        if not dateien:
            return []
        dateilist = []
        count = 0
        for i in dateien:
            datei = {}
            datei['title'] = i.filename
            datei['url'] = self.context.absolute_url()+'/@@mydownload?docindex=%s' %count
            count+=1
            dateilist.append(datei)
        return dateilist

    def getAcquisitionChain(self, object):
        inner = object.aq_inner
        iter = inner
        while iter is not None:
            yield iter
            if ISiteRoot.providedBy(iter):
                break
            if not hasattr(iter, "aq_parent"):
                raise RuntimeError("Parent traversing interrupted by object: " + str(parent))
            iter = iter.aq_parent

    def getTopic(self, context):
        parentobjects = self.getAcquisitionChain(context)
        for i in parentobjects:
            if hasattr(i, 'signalcolor'):
                topic = getattr(i, 'signalcolor')
                if topic:
                    return topic
        return 'Mist'

    def getColor(self, context):
        parentobjects = self.getAcquisitionChain(context)
        for i in parentobjects:
            if hasattr(i, 'dguvcolor'):
                topic = getattr(i, 'dguvcolor')
                if topic:
                    return topic
        return 'blau'

    def update(self):
        if self.context.ueberschrift:
            self.title = self.context.ueberschrift
        else:
            self.title = self.context.Title()
        self.text = self.context.haupttext.output
        self.details = ''
        self.zusatzinfos = ''
        if self.context.details:
            self.details = self.context.details.output
        if self.context.zusatzinfos:
            self.zusatzinfos = self.context.zusatzinfos.output
        color = self.getColor(self.context)
        self.tabclass = "nav nav-tabs siguv-tabs %s" %color
        self.bilder = self.splitImages(self.context.bilder)
        self.modale = self.getModale(self.context.bilder)
        self.contentboxes = self.splitContentBoxes(self.context.weiterlesen)
        self.dateien = self.createDateien(self.context.dateien)
        self.links = self.context.links

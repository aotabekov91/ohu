import os
import hashlib
from PyQt5 import QtGui
from zipfile import ZipFile
from xmltodict import parse
from urllib.parse import unquote
from bs4 import BeautifulSoup as Soup
from gizmo.ui.view.model import Model as Base

class EpubModel(Base):

    pattern='.*epub$'

    def setup(self):

        super().setup()
        self.content = []
        self.flist = None
        self.odict = None
        self.zfile = None
        self.schap = {}

    def kind(self):
        return 'document'

    def assignId(self, source):

        if os.path.isfile(source):
            source=os.path.expanduser(source)
            shash = hashlib.md5()
            with open(source, 'rb') as f:
                chunk = f.read(4096)
                while chunk:
                    shash.update(chunk)
                    chunk = f.read(4096)
            dhash=shash.hexdigest()
            self.setId(dhash)
        else:
            self.setId(None)

    def load(self, source):

        self.m_source=source
        self.assignId(source)
        self.setParts()

    def setParts(self):

        self.zfile = ZipFile(
            self.m_source, 
            mode='r', 
            allowZip64=True)
        self.flist = self.zfile.namelist()
        c = self.findPart('container.xml')
        if c:
            cxml = self.zfile.read(c)
            cdict = parse(cxml)
            rfile = cdict['container']['rootfiles']
            pfile = rfile['rootfile']['@full-path']
        else:
            pnames = (
                    'volume.opf',
                    'content.opf', 
                    'package.opf', 
                    )
            for i in pnames:
                pfile = self.findPart(i)
                if pfile: break

        pdata = self.zfile.read(pfile)
        self.odict = parse(pdata)

    def findPart(self, part):

        part = unquote(part)
        if part in self.flist:
            return part
        else:
            fbname = os.path.basename(part)
            for i in self.flist:
                if os.path.basename(i) != fbname:
                    continue
                return i
        return False

    def getPart(self, p):

        p = self.findPart(p)
        if p:
            p= self.zfile.read(p)
            d = QtGui.QTextDocument()
            d.setHtml(p.decode())
            t = d.toPlainText()
            return t.replace('\n', '')
        return 'Possible parse error: ' + p

    def parsePart(self, part):

        for p, anch in part.items():
            self.schap[p] = {}
            c = self.getPart(p)
            s = Soup(c, 'lxml')
            for a in reversed(anch):
                f=lambda x: x == a
                t = s.find(attrs={"id":f})
                m = str(s).split(str(t))
                s = Soup(m[0], 'lxml')
                if t:
                    d=str(t).strip() + m[1]
                    mrk = Soup(d, 'lxml')
                    self.schap[p][a] = str(mrk)
            self.schap[p]['top_level'] = str(s)

    def getContent(self):

        def getSpine(p):

            cspine=[]
            r=p['spine']['itemref']
            try:
                for i in r: 
                    cspine += [i['@idref']]
            except TypeError:
                cspine = [r['@idref']]
            return spine

        def getManifest(p, s):

            man = {}
            m=p['manifest']['item']
            for i in m: 
                man[i['@id']]=i['@href']
            f = []
            for i in cspine:
                try:
                    f.append(m.pop(i))
                except KeyError:
                    pass
            return man, f


        p=self.odict['package']
        cspine=getSpine(p)
        man, sfinal=getManifest(p, cspine)
        tchap = []
        for i in self.content:
            u=unquote(i[2].split('#')[0])
            tchap+=[u]
        for i in sfinal:
            if not i in tchap:
                sidx = sfinal.index(i)
                if sidx == 0: 
                    pchap_idx = -1
                else:
                    pchap = sfinal[sfinal.index(i) - 1]
                    pchap_idx = tchap.index(pchap)
                tchap.insert(pchap_idx + 1, i)
                self.content.insert(
                    pchap_idx + 1, 
                    [1, None, i])
        cscon = {}
        for i in self.content:
            if '#' in i[2]:
                s = i[2].split('#')
                chapter = s[0]
                anchor = s[1]
                try:
                    cscon[chapter].append(anchor)
                except KeyError:
                    cscon[chapter] = []
                    cscon[chapter].append(anchor)
        self.parsePart(cscon)
        tcopy = self.content[:]
        for count, i in enumerate(tcopy):
            chapter_file = i[2]
            if '#' in chapter_file:
                s = chapter_file.split('#')
                chapter_file_proper = s[0]
                this_anchor = s[1]
                try:
                    chapter_content = (
                        self.schap[chapter_file_proper][this_anchor])
                except KeyError:
                    chapter_content = 'Parse Error'
            elif chapter_file in self.schap.keys():
                try:
                    chapter_content = self.schap[chapter_file]['top_level']
                except KeyError:
                    chapter_content = 'Parse Error'
            else:
                chapter_content = self.getPart(chapter_file)
            self.content[count][2] = chapter_content
        uchapt = 1
        cc = []
        for i in self.content:
            if i[2]:
                chapter_title = i[1]
                if not chapter_title:
                    chapter_title = uchapt
                cc.append((
                    i[0], str(chapter_title), i[2]))
            uchapt += 1
        self.content = cc
        return cc

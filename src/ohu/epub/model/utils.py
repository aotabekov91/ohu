import os
from PyQt5 import QtGui
from zipfile import ZipFile
from xmltodict import parse
from urllib.parse import unquote
from bs4 import BeautifulSoup as Soup
from tempfile import TemporaryDirectory

def load(source):

    z = ZipFile(
            source, 
            mode='r', 
            allowZip64=True
            )
    f = z.namelist()
    c = findPart('container.xml', f)
    if c:
        x = z.read(c)
        cdict = parse(x)
        rfile = cdict['container']['rootfiles']
        pfile = rfile['rootfile']['@full-path']
    else:
        n = (
            'volume.opf', 
            'content.opf', 
            'package.opf'
            )
        for i in n:
            pfile = findPart(i, f)
            if pfile: break
    d = parse(z.read(pfile))

    t=TemporaryDirectory()
    z.extractall(t.name)
    return z, f, d, t

def getContent(z, f, d, c=[], s={}):

    p=d.get('package', None)
    if p:
        d=getData(p)
        c=setChaps(d, c)
        prts=getChapParts(c)
        parseSplitChaps(prts, s, f, z)
        c=updateContent(c, s, f, z)
        c=finalizeContent(c)
    return c, s

def getData(p):

    t, man, d = [], {}, []
    r=p['spine']['itemref']
    if type(r)!=list:
        r=[r]
    for i in r: 
        t += [i['@idref']]
    m=p['manifest']['item']
    for i in m: 
        man[i['@id']]=i['@href']
    for i in t:
        if i in man:
            d.append(man.pop(i))
    return d

def unquoteContent(content):

    d = []
    for i in content:
        c=i[2].split('#')[0]
        d+=[unquote(c)]
    return d

def setChaps(data, content):

    chaps=unquoteContent(content)
    for i in data:
        if i in chaps:
            continue
        idx = data.index(i)
        if idx == 0: 
            pidx = -1
        else:
            idx=data.index(i) - 1
            pchap = data[idx]
            pidx = chaps.index(pchap)
        chaps.insert(pidx + 1, i)
        content.insert(
            pidx + 1, [1, None, i])
    return content

def getChapParts(content):

    con = {}
    for i in content:
        if not '#' in i[2]:
            continue
        s = i[2].split('#')
        c, a = s[0], s[1]
        if not c in con:
            con[c]=[]
        con[c].append(a)
    return con

def parseSplitChaps(part, schaps, flist, zfile):

    for p, a in part.items():
        schaps[p] = {}
        c = getPart(p, flist, zfile)
        s = Soup(c, 'lxml')
        for a in reversed(a):
            f=lambda x: x == a
            t = s.find(attrs={"id":f})
            m = str(s).split(str(t))
            s = Soup(m[0], 'lxml')
            if not t:
                continue
            d=str(t).strip() + m[1]
            mrk = Soup(d, 'lxml')
            schaps[p][a] = str(mrk)
        schaps[p]['top_level'] = str(s)

def updateContent(content, chap, flist, zfile):

    c = content[:]
    for j, i in enumerate(c):
        d = i[2]
        if '#' in d:
            s = d.split('#')
            p, a = s[0], s[1]
            pp=chap.get(p, {})
            chapc = pp.get(a, 'Parse Error')
        elif d in chap:
            cd = chap[d]
            chapc= cd.get('top_level', 'Parse Error')
        else:
            chapc = getPart(d, flist, zfile)
        content[j][2] = chapc
    return content

def finalizeContent(content):

    d, c = [], 1
    for i in content:
        if not i[2]:
            continue
        t = i[1] or c
        td=(i[0], str(t), i[2])
        d.append(td)
        c += 1
    return d

def findPart(part, flist):

    part = unquote(part)
    if part in flist:
        return part
    else:
        fbname = os.path.basename(part)
        for i in flist:
            bname=os.path.basename(i)
            if bname == fbname:
                return i
    return False

def getPart(part, flist, zfile):

    p = findPart(part, flist)
    if p:
        p= zfile.read(p)
        return p.decode()
        # d = QtGui.QTextDocument()
        # d.setHtml(p.decode())
        # t = d.toPlainText()
        # return t.replace('\n', '')
    return 'Possible parse error: ' + p

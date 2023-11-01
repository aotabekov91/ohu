import os
import zipfile
import logging
from urllib.parse import unquote

import xmltodict
from PyQt5 import QtGui
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class EPUB:

    def __init__(self, book_filename, temp_dir):

        self.source = book_filename

        self.zip_file = None
        self.file_list = None
        self.opf_dict = None
        self.split_chapters = {}

        self.content = []

        self.generate_references()

    def generate_references(self):

        self.zip_file = zipfile.ZipFile(
            self.source, mode='r', allowZip64=True)
        self.file_list = self.zip_file.namelist()

        # Book structure relies on parsing the .opf file
        # in the book. Now that might be the usual content.opf
        # or package.opf or it might be named after your favorite
        # eldritch abomination. The point is we have to check
        # the container.xml
        container = self.find_file('container.xml')
        if container:
            container_xml = self.zip_file.read(container)
            container_dict = xmltodict.parse(container_xml)
            packagefile = container_dict['container']['rootfiles']['rootfile']['@full-path']
        else:
            presumptive_names = ('content.opf', 'package.opf', 'volume.opf')
            for i in presumptive_names:
                packagefile = self.find_file(i)
                if packagefile:
                    logger.info('Using presumptive package file: ' + self.source)
                    break

        packagefile_data = self.zip_file.read(packagefile)
        self.opf_dict = xmltodict.parse(packagefile_data)

    def find_file(self, filename):
        # Get rid of special characters
        filename = unquote(filename)

        # First, look for the file in the root of the book
        if filename in self.file_list:
            return filename

        # Then search for it elsewhere
        else:
            file_basename = os.path.basename(filename)
            for i in self.file_list:
                if os.path.basename(i) == file_basename:
                    return i

        # If the file isn't found
        logger.warning(filename + ' not found in ' + self.source)
        return False

    def get_chapter_content(self, chapter_file):
        this_file = self.find_file(chapter_file)
        if this_file:
            chapter_content = self.zip_file.read(this_file).decode()

            # Generate a None return for a blank chapter
            # These will be removed from the contents later
            contentDocument = QtGui.QTextDocument(None)
            contentDocument.setHtml(chapter_content)
            contentText = contentDocument.toPlainText().replace('\n', '')
            if contentText == '':
                chapter_content = None

            return chapter_content
        else:
            return 'Possible parse error: ' + chapter_file

    def parse_split_chapters(self, chapters_with_split_content):
        # For split chapters, get the whole chapter first, then split
        # between ids using their anchors, then "heal" the resultant text
        # by creating a BeautifulSoup object. Write its str to the content
        for i in chapters_with_split_content.items():
            chapter_file = i[0]
            self.split_chapters[chapter_file] = {}

            chapter_content = self.get_chapter_content(chapter_file)
            soup = BeautifulSoup(chapter_content, 'lxml')

            split_anchors = i[1]
            for this_anchor in reversed(split_anchors):
                this_tag = soup.find(
                    attrs={"id":lambda x: x == this_anchor})

                markup_split = str(soup).split(str(this_tag))
                soup = BeautifulSoup(markup_split[0], 'lxml')

                # If the tag is None, it probably means the content is overlapping
                # Skipping the insert is the way forward
                if this_tag:
                    this_markup = BeautifulSoup(
                        str(this_tag).strip() + markup_split[1], 'lxml')
                    self.split_chapters[chapter_file][this_anchor] = str(this_markup)

            # Remaining markup is assigned here
            self.split_chapters[chapter_file]['top_level'] = str(soup)

    def generate_content(self):
        # Find all the chapters mentioned in the opf spine
        # These are simply ids that correspond to the actual item
        # as mentioned in the manifest - which is a comprehensive
        # list of files
        try:
            # Multiple chapters
            chapters_in_spine = [
                i['@idref']
                for i in self.opf_dict['package']['spine']['itemref']]
        except TypeError:
            # Single chapter - Large xml
            chapters_in_spine = [
                self.opf_dict['package']['spine']['itemref']['@idref']]

        # Next, find items and ids from the manifest
        # This might error out in case there's only one item in
        # the manifest. Remember that for later.
        chapters_from_manifest = {
            i['@id']: i['@href']
            for i in self.opf_dict['package']['manifest']['item']}

        # Finally, check which items are supposed to be in the spine
        # on the basis of the id and change the toc accordingly
        spine_final = []
        for i in chapters_in_spine:
            try:
                spine_final.append(chapters_from_manifest.pop(i))
            except KeyError:
                pass

        toc_chapters = [
            unquote(i[2].split('#')[0]) for i in self.content]

        for i in spine_final:
            if not i in toc_chapters:
                spine_index = spine_final.index(i)
                if spine_index == 0:  # Or chapter insertion circles back to the end
                    previous_chapter_toc_index = -1
                else:
                    previous_chapter = spine_final[spine_final.index(i) - 1]
                    previous_chapter_toc_index = toc_chapters.index(previous_chapter)

                toc_chapters.insert(
                    previous_chapter_toc_index + 1, i)
                self.content.insert(
                    previous_chapter_toc_index + 1, [1, None, i])

        # Parse split chapters as below
        # They can be picked up during the iteration through the toc
        chapters_with_split_content = {}
        for i in self.content:
            if '#' in i[2]:
                this_split = i[2].split('#')
                chapter = this_split[0]
                anchor = this_split[1]

                try:
                    chapters_with_split_content[chapter].append(anchor)
                except KeyError:
                    chapters_with_split_content[chapter] = []
                    chapters_with_split_content[chapter].append(anchor)

        self.parse_split_chapters(chapters_with_split_content)

        # Now we iterate over the ToC as presented in the toc.ncx
        # and add chapters to the content list
        # In case a split chapter is encountered, get its content
        # from the split_chapters dictionary
        # What could possibly go wrong?
        toc_copy = self.content[:]

        # Put the book into the book
        for count, i in enumerate(toc_copy):
            chapter_file = i[2]

            # Get split content according to its corresponding id attribute
            if '#' in chapter_file:
                this_split = chapter_file.split('#')
                chapter_file_proper = this_split[0]
                this_anchor = this_split[1]

                try:
                    chapter_content = (
                        self.split_chapters[chapter_file_proper][this_anchor])
                except KeyError:
                    chapter_content = 'Parse Error'
                    error_string = (
                        f'Error parsing {self.source}: {chapter_file_proper}')
                    logger.error(error_string)

            # Get content that remained at the end of the pillaging above
            elif chapter_file in self.split_chapters.keys():
                try:
                    chapter_content = self.split_chapters[chapter_file]['top_level']
                except KeyError:
                    chapter_content = 'Parse Error'
                    error_string = (
                        f'Error parsing {self.source}: {chapter_file}')
                    logger.error(error_string)

            # Vanilla non split chapters
            else:
                chapter_content = self.get_chapter_content(chapter_file)

            self.content[count][2] = chapter_content

        # Cleanup content by removing null chapters
        unnamed_chapter_title = 1
        content_copy = []
        for i in self.content:
            if i[2]:
                chapter_title = i[1]
                if not chapter_title:
                    chapter_title = unnamed_chapter_title
                content_copy.append((
                    i[0], str(chapter_title), i[2]))
            unnamed_chapter_title += 1
        self.content = content_copy

        # Get cover image and put it in its place
        # I imagine this involves saying nasty things to it
        # There's no point shifting this to the parser
        # The performance increase is negligible
        cover_image = self.generate_book_cover()

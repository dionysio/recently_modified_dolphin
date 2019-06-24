import argparse
import os
import glob
from itertools import islice

import lxml.etree as ET


class Bookmarks:
    class _Bookmarks:
        def __init__(self, bookmarks_path):
            parser = ET.XMLParser(remove_blank_text=True)
            self.tree = ET.parse(bookmarks_path, parser=parser)
            self.root = self.tree.getroot()
            self.clean_bookmarks()

        def add_place(self, path, title, icon='blue-folder', hidden=False, href='file://'):
            bookmark = ET.SubElement(self.root, 'bookmark')
            bookmark.attrib['href'] = '{}{}'.format(href, path)

            ET.SubElement(bookmark, 'title').text = title

            info = ET.SubElement(bookmark, 'info')
            metadata_icon = ET.SubElement(info, 'metadata')
            bookmark_icon = ET.SubElement(metadata_icon, 'icon', namespace="bookmark")
            bookmark_icon.attrib['name'] = icon

            metadata = ET.SubElement(info, 'metadata')
            is_system_item = ET.SubElement(metadata, 'isSystemItem')
            is_system_item.text = 'false'
            is_hidden = ET.SubElement(metadata, 'isHidden')
            is_hidden.text = 'true' if hidden else 'false'
            is_added_automatically = ET.SubElement(metadata, 'isAddedAutomatically')
            is_added_automatically.text = 'true'

        def __iter__(self):
            yield from self.root.iterchildren('bookmark')

        def clean_bookmarks(self):
            for bookmark in self:
                if bookmark.xpath('./info/metadata/isAddedAutomatically[text()="true"]'):
                    self.root.remove(bookmark)

        def write(self, path, *args, **kwargs):
            return self.tree.write(path, *args, **kwargs)

    def __init__(self, bookmarks_path):
        self.bookmarks_path = bookmarks_path

    def __enter__(self):
        self._bookmarks = self._Bookmarks(self.bookmarks_path)
        return self._bookmarks

    def __exit__(self, *args):
        self._bookmarks.write(self.bookmarks_path, pretty_print=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--entries", type=int, default=5, help="The number of recent entries to include. The default is 5.")
    parser.add_argument("--bookmarks_path", default=os.path.expanduser('~/.local/share/user-places.xbel'), help='The path to bookmarks. Default is "{}"'.format(os.path.expanduser('~/.local/share/user-places.xbel')))
    parser.add_argument("--directory", default=os.path.expanduser("~/Projects/*/"), help='Directory to get the recent entries from. The default is "~/Projects/*/"')
    parser.add_argument("--icon", default="blue-folder", help="The folder icon to use for the entries. The default is blue-folder.")
    args = parser.parse_args()

    with Bookmarks(args.bookmarks_path) as bookmarks:
        for path in islice(sorted(glob.glob(args.directory), key=lambda d: os.stat(d).st_mtime, reverse=True), args.entries):
            name = [i for i in path.split('/') if i][-1]
            name = name.replace('-', ' ').replace('_', ' ').title()
            bookmarks.add_place(path, title=name, icon=args.icon)

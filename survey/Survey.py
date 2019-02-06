from lxml import etree as ET
import re

class Survey:
    def __init__(self, path):
        self.tree = self.open(path)
        self.rels = set()
        self.images()
        self.styles()

        self.clean_rels()

    def open(self, path):
        return ET.parse(path, ET.XMLParser(recover=True))

    def images(self):
        for img in self.tree.findall('.//img'):
            if '[rel ' in img.attrib['src']:
                self.rels.add(img.attrib['src'])

    def styles(self):
        for style in self.tree.findall('.//style'):
            resources = re.findall(r'\s*\[rel\s+\w+\.\w+\]\s*', style.text)

            for res in resources:
                self.rels.add(res)

    def clean_rels(self):
        temp = []
        for rel in self.rels:
            match = re.search(r'\s*\[rel\s+(\w+\.\w+)\s*\]\s*', rel)
            temp.append(match.group(1))

        self.rels = temp

    def resources(self):
        return self.rels

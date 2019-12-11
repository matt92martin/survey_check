#!/usr/bin/env python
from sys import exit
import os
import re
import argparse
from lxml import etree as ET

class Survey:
    def __init__(self, path):
        self.tree = self.open(path)
        self.rels = set()
        self.images()
        self.others()

    def open(self, path):
        return ET.parse(path, ET.XMLParser(recover=True))

    def images(self):
        for img in self.tree.findall('.//img'):
            if '[rel ' in img.attrib['src']:
                self.rels.add(self.clean_rels(img.attrib['src']))

    def others(self):
        for style in self.tree.findall('.//style') + self.tree.findall('.//res'):
            resources = re.findall(r'\s*\[rel\s+\w+\.\w+\]\s*', ET.tostring(style))

            for res in resources:
                self.rels.add(self.clean_rels(res))

    def clean_rels(self, rel):
        match = re.search(r'\s*\[rel\s+(\w+\.\w+)\s*\]\s*', rel)
        return match.group(1)

    def resources(self):
        return self.rels


class SurveyCheck:
    def __init__(self, opts):
        self.survey_path = os.path.join(os.path.abspath(opts.survey), 'survey.xml')
        self.path = self.set_path(self.survey_path)
        self.static = os.path.join(self.path, 'static')
        self.survey = Survey(self.survey_path)

        self.opts = opts

    def set_path(self, path):
        if os.path.isfile(path):
            return os.path.dirname(path)

        exit('{} does not exist'.format(path))

    def run(self):
        resources = self.survey.resources()

        for res in resources:
            f = os.path.join(self.static, res)
            if not os.path.isfile(f):
                print '{} is not in your static directory!'.format(res)


def options():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('survey', help='Survey to parse', type=str)

    return parser.parse_args()


if '__main__' == __name__:
    opts = options()
    survey_check = SurveyCheck(opts)
    exit(survey_check.run())
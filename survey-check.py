from sys import exit
import os
import argparse

from survey import Survey


class SurveyCheck:
    def __init__(self, opts):
        self.survey_path = os.path.join(opts.survey, 'survey.xml')
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
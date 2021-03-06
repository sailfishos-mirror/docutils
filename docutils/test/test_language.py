#!/usr/bin/env python3

# $Id$
# Authors: Engelbert Gruber <grubert@users.sourceforge.net>;
#          David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for language module completeness.

Specify a language code (e.g. "de") as a command-line parameter to test only
that language.
"""

import sys
import os
import re

import DocutilsTestSupport              # must be imported before docutils
import docutils.languages
import docutils.parsers.rst.languages
from docutils.parsers.rst import directives, roles
import docutils.utils
import docutils.frontend

_settings = docutils.frontend.get_default_settings()
_reporter = docutils.utils.new_reporter('', _settings)

reference_language = 'en'


class LanguageTestSuite(DocutilsTestSupport.CustomTestSuite):

    language_module_pattern = re.compile(r'^([a-z]{2,3}(_[a-z]{2,8})*)\.py$')

    def __init__(self, languages=None):
        super().__init__()
        if languages:
            self.languages = languages
        else:
            self.get_languages()

    def get_languages(self):
        """
        Get installed language translations from docutils.languages and from
        docutils.parsers.rst.languages.
        """
        languages = {}
        for mod in (os.listdir(docutils.languages.__path__[0])
                    + os.listdir(docutils.parsers.rst.languages.__path__[0])):
            match = self.language_module_pattern.match(mod)
            if match:
                languages[match.group(1)] = 1
        self.languages = list(languages.keys())
        # test language tag normalization:
        self.languages += ['en_gb', 'en_US', 'en-CA', 'de-DE', 'de-AT-1901',
                           'pt-BR', 'pt-foo-BR']
        # test that locally created language files are also loaded.
        # requires local_dummy_lang.py in test directory (testroot)
        # The local_dummy_lang.py contains all the fields from both
        # the docutils language tags and the parser.rst language tags
        self.languages += ['local_dummy_lang']

    def generateTests(self):
        for language in self.languages:
            for method in LanguageTestCase.test_methods:
                self.addTestCase(LanguageTestCase, method, None, None,
                                 id=language+'.py', language=language)


class LanguageTestCase(DocutilsTestSupport.CustomTestCase):

    test_methods = ['test_labels', 'test_bibliographic_fields',
                    'test_directives', 'test_roles']
    """Names of methods used to test each language."""

    def __init__(self, *args, language=None, **kwargs):
        """
        Set self.ref (from module variable) and self.language.

        Requires keyword argument `language`.
        Pass remaining arguments to parent __init__.

        Note: the modified signature is incompatible with
        the "pytest" and "nose" frameworks.
        """  # cf. feature-request #81

        self.ref = docutils.languages.get_language(reference_language,
                                                   _reporter)
        assert language is not None, 'required argument'
        self.language = language
        super().__init__(*args, **kwargs)

    def _xor(self, ref_dict, l_dict):
        """
        Returns entries that are only in one dictionary.
        (missing_in_lang, more_than_in_ref).
        """
        missing = []    # in ref but not in l.
        too_much = []   # in l but not in ref.
        for label in ref_dict.keys():
            if label not in l_dict:
                missing.append(label)
        for label in l_dict.keys():
            if label not in ref_dict:
                too_much.append(label)
        return missing, too_much

    def _invert(self, adict):
        """Return an inverted (keys & values swapped) dictionary."""
        inverted = {}
        for key, value in adict.items():
            inverted[value] = key
        return inverted

    def test_labels(self):
        try:
            module = docutils.languages.get_language(self.language, _reporter)
            if not module:
                raise ImportError
        except ImportError:
            self.fail('No docutils.languages.%s module.' % self.language)
        missed, unknown = self._xor(self.ref.labels, module.labels)
        if missed or unknown:
            self.fail('Module docutils.languages.%s.labels:\n'
                      '    Missed: %s; Unknown: %s'
                      % (self.language, str(missed), str(unknown)))

    def test_bibliographic_fields(self):
        try:
            module = docutils.languages.get_language(self.language, _reporter)
            if not module:
                raise ImportError
        except ImportError:
            self.fail('No docutils.languages.%s module.' % self.language)
        missed, unknown = self._xor(
            self._invert(self.ref.bibliographic_fields),
            self._invert(module.bibliographic_fields))
        if missed or unknown:
            self.fail('Module docutils.languages.%s.bibliographic_fields:\n'
                      '    Missed: %s; Unknown: %s'
                      % (self.language, str(missed), str(unknown)))

    def test_directives(self):
        try:
            module = docutils.parsers.rst.languages.get_language(
                self.language)
            if not module:
                raise ImportError
        except ImportError:
            self.fail('No docutils.parsers.rst.languages.%s module.'
                      % self.language)
        failures = []
        for d in module.directives.keys():
            try:
                func, msg = directives.directive(d, module, None)
                if not func:
                    failures.append('"%s": unknown directive' % d)
            except Exception as error:
                failures.append('"%s": %s' % (d, error))
        inverted = self._invert(module.directives)
        canonical = sorted(directives._directive_registry.keys())
        canonical.remove('restructuredtext-test-directive')
        for name in canonical:
            if name not in inverted:
                failures.append('"%s": translation missing' % name)
        if failures:
            text = ('Module docutils.parsers.rst.languages.%s:\n    %s'
                    % (self.language, '\n    '.join(failures)))
            if isinstance(text, str):
                text = text.encode('raw_unicode_escape')
            self.fail(text)

    def test_roles(self):
        module = docutils.parsers.rst.languages.get_language(self.language)
        if not module:
            self.fail('No docutils.parsers.rst.languages.%s module.'
                      % self.language)
        if not hasattr(module, "roles"):
            self.fail('No "roles" mapping in docutils.parsers.rst.languages.'
                      '%s module.' % self.language)
        failures = []
        for d in module.roles.values():
            try:
                roles._role_registry[d]
            except KeyError as error:
                failures.append('"%s": %s' % (d, error))
        inverted = self._invert(module.roles)
        canonical = sorted(roles._role_registry.keys())
        canonical.remove('restructuredtext-unimplemented-role')
        for name in canonical:
            if name not in inverted:
                failures.append('"%s": translation missing' % name)
        if failures:
            text = ('Module docutils.parsers.rst.languages.%s:\n    %s'
                    % (self.language, '\n    '.join(failures)))
            if isinstance(text, str):
                text = text.encode('raw_unicode_escape')
            self.fail(text)


languages_to_test = []


def suite():
    s = LanguageTestSuite(languages_to_test)
    s.generateTests()
    return s


def get_language_arguments():
    while len(sys.argv) > 1:
        last = sys.argv[-1]
        if last.startswith('-'):
            break
        languages_to_test.append(last)
        sys.argv.pop()
    languages_to_test.reverse()


if __name__ == '__main__':
    get_language_arguments()
    import unittest
    unittest.main(defaultTest='suite')

# vim: set et ts=4 ai :

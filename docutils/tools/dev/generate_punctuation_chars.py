#!/usr/bin/env python3
# :Copyright: © 2011, 2017, 2022 Günter Milde.
# :License: Released under the terms of the `2-Clause BSD license`_, in short:
#
#    Copying and distribution of this file, with or without modification,
#    are permitted in any medium without royalty provided the copyright
#    notice and this notice are preserved.
#    This file is offered as-is, without any warranty.
#
# .. _2-Clause BSD license: https://opensource.org/licenses/BSD-2-Clause

# :Id: $Id$
#
# ::

"""(Re)generate the utils.punctuation_chars module.

The category of some characters can change with the development of the
Unicode standard. This tool checks the patterns in `utils.punctuation_chars`
against a re-calculation based on the "unicodedata" stdlib module
which may give different results for different Python versions.

.. admonition:: API change

   Updating the module with changed `unicode_punctuation_categories`
   (due to a new Python or Unicode standard version is an API change
   (may render valid rST documents invalid). It should only be done for
   "feature releases" and requires also updating the specification of
   `inline markup recognition rules`_.

   .. _inline markup recognition rules:
      https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html
      #inline-markup-recognition-rules
"""

import sys
import unicodedata


# Template for utils.punctuation_chars
# ------------------------------------

module_template = r'''# :Id: $Id$
# :Copyright: © 2011, 2017, 2022 Günter Milde.
# :License: Released under the terms of the `2-Clause BSD license`_, in short:
#
#    Copying and distribution of this file, with or without modification,
#    are permitted in any medium without royalty provided the copyright
#    notice and this notice are preserved.
#    This file is offered as-is, without any warranty.
#
# .. _2-Clause BSD license: https://opensource.org/licenses/BSD-2-Clause
#
# This file is generated by
# ``docutils/tools/dev/generate_punctuation_chars.py``.
# ::

"""Docutils character category patterns.

   Patterns for the implementation of the `inline markup recognition rules`_
   in the reStructuredText parser `docutils.parsers.rst.states.py` based
   on Unicode character categories.
   The patterns are used inside ``[ ]`` in regular expressions.

   Rule (5) requires determination of matching open/close pairs. However, the
   pairing of open/close quotes is ambiguous due to  different typographic
   conventions in different languages. The ``quote_pairs`` function tests
   whether two characters form an open/close pair.

   The patterns are generated by
   ``docutils/tools/dev/generate_punctuation_chars.py`` to  prevent dependence
   on the Python version and avoid the time-consuming generation with every
   Docutils run. See there for motives and implementation details.

   The category of some characters changed with the development of the
   Unicode standard. The current lists are generated with the help of the
   "unicodedata" module of Python %(python_version)s (based on Unicode version %(unidata_version)s).

   .. _inline markup recognition rules:
      https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html
      #inline-markup-recognition-rules
"""

%(openers)s
%(closers)s
%(delimiters)s
closing_delimiters = r'\\.,;!?'


# Matching open/close quotes
# --------------------------

# Matching open/close pairs are at the same position in
# `punctuation_chars.openers` and `punctuation_chars.closers`.
# Additional matches (due to different typographic conventions
# in different languages) are stored in `quote_pairs`.

quote_pairs = {
    # open char: matching closing characters  # use case
    '\xbb': '\xbb',            # » » Swedish
    '\u2018': '\u201a',        # ‘ ‚ Albanian/Greek/Turkish
    '\u2019': '\u2019',        # ’ ’ Swedish
    '\u201a': '\u2018\u2019',  # ‚ ‘ German, ‚ ’ Polish
    '\u201c': '\u201e',        # “ „ Albanian/Greek/Turkish
    '\u201e': '\u201c\u201d',  # „ “ German, „ ” Polish
    '\u201d': '\u201d',        # ” ” Swedish
    '\u203a': '\u203a',        # › › Swedish
    '\u301d': '\u301f'         # 〝 〟 CJK punctuation
    '\u2e42': '\u201F',        # ⹂ ‟ Old Hungarian (right to left)
    }
"""Additional open/close quote pairs."""


def match_chars(c1, c2):
    """Test whether `c1` and `c2` are a matching open/close character pair."""
    try:
        i = openers.index(c1)
    except ValueError:  # c1 not in openers
        return False
    return c2 == closers[i] or c2 in quote_pairs.get(c1, '')
'''


# Generation of the  character category patterns
# ----------------------------------------------
#
# Unicode punctuation character categories
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# For details about Unicode categories, see
# https://www.unicode.org/Public/5.1.0/ucd/UCD.html#General_Category_Values
# ::

unicode_punctuation_categories = {
    'Pd': 'dash',
    'Ps': 'open',
    'Pe': 'close',
    'Pi': 'initial quote',  # may behave like Ps or Pe depending on language
    'Pf': 'final quote',    # may behave like Ps or Pe depending on language
    'Po': 'other'
    }
"""Unicode character categories for punctuation"""


# generate character pattern strings
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# ::

def unicode_charlists(categories, cp_min=0, cp_max=sys.maxunicode):
    """Return dictionary of Unicode character lists.

    For each of the `catagories`, an item contains a list with all Unicode
    characters with `cp_min` <= code-point <= `cp_max` that belong to
    the category.
    """
    char_lists = {cat: [] for cat in categories}
    for i in range(cp_min, cp_max+1):
        chr_i = chr(i)
        cat_i = unicodedata.category(chr_i)
        if cat_i in char_lists:
            char_lists[cat_i].append(chr_i)
    return char_lists


# Character categories in Docutils
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# ::

def character_category_patterns():

    """Docutils character category patterns.

    Return list of pattern strings for the categories "Open", "Close",
    "Delimiters" and "Closing-Delimiters" used in the `inline markup
    recognition rules`_.
    """

    cp_min = 160  # ASCII chars have special rules for backwards compatibility
    ucharlists = unicode_charlists(unicode_punctuation_categories, cp_min)
    """Strings of characters in Unicode punctuation character categories"""

    # match opening/closing characters
    # --------------------------------
    # Rearange the lists to ensure matching characters at the same
    # index position.

    # LOW-9 QUOTATION MARKs are categorized as Ps (open) without matching Pe.
    # They are used as initial quotes in German and final quotes in Greek.
    # Remove them to get balanced Ps/Pe pairs.
    ucharlists['Ps'].remove('‚')  # 201A  SINGLE LOW-9 QUOTATION MARK
    ucharlists['Ps'].remove('„')  # 201E  DOUBLE LOW-9 QUOTATION MARK
    #
    # HIGH-REVERSED-9 QUOTATION MARKs are categorized as Pi (initial quote)
    # without matching Pf (final quote).
    # Insert the LOW-9 QUOTATION MARKs at the "empty slots" in Pf.
    ucharlists['Pf'].insert(ucharlists['Pi'].index('‛'), '‚')
    ucharlists['Pf'].insert(ucharlists['Pi'].index('‟'), '„')

    # '⹂' 2E42 DOUBLE LOW-REVERSED-9 QUOTATION MARK
    # is categorized as Ps (open) without matching Pe (close).
    # It is used in Old Hungarian (written right to left) as quoting character
    # matching DOUBLE HIGH-REVERSED-9 QUOTATION MARK.
    # https://www.unicode.org/L2/L2012/12168r-n4268r-oldhungarian.pdf#page=26
    #
    # '⹂' 301F LOW DOUBLE PRIME QUOTATION MARK
    # is categorized as Pe (close) without matching Ps (open).
    # Move to the place matching  2E42:
    ucharlists['Pe'].remove('\u301f')
    ucharlists['Pe'].insert(ucharlists['Ps'].index('⹂'), '\u301f')

    # check for balanced lists:
    if len(ucharlists['Ps']) != len(ucharlists['Pe']):
        print('Missmatch between "Open" and "Close" categories')
        print(''.join(ucharlists['Ps']))
        print(''.join(ucharlists['Pe']))
        raise AssertionError
    if len(ucharlists['Pi']) != len(ucharlists['Pf']):
        print('Missmatch between "initial quote" and "final quote" categories')
        print(''.join(ucharlists['Pi']))
        print(''.join(ucharlists['Pf']))
        raise AssertionError

    # The Docutils character categories
    # ---------------------------------
    #
    # The categorization of ASCII chars is non-standard to reduce
    # both false positives and need for escaping. (see `inline markup
    # recognition rules`_)

    # allowed before markup if there is a matching closer
    openers = ['"\'(<\\[{']
    for category in ('Ps', 'Pi', 'Pf'):
        openers.extend(ucharlists[category])

    # allowed after markup if there is a matching opener
    closers = ['"\')>\\]}']
    for category in ('Pe', 'Pf', 'Pi'):
        closers.extend(ucharlists[category])

    # non-matching, allowed on both sides
    delimiters = [r'\-/:']
    for category in ('Pd', 'Po'):
        delimiters.extend(ucharlists[category])

    # non-matching, after markup
    closing_delimiters = [r'\\.,;!?']

    return [''.join(chars) for chars in (openers, closers, delimiters,
                                         closing_delimiters)]


def mark_intervals(s):
    """Return s with shortcut notation for runs of consecutive characters

    Sort string and replace 'cdef' by 'c-f' and similar.
    """
    lst = []
    s = sorted(ord(ch) for ch in s)
    for n in s:
        try:
            if lst[-1][-1] + 1 == n:
                lst[-1].append(n)
            else:
                lst.append([n])
        except IndexError:
            lst.append([n])

    lst2 = []
    for i in lst:
        i = [chr(n) for n in i]
        if len(i) > 2:
            i = i[0], '-', i[-1]
        lst2.extend(i)

    return ''.join(lst2)


def wrap_string(s, startstring="(", endstring="    )", wrap=71):
    """Line-wrap a unicode string literal definition."""
    s = s.encode('unicode-escape').decode()
    c = len(startstring)
    left_indent = ' '*(c - len(startstring.lstrip(' ')))
    line_start_string = f"\n    {left_indent}'"
    cont_string = f"'{line_start_string}"
    lst = [startstring, line_start_string]
    for ch in s.replace("'", r"\'"):
        c += 1
        if ch == '\\' and c > wrap:
            c = len(startstring)
            lst.append(cont_string)
        lst.append(ch)
    lst.append(f"'\n{left_indent}{endstring}")
    return ''.join(lst)


def print_differences(old, new, name):
    """List characters missing in old/new."""
    if old != new:
        print(f'"{name}" changed')
        if '-' in old or '-' in new:
            print('-', old)
            print('+', new)
        else:
            for c in new:
                if c not in old:
                    print('+ %04x'%ord(c), c, unicodedata.name(c))
            for c in old:
                if c not in new:
                    print('- %04x'%ord(c), c, unicodedata.name(c))
        return True
    else:
        print(f'"{name}" unchanged')
        return False


# Output
# ------
#
# ::

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-t', '--test', action="store_true",
                        help='test for changed character categories')
    parser.add_argument('--pairs', action="store_true",
                        help='show openers/closers in human readable form')
    args = parser.parse_args()

# (Re)create character patterns
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# ::

    (o, c, d, cd) = character_category_patterns()

# delimiters: sort and use shortcut for intervals (saves ~150 characters)
# (`openers` and `closers` must be verbose and keep order
# because they are also used in `match_chars()`)::

    d = d[:5] + mark_intervals(d[5:])


# Test: compare module content with re-generated definitions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Import the punctuation_chars module from the source
# or Py3k build path for local Python modules::

    if args.test:

        sys.path.insert(0, '../../docutils')

        from docutils.utils.punctuation_chars import (
                 openers, closers, delimiters, closing_delimiters)

        print('Check for differences between the current `punctuation_chars`'
              ' module\n and a regeneration based on Unicode version %s:'
              % unicodedata.unidata_version)

        delta_o = print_differences(openers, o, 'openers')
        delta_c = print_differences(closers, c, 'closers')
        print_differences(delimiters, d, 'delimiters')
        print_differences(closing_delimiters, cd, 'closing_delimiters')

        if delta_o or delta_c:
            print('\nChanges in "openers" and/or "closers",'
                  '\nCheck open/close pairs with option "--pairs"!')
        sys.exit()


# Print debugging output
# ~~~~~~~~~~~~~~~~~~~~~~
#
# Print comparison of `openers` and `closers` in human readable form
# to allow checking for matching pairs.

    if args.pairs:
        for o_i, c_i in zip(o, c):
            print(o_i, c_i,
                  unicodedata.name(o_i), '\t', unicodedata.name(c_i))
        sys.exit()

# Print re-generation of the punctuation_chars module
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# The output can be copied to docutils/utils if an update is wanted
# (API change, see Intro).

# Replacements::

    substitutions = {
        'python_version': sys.version.split()[0],
        'unidata_version': unicodedata.unidata_version,
        'openers': wrap_string(o, startstring="openers = ("),
        'closers': wrap_string(c, startstring="closers = ("),
        'delimiters': wrap_string(d, startstring="delimiters = ("),
        }

    print(module_template % substitutions, end='')

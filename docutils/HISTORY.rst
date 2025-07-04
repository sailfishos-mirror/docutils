.. include:: docs/header0.rst

==================
 Docutils History
==================

:Author: David Goodger; open to all Docutils developers
:Contact: docutils-develop@lists.sourceforge.net
:Date: $Date$
:Revision: $Revision$
:Web site: https://docutils.sourceforge.io/
:Copyright: This document has been placed in the public domain.

.. contents::


Release 0.22rc6 (unpublished)
=============================

.

Release 0.22rc5 (2025-06-24)
============================

* docutils/nodes.py

  - Don't invalidate indirect targets with duplicate name, if they refer to
    the same refname (similar to external targets refering to the same URI).

* docutils/parsers/rst/states.py

  - "Downgrade" targets generated from hyperlink references with embedded
    URI or alias from explicit to implicit (cf. bug #502).


Release 0.22rc4 (2025-06-17)
============================

* docutils/nodes.py

  - Don't include a "backlink" reference in system messages, if the
    referenced element is an external target (not visible in the output).

* docutils/parsers/rst/directives/references.py

  - Remove "name" from `TargetNotes.option_spec`.
    The "target-notes" directive generates one footnote element per
    external target but "name" must be unique across the document.
    So far, the name was silently dropped.

* docutils/parsers/rst/languages/en.py

  - Add alias "rst-class" for the "class" directive to improve the
    compatibility with Sphinx.


Release 0.22rc3 (2025-06-10)
============================

* docutils/parsers/rst/states.py

  - Warn about duplicate name in references with embedded internal targets.
    Fixes bug #502.

* docutils/transforms/references.py

  - New transform `CitationReferences`. Marks citation_references
    as resolved if BibTeX is used by the backend (LaTeX).

* docutils/writers/latex2e/__init__.py

  - Replace `Writer.bibtex_reference_resolver()` with a transform.
  - `LaTeXTranslator.visit_inline()` now inserts labels for the
    node's IDs.
  - Disable footnote handling by the "hyperref" LaTeX package (Docutils'
    ``\DUfootnotemark`` and ``\DUfootnotetext`` macros implement
    hyperlinks and backlinks).  Avoids "empty anchor" warnings.
  - Fix target position and re-style system messages.
  - Don't merge paragraphs if there is a target between them.

* docutils/writers/manpage.py

  - Do not drop text of internal targets.


Release 0.22rc2 (2025-05-22)
============================


* docutils/parsers/rst/directives/misc.py

  - Pass default settings to custom parser for included file.

* docutils/parsers/rst/states.py

  - Remove the `states.RSTStateMachine.memo.section_parents` cache
    (introduced in Docutils 0.22rc1) that broke 3rd-party applications
    employing a "mock memo".
  - Use `types.SimpleNamespace` instead of a local definition for
    the auxilliary class `states.Struct`.

* docutils/writers/_html_base.py

  - Fix error when determining the document metadata title from the
    source path and the internal `source` attribute is None.


Release 0.22rc1 (2025-05-06)
============================

* General

  - We have started to add type hints to Docutils (feature-request #87).

    This will be a complex programme of work and as such,
    for the time being, these type hints are "provisional"
    and should not be relied upon.

    By default, the Python interpreter treats type hints as annotations.
    Python >= 3.10 is required with active type hints
    (``typing.TYPE_CHECKING == True``).

* docs/ref/docutils.dtd

  - Allow multiple <term> elements in a <definition_list_item>.
    Fixes feature-request #60
  - The first element in a <figure> may also be a <reference>
    (with nested "clickable" <image>).

* docutils/core.py

  - Removed `Publisher.setup_option_parser()` (internal, obsolete).
  - Allow a string value (component name or alias) in the "reader",
    "parser", and "writer" arguments of `Publisher.__init__()` and
    the `publish_*()` convenience functions.

* docutils/frontend.py

  - Drop short options ``-i`` and ``-o`` for ``--input-encoding``
    and ``--output-encoding``.
  - Change the default input encoding from ``None`` (auto-detect) to "utf-8".
  - Change the default value of the root_prefix_ setting to the empty string
    (no change to the behaviour).

* docutils/io.py

  - Change the default input encoding from ``None`` (auto-detect) to "utf-8".

* docutils/nodes.py

  - Raise TypeError if the "rawsource" argument in `Element.__init__()`
    is an `Element` instance.
    Catches errors like ``nodes.hint(nodes.paragraph())``.
  - New element category classes `SubStructural` and `PureTextElement`.
  - Fix element categories.
  - New method `Element.validate()`: raise `nodes.ValidationError` if
    the element does not comply with the "Docutils Document Model".
    Provisional.
  - New "attribute validating functions"
    convert string representations to correct data type,
    normalize values, and
    raise ValueError for invalid attribute names or values.
  - New function `parse_measure()`.
  - Removed `Element.set_class()`.
  - Downgrade "duplicate ID" message level from SERIOUS to ERROR.
  - Fix recursion in `Element.get_language_code()`.
  - Do not insert <system_message> elements for duplicate explicit targets
    if this results in an invalid doctree (cf. bug #489).

* docutils/parsers/docutils_xml.py

  - New parser for Docutils XML sources. Provisional.

* docutils/parsers/recommonmark_wrapper.py

  - New method `Parser.finish_parse()` to clean up (before validating).

* docutils/parsers/rst/languages/

  - Remove mistranslations of the "admonition" directive name.

* docutils/parsers/rst/directives/__init__.py

  - Support CSS3 `length units`_. Fixes feature-request #57.

* docutils/parsers/rst/directives/images.py

  - New option "figname" for the "figure" directive.
    Fixes feature-request #44.

* docutils/parsers/rst/directives/misc.py

  - Pass the included file's path to the parser when the
    "include" directive is used with :parser: option.
    Enables system messages with correct source/line info.

* docutils/parsers/rst/directives/tables.py

  - Removed `CSVTable.decode_from_csv()` and `CSVTable.encode_from_csv()`.
    Not required with Python 3.

* docutils/parsers/rst/roles.py

  - Renamed `normalized_role_options()` to `normalize_options()`
    (it is now also used for directive options).

* docutils/parsers/rst/states.py

  - Raise warning for empty footnotes and citations.
  - Add source and line info to <enumerated-list> elements.
    Fix line number of "start value not ordinal-1" INFO message.
  - Change section handling to not rely on exceptions and reparsing.
    Based on patch #213 by Arne Skjærholt.
    Fixes bug #346 (duplicate System Messages).

* docutils/readers/__init__.py:

  - Deprecate "parser_name" argument of `Reader.__init__()`.

* docutils/transforms/frontmatter.py

  - Update `DocInfo` to work with corrected element categories.

* docutils/transforms/misc.py:

  - Fix for `misc.Transitions`: report an error if a <transition> element
    follows a <meta> or <decoration> element as this is invalid
    according to ``docutils.dtd``.

* docutils/transforms/writer_aux.py

  - Removed `Compound` transform.

* docutils/transforms/references.py

  - Make `AnonymousHyperlinks` transform idempotent.

* docutils/transforms/universal.py

  - `Messages` transform now also handles "loose" system messages
    generated by the parser.

* docutils/utils/__init__.py

  - Removed `Reporter.set_conditions()`.
    Set attributes via configuration settings or directly.

* docutils/utils/_roman_numerals.py

  - New implementation or Roman numeral support.
    Replaces the local copy of the roman.py package.

* docutils/utils/error_reporting.py

  - Removed. Obsolete in Python 3.

* docutils/writers/docutils-xml.py

  - Do not increase indentation of follow-up lines inside inline elements.
    when formatting with `indents`_.

* docutils/writers/__init__.py

  - New base class `writers.DoctreeTranslator`
    with auxiliary method `uri2path()`.

* docutils/writers/_html_base.py

  - Make MathML the default math_output_.
  - Revise image size handling methods,
    use "width" and "height" attributes for unitless values.
  - Add "px" to unitless table "width" values.

* docutils/writers/html4css1/__init__.py

  - Keep default math_output_ value "HTML math.css".
  - Add "px" to unitless table "width" values.

* docutils/writers/latex2e/__init__.py

  - `LaTeXTranslator.to_latex_length()`:
    Handle CSS3 `length units`_.
    Remove optional argument `pxunit` (ignored since at least 2012).
    Drop trailing zeroes from length values.
    Move XeTeX-specific code to the "xetex" writer.
  - Don't wrap references with custom reference-label_ in
    a ``\hyperref`` command.
  - Mark the main language when loading "babel".
  - Provide an "unknown_references_resolver" (cf. `docutils/TransformSpec`)
    for citation references resolved with BibTeX (cf. `use_bibtex`_ setting).
  - Support SVG image inclusion with the "svg" LaTeX package (see the
    `stylesheet`__ configuration setting). Solves feature-request #83
  - Add "template" to the parts returned by `Writer.assemble_parts()`.
  - Use standard `dict` for `LaTeXTranslator.requirements`
    and `LaTeXTranslator.fallbacks`.
  - Use <document> "title" attribute in pdfinfo.
  - Encode <meta> element content in pdfinfo.
  - Improve formatting of docinfo fields.
  - `LaTeXTranslator.pop_output_collector()` now returns the popped list.

  .. _reference-label: docs/user/config.html#reference-label
  __ docs/user/config.html#stylesheet-latex-writers

* docutils/writers/latex2e/docutils.sty

  - Replace use of ``\ifthenelse{\isundefined...`` (from "ifthen.sty")
    with the eTeX primitive ``\ifdefined``.
  - Add macros to emulate CSS3 `length units`_ unknown to LaTeX.

* docutils/writers/manpage.py

  - Remove code for unused emdash bullets.
  - Print Docutils version in header comment (feature-request #105).
  - Stop converting text to full capitals (bug #481).
  - Fix reference output (bug #497).
  - Use macros .UR/.UE for hyperlink references unless the new
    configuration setting text_references_ is True.
    The current default is True (text references), it will change
    to False (macro references) in Docutils 1.0.

* docutils/writers/null.py

  - `null.Writer.translate()` sets `self.output` to the empty string.

* docutils/writers/odf_odt/__init__.py

  - Use "px" as fallback unit for unitless image size attributes.
  - Fix conversion factor of "pc" (pica) to "cm".
  - Fix conversion of image width in "%" if the height is specified.
  - Adjust fallback DPI value (currently not used) to match CSS units.
  - Fix errors with ``*.xml`` style files (bug #494).
  - Use <document> "title" attribute in document metadata.

* pyproject.toml

  - Add tox.ini to the "include" list (fixes bug #486).

* tools/rst2odt.py

  - Use `core.publish_file()` instead of `core.publish_file_to_binary()`.

* tools/rst2odt_prepstyles.py

  - Removed. Use ``python -m docutils.writers.odf_odt.prepstyles``.

.. _length units: docs/ref/rst/restructuredtext.html#length-units


Release 0.21.2 (2024-04-23)
===========================

* Declare support for languages Georgian and Catalan (Valencian).

* docs/ref/docutils.dtd

  - Remove declaration of element <info>.
  - Remove <decoration> from content declaration of <section> elements.

* Fix test failures.


Release 0.21.1 (2024-04-10)
===========================

* Add missing files in Docutils 0.21 source distribution (sdist).

Release 0.21 (2024-04-09)
=========================

* General

  - Drop support for Python 3.7 and 3.8.
  - Updated build system to use Flit_ (patch #186 by Adam Turner).
    Removed ``setup.py``.
  - Provide ``rst2*`` "console_scripts" `entry points`_
    (without the ``.py`` extension) instead of installing the
    ``rst2*.py`` front end tools in the binary PATH.

  .. _Flit: https://github.com/pypa/flit/

* docs/ref/docutils.dtd

  - The <image> element accepts a new attribute "loading".

  - Fix definitions (no change to actual behaviour):

    * The <math_block> element uses the attribute "xml:space".
    * The <raw> element may contain text only (no inline elements).
    * The <topic> element uses the "depth" and "local" attributes to
      store "contents" directive options when used as placeholder for a
      generated table of contents (LaTeX writers with `use_latex_toc`_
      setting).

  - Documentation fix:
    Reference names (``%refname.type`` and ``%refnames.type``)
    are whitespace-normalized but **not** always downcased.

* docutils/frontend.py

  - Allow `validate_*()` functions to be called with just the "value"
    argument but keep the legacy interface for use with optparse.
  - New function `frontend.validate_math_output()`.

* docutils/io.py

  - Simpler and more secure `input encoding`_ default behaviour:

    Do not use the locale encoding as fallback if Python is started in
    `UTF-8 mode`_. Stop using "latin1" as second fallback.

    Remove BOM (U+FEFF ZWNBSP at start of data) only if the "input_encoding"
    configuration setting is None, '', 'utf-8-sig', 'utf-16', or 'utf-32'.
    Do not remove other ZWNBSPs.

    .. _UTF-8 mode: https://docs.python.org/3/library/os.html#utf8-mode
    .. _input encoding: docs/api/publisher.html#encodings

  - Auto-close `FileInput.source` in case of reading/decoding errors.

* docutils/languages/, docutils/parsers/rst/languages/

  - Mark/Fix mistranslated localizations of the "admonition" directive
    name. In Docutils, "admonition" is used as a generic term for
    "advice"/"advisory"/"remark", not a reprimand.
  - Add support for Georgian language (patch #204 by Temuri Doghonadze).
  - Update/complete Catalan translations (patch #203 by Antoni Bella Pérez).

* docutils/nodes.py

  - Remove compatibility hacks `nodes.reprunicode` and `nodes.ensure_str()`.

* docutils/parsers/rst/directives/images.py

  - New "image" directive option "loading".

* docutils/parsers/rst/directives/tables.py

  - Use the same CSV format for the ``:header:`` option and the main data
    of the "csv-table" directive.

  - Move `parsers.rst.directives.Table.process_header_option()` method
    to `parsers.rst.directives.CSVTable`.

* docutils/parsers/rst/states.py

  - Don't split inside "< >" when parsing "option groups" (fixes bug #474).

* docutils/parsers/rst/directives/misc.py,
  docutils/parsers/rst/directives/tables.py

  - Consider the new root_prefix_ setting when including files with
    "include", "raw", or "csv-table" directives.

* docutils/utils/math/*

  - Use custom exception `utils.math.MathError` instead of
    abusing `SyntaxError` for LaTeX math syntax errors.
  - Unify interface of LaTeX -> MathML conversion functions.
    Improve error reporting.
  - Sort ℏ (`\hslash`) as "mathord", not "mathalpha".

* docutils/utils/math/latex2mathml.py

  - Generate "MathML Core" to fix rendering with Chromium/Android.

    Use CSS rules instead of the deprecated "columnalign" attribute
    to style <mtable> as "align" environment.

    Use Mathematical Alphanumeric Symbols instead of <mstyle> with
    "mathvariant" attribute.

  - Use <mi> instead of <mo> for character class "mathord".

  - Support "aligned" environment.

  - Eliminate side-effect on later import of "tex2unichar".

* docutils/utils/math/mathml_elements.py

  - New module defining MathML element classes
    (outsourced from latex2mathml.py).
  - Base MathML element classes on `xml.etree.ElementTree`.

* docutils/utils/roman.py

  - Update to version `1.4 <https://pypi.org/project/roman/4.1/>`__.
    Fixes feature-request #95 (license is now ZPL 2.1).

* docutils/utils/smartquotes.py

  - Pre-compile regexps once, not with every call of `educateQuotes()`
    (patch #206 by Chris Sewell).
  - Simplify regexps; skip replacement rules if there is nothing to replace.

* docutils/writers/html4css1/__init__.py

  - Support video inclusion via ``<object>`` tags.

* docutils/writers/html5_polyglot/\*.css

  - Move MathML styles to "minimal.css" (required for correct rendering).
  - Highlight heading of target section also with explicit hyperlink target.
  - No additional margins for line-blocks.

* docutils/writers/_html_base.py

  - Stop setting the "footnote-reference" class value for footnote references.
    Since 0.18, you can use the CSS selector ``[role="doc-noteref"]``.
  - Support reading/embedding images also with "file:" URI.
  - Warn, if image scaling fails because the image file cannot be read.
  - Support video inclusion via ``<video>`` tags
    (moved here from writers/html5_polyglot/__init__.py).
  - New auxiliary method `HTMLTranslator.uri2imagepath()` ensures the
    image file can also be read when CWD and output directory differ.
  - Consider the root_prefix_ setting when converting an image URI
    to a local filesystem path.
  - New `\<image>`_ attribute "loading" overrides image_loading_ setting.
  - Embed SVG images as ``<svg>`` instead of data-URI.
    Fixes feature-request #100.
  - Generate system messages for errors/warnings during the writing stage
    (image transformations, math content conversion, ...).
  - Close ``<dt>`` element in `depart_term()` to allow a
    "definition_list_item" with multiple "terms" (cf. feature-request #60).
  - Link to the document "#top" from the ToC heading
    (unless toc_backlinks_ is False).
  - Transfer `id` attribute from <field> elements to the respective
    <field_name> child element to allow cross-references to field-list items
    (<field>s are skipped in HTML output).

* docutils/writers/latex2e/__init__.py

  - Fix placement of hyperlink target (label) for tables (bug #440).
  - More compact LaTeX source for option-lists and description-lists
    (no change in output).

* docutils/writers/manpage.py

  - Put manual section in .TH in quotes.
  - Skip footer to avoid the link to document source in the manpage.
  - Add multiple definition list term support, see feature #60.
  - Render reference, refid and refuri.
    Use of ``.UR`` and ``.UE`` macros for reference markup is too brittle.
  - Add preprocessor hinting tbl first line, see bug #477.
  - Change tbl-Tables using box option, see bug #475.
  - Apply literal block patch #205. Use ``.EE`` and ``.EX`` macros.
    Thanks to G. Branden Robinson.

* docutils/writers/odf_odt/__init__.py

  - Use context manager for image reading operations.
    Catch `URLError` when `urllib.request.urlopen()` fails.

  - Convert image URI to path if accessing a local file. Fixes bug #153.

* docutils/writers/s5_html/__init__.py

  - Warn if the S5 writer cannot copy the theme files.
  - Programmatic customization of theme_url_ setting no longer
    overridden by the default for theme_.

* tools/buildhtml.py

  - New configuration setting `sources`_.
  - Match `prune`_ values with `fnmatch.fnmatch()`.


Release 0.20.1 (2023-05-17)
===========================

* docutils/MANIFEST.in

  - Include tox.ini and docutils.conf in the source package
    (cf. bug #467 and bug #461).

* tools/rst2odt_prepstyles.py

  - Moved to ``docutils/writers/odf_odt/prepstyles.py``.
    Replaced with a provisional backwards compatibility script.


Release 0.20 (2023-05-09)
=========================

* General

  - Docutils 0.20 is the last version supporting Python 3.7 and 3.8.
  - Support Python 3.11 (patch #198 by Hugo van Kemenade).

* docutils/core.py

  - New functions `rst2…()` for use as "console_scripts" `entry points`_.
    (cf. `Future changes` in the RELEASE-NOTES_).

* docutils/frontend.py

  - New configuration setting "output_". Obsoletes the ``<destination>``
    positional argument (cf. `Future changes` in the RELEASE-NOTES_).

* docutils/languages/
  docutils/parsers/rst/languages/

  - Support Ukrainian. Patch by Dmytro Kazanzhy.

* docutils/nodes.py

  - Fix `previous_sibling()` method that led to invalid HTML in some cases
    (cf. patch #195).
  - Fix bug #463. Spurious comma in deprecation warning.

* docutils/parsers/recommonmark_wrapper.py

  - Improved mock Sphinx module.

* docutils/transforms/__init__.py

  - `Transformer.populate_from_components()` now silently ignores
    components that are not instances of `docutils.TransformSpec`.

* docutils/transforms/frontmatter.py

  - Accept author names with initials like ``A. Einstein`` in the "author"
    `bibliographic field`_ instead of rising an error
    (generally, such names are `parsed as enumerated list`__).

    .. _bibliographic field:
        docs/ref/rst/restructuredtext.html#bibliographic-fields
    __ docs/ref/rst/restructuredtext.html#enumerated-lists

* docutils/transforms/references.py

  - `DanglingReferences` ignores `citation_reference` nodes if the
    "use_bibex" setting is active. (In this case, citations are provided
    by LaTeX/BibTeX.) Fixes bug #384.

* docutils/utils/__init__.py

  - New utility function `xml_declaration()`.
  - `DependencyList.add()` accepts `pathlib.Path` instances.
  - `find_file_in_dirs()` now returns a POSIX path also on Windows;
    `get_stylesheet_list()` no longer converts ``\`` to ``/``.

* docutils/utils/math/latex2mathml.py

  - Support "mod" notation for modulo operation / modulus arithmetic.

* docutils/utils/math/tex2mathml_extern.py

  - Support `Pandoc` as alternative LaTeX to MathML converter.
    Patch by Ximin Luo.

* docutils/writers/_html_base.py

  - Refactoring of `HTMLTranslator` initialization and collecting of
    document "parts". Adapt HTML writers importing `_html_base`.

    Changes to the HTML output (no space character before closing tag of
    XML declaration, order of metadata elements)
    don't affect the HTML semantics, styling, and rendering.

  - Wrap definition lists with "details" class argument in a <div>
    with the "id" and "class" values of the list node.

  - Use dpub-ARIA role "doc-footnote__" (instead of ARIA role "note")
    for footnotes.

    __ https://www.w3.org/TR/dpub-aria-1.1/#doc-footnote

* docutils/writers/html5_polyglot/__init__.py

  - Do not convert class values to HTML5 text-level tags inside
    <code> and <code-block> (fixes bug #476).

* docutils/writers/latex2e/__init__.py

  - Do not load the `inputenc` package in UTF-8 encoded LaTeX sources.
    (UTF-8 is the default encoding for LaTeX2e since 2018).
  - Fix behaviour of the use_bibtex_ setting.
  - Outsource parts of `depart_document()` to new auxiliary methods
    `make_title()` and `append_bibliography()`.
  - Ensure POSIX paths in stylesheet loading macros.

* docutils/writers/latex2e/titlepage.tex

  - Drop ``\usepackage{fixltx2e}`` from template.
    (Obsolete since 2015 and dropped from other templates in Docutils 0.14.)

* docutils/writers/manpage.py

  - Do not output empty "manual" in ``.TH``.

* docutils/writers/xetex/__init__.py

  - Ignore settings in the [latex2e writer] configuration file section.
    Place common settings in section [latex writers].

* setup.py

  - Fix SetuptoolsDeprecationWarning: ``Installing '' as data is deprecated``
    by adding data directories to package_data.packages list.

* tox.ini

  - Extracted flake8 configuration and moved to ``.flake8``.
  - changedir to directory ``test`` to avoid path problems.

* test/

  - Refactored tests to use common `unittest` idioms.
    Fixes errors when running the test suite with ``python -m unittest``
    or external test frameworks, such as Pytest_.

  .. _pytest: https://pypi.org/project/pytest/

* test/coverage.sh

  - Removed. Use the coverage.py_ project instead,
    ``coverage run test/alltests.py`` and ``coverage report``.

  .. _coverage.py: https://pypi.org/project/coverage/

* tools/

  - Moved ``quicktest.py`` to ``tools/dev/``.


Release 0.19 (2022-07-05)
=========================

* General

  - Dropped support for Python 2.7, 3.5, and 3.6. and removed compatibility
    hacks from code and tests.
  - Code cleanup,
    check PEP 8 conformity with `flake8` (exceptions in file tox.ini).

* docutils/__main__.py

  - New module. Support for ``python -m docutils``.
    Also used for the ``docutils`` console script `entry point`_.

* docutils/core.py

  - Let `Publisher.publish()` print info and prompt when waiting for input
    from a terminal (cf. https://clig.dev/#interactivity).
  - Respect `input_encoding_error_handler`_ setting when opening a source.

* docutils/io.py

  - New function `error_string()`
    obsoletes `utils.error_reporting.ErrorString`.
  - Class `ErrorOutput` moved here from `utils.error_reporting` module.
  - Use "utf-8-sig" instead of Python's default encoding if the
    `input_encoding`_ setting is None.
  - Fix error when reading of UTF-16 encoded source without trailing newline.
  - Suppress deprecation warning (fixes bug #464).

* docutils/parsers/__init__.py

  - Aliases "markdown" and "commonmark" point to "commonmark_wrapper".
  - Alias for the "myst" parser (https://pypi.org/project/myst-docutils).
  - Use absolute module names in `_parser_aliases` instead of two
    import attempts. (Keeps details if the `recommonmark_wrapper` module
    raises an `ImportError`.)
  - Prepend parser name to `ImportError` if importing a parser class fails.

* docutils/parsers/commonmark_wrapper.py

  - New module for parsing CommonMark input. Selects a locally installed
    3rd-party parser (`pycmark`, `myst`, or `recommonmark`).

* docutils/parsers/recommonmark_wrapper.py

  - Raise `ImportError`, if import of the upstream parser module fails.
    If called from an `"include" directive`_,
    the system-message now has source/line info.
  - Adapt to and test with `recommonmark` versions 0.6.0 and 0.7.1.

  .. _"include" directive: docs/ref/rst/directives.html#include

* docutils/parsers/rst/__init__.py

  - Update PEP base URL (fixes bug #445),
    use "https:" scheme in RFC base URL.
  - Add `reporter` to `Directive` class attributes.

* docutils/parsers/rst/directives/__init__.py

  - `parser_name()` keeps details when converting `ImportError`
    to  `ValueError`.

* docutils/parsers/rst/roles.py

  - Don't use mutable default values for function arguments. Fixes bug #430.

* docutils/transforms/universal.py

  - Fix bug #435: invalid references in `problematic` nodes
    with report_level=4.

* docutils/utils/__init__.py

  - `decode_path()` returns `str` instance instead of `nodes.reprunicode`.

* docutils/utils/error_reporting.py

  - Add deprecation warning.

* docutils/writers/_html_base.py

  - Add "html writers" to `config_section_dependencies`. Fixes bug #443.
  - Write table column widths with 3 digits precision. Fixes bug #444.

* docutils/writers/html5_polyglot/__init__.py

  - Add space before "charset" meta tag closing sequence.
  - Remove class value "controls" from an `image` node with video content
    after converting it to a "control" attribute of the <video> tag.
  - Wrap groups of footnotes in an ``<aside>`` for easier styling.

* docutils/writers/pep_html/

  - Use "https:" scheme in "python_home" URL default.
  - Fix links in template.txt.

* setup.py

  - New ``docutils``" console script `entry point`_. Fixes bug #447.

* test/alltests.py

  - Always encode the log file ``alltests.out`` using "utf-8".

* test/DocutilsTestSupport.py

  - `exception_data()` now returns None if no exception was raised.
  - `recommonmark_wrapper` only imported if upstream parser is present.

* test/test_parsers/test_rst/test_directives/test_tables.py

  - Fix bug #436: Null char valid in CSV since Python 3.11.

* tools/docutils-cli.py

  - Allow 3rd-party drop-in components for reader and parser, too.
  - Fix help output.
  - Actual code moved to docutils.__main__.py.

* tools/rst2odt_prepstyles.py

  - Options ``-h`` and ``--help`` print short usage message.

.. _entry point:
.. _entry points:
    https://packaging.python.org/en/latest/specifications/entry-points/


Release 0.18.1 (2021-11-23)
===========================

* docutils/nodes.py

  - `Node.traverse()` returns a list again to restore backwards
    compatibility. Fixes bug #431.

  - New method `Node.findall()`: like `Node.traverse()` but returns an
    iterator. Obsoletes `Node.traverse()`.

* docutils/utils/__init__.py

  - Fix behaviour of `get_stylesheet_list()`: do not look up stylesheets
    given as `stylesheet`_ setting. Cf. bug #434.

* docutils/writers/_html_base.py

  - Fix handling of ``footnote_backlinks == False`` (report Alan G Isaac).

* docutils/writers/html5_polyglot/math.css

  - Fix typo (bug #432).

* docutils/writers/odf_odt/__init__.py

  - Fix spurious output with Windows (bug #350).

* test/test_error_reporting.py

  - Fix a false positive (bug #434).


Release 0.18 (2021-10-26)
=========================

* docutils/frontend.py

  - Mark as provisional (will switch from using `optparse` to `argparse`).
  - Remove hack for the now obsolete "mod_python" Apache module.
  - New function `get_default_settings()` as a replacement for the
    deprecated `OptionParser`\ s `get_default_values()` method.

* docutils/nodes.py

  - Don't change a list while looping over it (in
    `document.set_name_id_map()`). Thanks to Mickey Endito.

* docutils/parsers/recommonmark_wrapper.py

  - Test and update to work with `recommonmark` version 0.6.0.
    Still provisional.

    Unfortunately, recommonmark_ is `no longer maintained`__.

    __ https://github.com/readthedocs/recommonmark/issues/221

* docutils/parsers/rst/directives/misc.py

  - Fix bug #424 Wrong circular inclusion detection.
    Use a "magic" comment instead of line numbers
    to keep a log of recursive inclusions.

* docutils/parsers/rst/states.py

  -  Use a "magic" comment to update the log of recursive inclusions.

* docutils/writers/html5_polyglot/__init__.py

  - New option `image_loading`_. Support "lazy" loading of images.
    Obsoletes `embed_images`_.

* docutils/writers/pseudoxml.py

  - Fix spelling of setting `detailed`_.

* tools/docutils-cli.py

  - Read settings from standard configuration files.

Fix spelling errors in documentation and docstrings.
Thanks to Dimitri Papadopoulos.


Release 0.18b1 (2021-10-05)
===========================

* docs/ref/docutils.dtd

  - New document tree element <meta>.

* docutils/frontend.py

  - The default value for the `auto_id_prefix`_ setting changed to "%":
    auto-generated IDs use the tag name as prefix.

* docutils/nodes.py

  - Make `\<meta>`_ a standard Docutils doctree node. Writers may ignore
    <meta> nodes if they are not supported by the output format.

  - document.make_id(): Do not strip leading number and hyphen characters
    from `name` if the `id_prefix`_ setting is non-empty.

  - `Node.traverse()` returns an iterator instead of a list.

* docutils/parsers/rst/directives/html.py

  - Removed. (Meta directive moved to ``misc.py``.)

* docutils/parsers/rst/directives/misc.py

  - `Meta` directive class (moved from html.py) inserts `meta`
    (instead of `pending`) nodes.

  - Add `class` option to `Raw` directive.

* docutils/parsers/rst/directives/tables.py

  - Unify behaviour of `"widths" option`_: check that the length of an
    integer list equals the number of table columns also for the "table"
    directive.

* docutils/tools/math/math2html.py,
  docutils/tools/math/tex2unicode.py,
  docutils/writers/html5/math.css

  - Fork from elyxer and remove code that is not required
    for math conversion.
  - Scale variable sized operators and big delimiters with CSS
  - Support more commands, fix mapping of commands to Unicode characters
    (cf. `LaTeX syntax for mathematics`_).
  - Fix bug #244 Wrong subscript/superscript order.
  - Don't use <tt> element (deprecated in HTML5).
  - Use STIX fonts if available.

  .. _LaTeX syntax for mathematics: docs/ref/rst/mathematics.html

* docutils/parsers/rst/states.py

  - Fix source location (line number) for attribution elements.
    Patch by Mickey Endito.
  - Add line, source, and rawsource internal attributes for blockquote
    elements. Patch by Mickey Endito.

* docutils/transforms/references.py

  - Skip system_messages when propagating targets. Fixes bug #425.

* docutils/utils/__init__.py

  - Removed `unique_combinations()` (obsoleted by `itertools.combinations()`).

* docutils/utils/latex2mathml.py

  - Major update (fixes and support for additional commands and symbols).
    Fixes bug #407.

* docutils/writers/_html_base.py

  - Write footnote brackets and field term colons to HTML, so that
    they are present also without CSS and when copying text.
    Adapt ``minimal.css``.

  - Use semantic tags <aside> for footnote text, topics, admonitions,
    and system-messages and <nav> for the table of contents. Use <div>
    for citations.

  - Only specify table column widths, if the `"widths" option`_ is set
    and is not "auto" (fixes bug #426).
    The `table_style`_ setting "colwidths-grid" restores the current default.

    .. _"widths" option: docs/ref/rst/directives.html#column-widths

  - Use ARIA roles to enable accessible HTML for abstract, dedication,
    the table of contents, footnote, references, footnotes, citations,
    and backlinks.

  - Use "aria-level" attribute instead of invalid tags <h7>, <h8>, ...
    for headings of deeply nested sections.

  - Do not set classes "compound-first", "compound-middle", or
    "compound-last" to elements nested in a compound.
    Use class value "backrefs" instead of "fn-backref" for a span of
    back-references.

  - Do not write class values handled by the HTML writer ("colwidths-auto",
    "colwidths-given", "colwidths-grid") to the output.

  - Move space character between section number and heading into
    "sectnum" span.

  - Removed attribute `HTMLTranslator.topic_classes`

  - Items of a definition list with class argument "details" are
    converted to <details> disclosure elements.

* docutils/writers/html4css1/__init__.py

  - Overwrite methods in _html_base.HTMLTranslator that use HTML5 tags
    (details, aside, nav, ...) and attributes (role, aria-level).

* docutils/writers/latex2e/__init__.py

  - The setting `legacy_class_functions`_ now defaults to "False".
    Adapt stylesheets modifying ``\DUadmonition`` and/or ``\DUtitle``.

  - Apply patch #181 "Fix tocdepth when chapter/part in use" by
    John Thorvald Wodder II.

  - Fix newlines after/before `ids_to_labels()` (cf. patch #183).

  - Refactor/revise ToC writing.

  - Don't add ``\phantomsection`` to labels in math-blocks.

  - Improve spacing and allow customization of Docutils-generated table
    of contents.

  - New algorithm for table column widths. Fixes bug #422.
    New configuration setting `legacy_column_widths`_.

    `Table.set_table_style()` arguments changed.

    Only write "continued on next page..." if it fits
    without making the table columns wider.

    Table "width" option overrides conflicting "auto" column "widths".

* docutils/writers/latex2e/docutils.sty

  - Fix excessive padding above sidebar titles.

* docutils/writers/pseudoxml.py

  - Fix option `detailed`_ under Python 2.7.

* docutils/writers/s5_html/themes/default

  - Remove IE 6 compatibility workarounds ``iepngfix.htc`` and
    ``blank.gif`` (fixes bug #169).

* docutils/writers/manpage.py

  - Fix: double quotes need to be escaped on macro invocation.
    Done everywhere.


Release 0.17.1 (2021-04-16)
===========================

* docutils/utils/math/latex2mathml.py

  - Fix bug #406 (MathML translation of ``\mathbf``).

* docutils/writers/latex2e/__init__.py

  - Open ``docutils.sty`` with encoding set to "utf-8".
    Fixes bug #414: error with Py3k when locale encoding is "ascii".

* docutils/parsers/ docutils/transforms/

  - Provide fallbacks for parser config settings
    to facilitate programmatic use.

* docutils/writers/manpage.py

  - Apply patch #166: move macro defs above ``.TH``
    (thanks Willie and sorry for the delay).


Release 0.17 (2021-04-03)
=========================

* General

  - Installing with ``setup.py`` now requires `setuptools`.
    Alternatively, install with `pip`_ (or "manually").
  - Use `importlib.import_module()` to programmatically import modules.
  - Fix bug #385: Import of language modules.

  .. _pip: https://pypi.org/project/pip/

* docs/ref/docutils.dtd

  - The "title" attribute of <sidebar> elements is now optional.

* docutils/MANIFEST.in

  - Exclude test outputs.

* docutils/__init__.py

  - VersionInfo:  `ValueError` for invalid values, fix comparison to tuples.

* docutils/languages/
  docutils/parsers/rst/languages/

  - Apply patch # 177 Arabic mappings by Shahin.
  - Apply patch for bug #399 Fixes in Korean translation by Shinjo Park.

* docutils/nodes.py

  - Apply patch #165 "Fix error when copying `system_message` node"
    by Takeshi KOMIYA.
  - Apply version of patch #167 "Let `document.set_id()` register all
    existing IDs". Thanks to Takeshi KOMIYA.
  - Fix bug #410: Use a "property" function to recursively fetch
    `Node.document` value from parent node.

* docutils/parsers/recommonmark_wrapper.py

  - New, **experimental** wrapper to integrate the
    `recommonmark`_ Markdown parser for use with Docutils.
    Currently only tested with `recommonmark` version 0.4.0.

    .. _recommonmark: https://pypi.org/project/recommonmark/

* docutils/parsers/rst/directives/body.py

  - Make the sidebar's "title" argument optional (feature request #69).

* docutils/parsers/rst/directives/html.py

  - Make `meta` elements available for "latex" and "odt" writers.

* docutils/parsers/rst/directives/misc.py

  - Prevent infinite inclusion loops.

* docutils/parsers/rst/roles.py

  - Apply patch #174 "Lowercase new role names on registration"
    by John Thorvald Wodder II.

* docutils/utils/smartquotes.py

  - Fix bug #383: Smart quotes around opening and separator characters.

* docutils/transforms/components.py

  - Allow a comma-separated list of formats for the Filter transform.

* docutils/writers/html*

  - Implement feature request #40 "Option to embed images as data URI".

* docutils/writers/html5_polyglot/__init__.py

  - Use the new semantic tags <main>, <section>, <header>,
    <footer>, <aside>, <figure>, and <figcaption>.
    See ``minimal.css`` and ``plain.css`` for styling rule examples.

    Change the `initial_header_level`_ setting default to "2", as browsers
    use the `same style for <h1> and <h2> when nested in a <section\>`__.

    __ https://stackoverflow.com/questions/39547412/same-font-size-for-h1-and-h2-in-article

  - Use HTML text-level tags <small>, <s>, <q>, <dfn>, <var>, <samp>, <kbd>,
    <i>, <b>, <u>, <mark>, and <bdi> if a unique, matching class value
    is found in `\<inline>`_ and `\<literal>`_ elements.
    Use <ins> and <del> if a unique matching class value
    is found in `inline`, `literal`, or `container` elements.
    Use <small> for generated code line numbers.

  - Fix bug #398: properly close link tag to "schema.dcterms".

  - Add a `viewport meta tag`__ to fix rendering in mobile browsers.

    __ https://developer.mozilla.org/en-US/docs/Web/HTML/Viewport_meta_tag

  - Use <video> for images with video MIME types supported by HTML5.

* docutils/writers/html5_polyglot/minimal.css

  - Move non-essential styling to ``plain.css``.
    Small fixes and tweaks.

  - Support "captionbelow" class value for tables.

  - Display code line numbers as pseudo-elements which are skipped
    when copying text from code blocks. Solves feature request #32.

* docutils/writers/html5_polyglot/plain.css

  - Support numbered figures.

* docutils/writers/html5_polyglot/responsive.css

  - New optional style that adapts to different screen sizes.

* docutils/writers/latex2e/__init__.py

  - Use LaTeX environments for admonitions and "class wrappers" for styling
    admonitions and titles if the new configuration setting
    `legacy_class_functions`_ is False.

  - Remove backwards compatibility code for the deprecated
    `styling command`__ prefix ``\docutilsrole``.

    __ docs/user/latex.html#custom-interpreted-text-roles

  - Remove legacy LaTeX stylesheet ``docutils-05-compat.sty``.

  - Support the `memoir` LaTeX document class.
    Fixes bugs #390, #391, and #392. Thanks to John Thorvald Wodder II.

  - The special value "auto" for the `graphicx_option`_ setting
    is no longer supported (it never worked for xetex/luatex).

  - Most helper commands and element definitions are now defined in the
    LaTeX package `docutils.sty`_ and only inserted in the document
    preamble if the `stylesheet`__ setting does not list "docutils".

    .. _docutils.sty: https://ctan.org/pkg/docutils
    __ docs/user/config.html#stylesheet-latex-writers

  - Apply patch #173 "Make \*TeX writers convert nonstandard table
    classes to DUclass environments" by John Thorvald Wodder II.

  - Fix bug #408 "Incorrect assert in latex writer
    for multiple citation references".

  - Apply patch #175 "Fix alignment of nested tables"
    by John Thorvald Wodder II. Additional fixes to table alignment.

  - Do not write Docutils-generated ToC, when ``use_latex_toc == True``.
    (This did happen when publishing from a doctree.)

  - Set PDF document properties from "meta" directive content.

  - Apply version of patch #176 "LaTeX writer: Append ``\leavevmode`` to
    non-docinfo field names" by John Thorvald Wodder II.

* docutils/writers/manpage.py

  - Fix #394 fix missing new line after rubric.
  - Patch #168 fix crashing on empty citation (by Takeshi KOMIYA).
  - Fix #126 manpage title with spaces.
  - Fix #380 command line option problem in sphinx.

* docutils/writers/odf_odt/__init__.py

  - Fix/improve metadata handling:
    fix "keyword" splitting,
    allow generic fields (stored as "Custom Properties").

* docutils/writers/pseudoxml.py

  - New option `detailled`__.

    __ detailed_

* test/DocutilsTestSupport.py

  - Run python3 test like python2 against source not the build/-directory

* tools/docutils-cli.py

  - New generic command line front end that allows the free selection of
    reader, parser, and writer components.


Release 0.16 (2020-01-16)
=========================

* General

  - Dropped support for Python 2.6, 3.3 and 3.4
  - Docutils now supports Python 2.7 and Python 3.5+ natively
    (without conversion by `2to3`).
  - Keep `backslash escapes`__ in the document tree. Backslash characters in
    text are be represented by NULL characters in the `text` attribute of
    Doctree nodes and removed in the writing stage by the node's
    `astext()` method.

  __ https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#escaping-mechanism

* docs/ref/docutils.dtd

  - Use "parameter entities" for `class names`, `reference names`,
    and `ids`.

* docutils/io.py

  - Remove the `handle_io_errors` option from io.FileInput/Output.

* docutils/nodes.py

  - Speed up Node.next_node().
  - If `auto_id_prefix`_ ends with "%", this is replaced with the tag name.
  - Warn about `Node.traverse()` returning an iterator instead of a list
    in future.

* docutils/statemachine.py

  - Patch [ 158 ] Speed up patterns by saving compiled versions (eric89gxl)

* docutils/transforms/universal.py

  - Fix [ 332 ] Standard backslash escape for smartquotes.
  - Fix [ 342 ] No escape in roles descending from `inline literal`.

* docutils/utils/__init__.py

  - `unescape()` definition moved to `nodes` to avoid circular import
    dependency. Fixes [ 366 ].

* docutils/writers/latex2e/__init__.py

  - Fix topic subtitle.
  - Make "rubric" bold-italic and left aligned.
  - Fix [ 339 ] don't use "alltt" or literal-block-environment
    in admonitions and footnotes.
  - Deprecation warning for ``\docutilsrole``-prefixed styling commands.
  - Add "latex writers" to the `config_section_dependencies`.
  - Ignore classes for `rubric` elements
    (class wrapper interferes with LaTeX formatting).

* docutils/writers/manpage.py

  - Apply fix for [ 287 ] comma after option is bold.
  - Apply fix for [ 289 ], line starting with ``.`` in a text.

* docutils/writers/odf_odt/__init__.py

  - Fix: ElementTree.getchildren deprecated warning

* docutils/writers/xetex/__init__.py

  - Add "latex writers" to the `config_section_dependencies`.

* test/alltests.py

  - Fix [ 377 ] ResourceWarning: unclosed file python3.8
    Close alltests.out with atexit.

* test/functional/*

  - Fix [ 377 ] ResourceWarning: unclosed file python3.8
    Read defaults file with context.

  - Set `auto_id_prefix`_ to "%" (expands to tag-names).
    Results in descriptive links in HTML and more localized changes when
    editions to the input add or remove auto-ids.

* test/test_io.py

  - Apply patch #157: avoid test failure because of a `ResourceWarning`.

* test/test_writers/test_odt.py

  - Fix [ 359 ] Test suite fails on Python 3.8. odt XML sorting.
    Use ElementTree instead of minidom.

* tools/buildhtml.py

  - New option `html_writer`_.


Release 0.15.1 (2019-07-24)
===========================

source: branches/rel-0.15

Fix [ 366 ] circular dependency. Release for Python 2 only.


Release 0.15 (2019-07-20)
=========================

* General

  - Dropped support for Python 2.4, 2.5, 3.1, and 3.2.
  - Infrastructure automation.

* docs/ref/docutils.dtd

  - The <table> element accepts the new attribute "width".

* docs/ref/rst/restructuredtext.txt

  - Document rST syntax change: Tokens like ``:this:example:`` are now valid
    field list names (instead of ordinary text).

* docutils/io.py

  - Fix [ 348 ] Since Python 3.4, the 'U' universal newlines mode has been
    deprecated. Thanks to hugovk.

* docutils/languages/ko.py, docutils/parsers/rst/languages/ko.py

  - Apply [ 153 ] Korean mappings by Thomas Sungjin Kang.

* docutils/nodes.py

  - Fix [ 251 ] `system_message.copy()`  `TypeError`.
  - `Element.copy()` also copies `document`, `line`, and `source` attributes.

* docutils/parsers/rst/__init__.py

  - Apply [ 152 ] reset `default role` at end of document.

* docutils/parsers/rst/states.py

  - Allow embedded colons in field list field names.

* docutils/parsers/rst/directives/html.py

  - Fix bug #281: Remove escaping backslashes in meta directive content.

* docutils/parsers/rst/directives/misc.py

  - Don't convert tabs to spaces, if `tab_width` is negative in
    "include" directive with "code" option.

* docutils/parsers/rst/directives/tables.py

  - Apply patch #121: Add "width" option for the table directives.

* docutils/transforms/frontmatter.py

  - Add field name as class argument to generic docinfo fields unconditionally.

* docutils/transforms/references.py

  - Fix bug #331: fixed the "trim" options of the "unicode" directive.

* docutils/utils/__init__.py

  - Deprecate `unique_combination()` (obsoleted by `itertools.combination()`.

* docutils/utils/smartquotes.py

  - Fix bug #332: use open quote after whitespace, ZWSP, and ZWNJ.

* docutils/writers/html5_polyglot/

  - automatically add HTML5-compatible meta tags for docinfo items
    "authors", "date", and "copyright".

* docutils/writers/_html_base.py

  - Fix bug #358: Non-breaking space removed from fixed-width literal.

* docutils/writers/latex2e/__init__.py

  - Fix bug #323: spurious ``\phantomsection`` and whitespace in
    ``parts['title']``.
  - Fix bug #324: Invalid LaTeX for table with empty multi-column cell.
  - Fixes to literal block handling.


Release 0.14 (2017-08-03)
=========================

* docs/ref/docutils.dtd

  - Enable validation of Docutils XML documents against the DTD:

    Use attribute type NMTOKEN instead of REFID for the `refid` attribute
    and NMTOKENS for `backrefs`: REFID refers to an ID type instance,
    however, the `ids` attribute cannot use the ID type because `XML only
    allows one ID per Element Type`__ and doesn't support a multiple-ID
    "IDS" attribute type.

  __ https://www.w3.org/TR/REC-xml/#sec-attribute-types

* docs/ref/rst/restructuredtext.txt

  - Added documentation for escaped whitespace in URI contexts.
  - Clarify use of Unicode character categories.

* docutils/parsers/rst/states.py

  - Added functionality: escaped whitespace in URI contexts.
  - Consistent handling of all whitespace characters in inline markup
    recognition. Fixes [ 307 ] and [ 3402314 ] (now [ 173 ]).

* docutils/parsers/rst/directives/images.py

  - Added support for escaped whitespace in URI contexts.

* docutils/parsers/rst/directives/tables.py

  - Rework patch [ 120 ] (revert change to Table.get_column_widths()
    that led to problems in an application with a custom table directive).

* docutils/transforms/frontmatter.py

  - Fix [ 320 ] Russian docinfo fields not recognized.

* docutils/transforms/references.py

  - Don't add a second ID to problematic references.

* docutils/transforms/universal.py

  Fix `SmartQuotes`: warn only once if language is unsupported,
  keep "rawsource" when "educating" quotes.

* docutils/utils/__init__.py

  - Added `split_escaped_whitespac()` function, support for escaped
    whitespace in URI contexts.

* docutils/utils/error_reporting.py

  - Fix [ 321 ] Import block might cause name error.

* docutils/utils/smartquotes.py

  - Update quote definitions for languages et, fi, fr, ro, sv, tr, uk.
  - New quote definitions for hr, hsb, hu, lv, sh, sl, sr.
  - Fix [ 313 ] Differentiate apostrophe from closing single quote
    (if possible).
  - Fix [ 317 ] Extra space inserted with French smartquotes.
  - Add command line interface for stand-alone use (requires 2.7).

* docutils/writers/_html_base.py

  - Provide default title in metadata (required by HTML5).
  - Fix [ 312 ] HTML writer generates invalid HTML if the table has two tags.
  - Fix [ 319 ] The MathJax CDN shut down on April 30, 2017. For security
    reasons, we don't use a third party public installation as default but
    warn if `math_output`_ is set to MathJax without specifying a URL.

* docutils/writers/html4css1/__init__.py

  - Apply [ 125 ] HTML writer: respect automatic table column sizing.

* docutils/writers/latex2e/__init__.py

  - Handle class arguments for block-level elements by wrapping them
    in a "DUclass" environment. This replaces the special handling for
    `epigraph` and `topic` elements.

* docutils/writers/manpage.py

  - Apply [ 141 ] Handling inline in manpage writer.

* docutils/writers/odf_odt/__init__.py

  - Command line setting `language`_ now sets the default language of the
    generated ODF document.
  - The use of image directive options :width: (%), :scale:, etc now
    set the width/height/size of images in the generated ODF
    documents.
  - The heading/title of admonitions now reflects the language
    specified by the `language`_ setting.
  - Fixed [ 306 ] only first of multiple "image" directives with the same URL
    shown in output.
  - Fixed [ 282 ] python3:  `AttributeError`.

* tools/rst2html4.py: New front-end.

* tools/dev/generate_punctuation_chars.py: New script
  to test and update utils.punctuation_chars.


Release 0.13.1 (2016-12-09)
===========================

* docs/ref/docutils.dtd

  - Add the document tree elements <math> and <math_block> (already in use).

* docutils/languages/fa.py
  docutils/parsers/rst/languages/fa.py
  docutils/languages/la.py
  docutils/parsers/rst/languages/la.py:

  - Apply [ 133 ] Persian mappings by Shahin Azad.
  - Apply [ 135 ] Language modules for Latvian by Alexander Smishlajev

* docutils/nodes.py

  - Fix [ 253 ] Attribute key without value not allowed in XML.

* docutils/parsers/

  - Apply [ 103 ] Recognize inline markups without word boundaries.
  - Enable escaping in embedded URIs and aliases (fixes [ 284 ]).

* docutils/parsers/rst/__init__.py

  - Fix [ 233 ] Change the base URL for the :rfc: role.

* docutils/parsers/rst/directives/tables.py

  - Apply [ 120 ] tables accept option widths: list of relative widths, 'auto'
    or 'grid'.

  - Implement feature request [ 48 ]
    Add :align: option to the table directives.
    Thanks to Takeshi KOMIYA for the patch.

* docutils/parsers/rst/roles.py

  - Fix [ 295 ] Class argument for custom role inheriting from math.

* docutils/parsers/rst/tableparser.py

  - Really fix [ 159 ] Spurious table column alignment errors.

* docutils/transforms/frontmatter.py

  - Add name of generic bibliographic fields as a "classes" attribute value
    (after conversion to a valid identifier form).

* docutils/utils/error_reporting.py

  - Fix [ 130 ] support streams expecting byte-strings in ErrorOutput.

* docutils/utils/math/math2html.py

  - Add ``\colon`` macro, fix spacing around colons. Fixes [ 246 ].
  - New upstream version (additional macros, piece-wise integrals and sums).

* docutils/writers/_html_base.py

  - New auxiliary module for definitions common to all HTML writers.

* docutils/writers/html5_polyglot/

  - New HTML writer generating clean, polyglot_ markup conforming to
    `HTML 5`_.

    The CSS stylesheets ``minimal.css`` and ``plain.css`` contain required
    and recommended layout rules.

* docutils/writers/html4css1/__init__.py

  - Add "docutils" to class values for "container" object to address [ 267 ].
  - Apply patch [ 119 ] by Anatoly Techtonik: use absolute paths for
    `default_stylesheet_path` and `default_template_path`.
  - Fix [ 266 ] creating labels/class values in description list items.
  - Do not use <sup> and <sub> tags inside <pre> (parsed-literal blocks).
  - Fix footnotes with content that does not start with a paragraph.
  - Use https in default MathJax URL (report Alan G Isaac).
  - Outsourcing of common code to _html_base.py.

* docutils/writers/latex2e/__init__.py

  - Fix [ 262 ] Use ``\linewidth`` instead of ``\textwidth`` for figures,
    admonitions and docinfo.

  - Use absolute path for `default_template_path`.

  - Removed deprecated options ``--use-latex-footnotes`` and
    ``--figure-footnotes``.

  - Cleaner LaTeX code for enumerations and literal blocks.

  - Use `hyperref` package together with `bookmark` (improved hyperlinking
    by the same author).

  - Fix [ 286 ] Empty column title cause invalid latex file.

  - Fix [ 224 ] Fix rowspan support for tables.

  - Let LaTeX determine the column widths in tables with "colwidths-auto".
    Not suited for multi-paragraph cells!

* docutils/writers/odf_odt/__init__.py

  - remove decode.encode of filename stored in zip.

* docutils/writers/xetex/__init__.py

  - LuaLaTex compatibility: do not load `xunicode` package.

* tools/

  - New front-end ``rst2html5.py``.

* tox.ini

  - Test py26, py27, py33 and py34.

    To use, install the `tox` package via pip or easy_install and use
    tox from the project root directory.

.. _polyglot: https://www.w3.org/TR/html-polyglot/
.. _HTML 5: https://www.w3.org/TR/html5/


Release 0.12 (2014-07-06)
=========================

* docs/ref/rst/directives.txt

  - Update "math" and "csv-table" descriptions.

* docutils/parsers/rst/directives/images.py

  - Fix [ 258 ] ``figwidth="image"`` generates unitless width value.

* docutils/parsers/rst/states.py

  - Improve error report when a non-ASCII character is specified as
    delimiter, quote or escape character under Python 2.
    Fixes [ 249 ] and [ 250 ].

* docutils/writers/html4css1/__init__.py

  - Don't add newline after inline math.
    Thanks to Yury G. Kudryashov for the patch.

* docutils/writers/latex2e/__init__.py

  - Fix [ 239 ] Latex writer glues paragraphs with figure floats.
  - Apply [ 116 ] by Kirill Smelkov. Don't hard code \large for subtitle.

* docutils/writers/odf_odt/__init__.py

  - Apply patch by Jakub Wilk to fix bug [ 100 ].

* test/test_error_reporting.py

  - Fix [ 223 ] by removing redundant tests we do not have control over.

* test/test_nodes.py

  - Apply [ 115 ] respect fixed 2to3 string literal conversion behaviour.


Release 0.11 (2013-07-22)
=========================

* General

  - Apply [ 2714873 ] Fix for the overwriting of document attributes.
  - Support embedded aliases within hyperlink references.
  - Fix [ 228 ] try local import of docutils components (reader, writer, parser,
    language module) before global search.

* docutils/nodes.py

  - Fix [ 3601607 ] `node.__repr__()` must return `str` instance.

* docutils/parsers/rst/directives/__init__.py

  - Fix [ 3606028 ] `assert` is skipped with ``python -O``.

* docutils/parsers/rst/directives/images.py

  - Apply [ 3599485 ] node source/line information for sphinx translation.

* docutils/parsers/rst/directives/tables.py

  - Fix [ 210 ] Python 3.3 checks CVS syntax only if "strict" is True.

* docutils/parsers/rst/states.py

  - Fix [ 157 ] Line block parsing doesn't like system message.
  - Always import our local copy of roman.py (report Larry Hastings).

* docutils/transforms/references.py

  - Fix [ 3607029 ] traceback with embedded alias pointing to missing target.

* docutils/utils/__init__.py

  - Fix [ 3596884 ] exception importing `docutils.io`.

* docutils/writers/html4css1/__init__.py

  - Fix [ 3600051 ] for tables in a list, table cells are not compacted.
  - New setting `stylesheet_dirs`_: Comma-separated list of directories
    where stylesheets are found. Used by `stylesheet_path` when expanding
    relative path arguments.
  - New default for `math_output`_: ``HTML math.css``.
  - Avoid repeated class declarations in html4css1 writer
    (modified version of patch [ 104 ]).


* docutils/writers/latex2e/__init__.py

  - Drop the simple algorithm replacing straight double quotes with
    English typographic ones.
    Use the `smart_quotes`_ setting to activate this feature.
  - Fix literal use of babel shorthands (straight quote, tilde, ...).
  - Fix [ 3603246 ] Bug in option ``--graphicx-option=auto``.
  - New setting `stylesheet_dirs`__.

    __ docs/user/config.html#stylesheet-dirs-latex-writers


* docutils/writers/manpage.py

  - Fix [3607063] handle lines starting with a period.
  - Fix option separating comma was bold (thanks to Bill Morris).


Release 0.10 (2012-12-16)
=========================

* General

  - Dropped support for Python 2.3.
  - ``docutils/math``, ``docutils/error_reporting.py``, and
    ``docutils/urischemes.py`` moved to the utils package.
  - Fix [3541369] Relative __import__ also with Python 3.3.
  - Fix [3559988] and [3560841] __import__ local writer, reader, languages
    and parsers for Python 2.7 up.
  - Fix import of PIL.Image.
  - Change default of `syntax_highlight`_ option to "long",
    basic syntax highlight styles for LaTeX and HTML.

* docutils/io.py

  - FileInput/FileOutput: no system-exit on IOError.  The `handle_io_errors`
    option is ignored and will be removed in a future release.
  - Fix Py3k error writing to stdout with encoding differing from default.
  - Fix opening binary files under Py3k (thanks to Dominic Fitzpatrick).

* docutils/parsers/rst/directives/misc.py

  - Fix [ 3546533 ] Unicode error with "date" directive.

* docutils/transforms/universal.py

  - SmartQuotes transform for typographic quotes and dashes.

* docutils/utils/__init__.py

  - `normalize_language_tag()` now returns `BCP 47`_ conforming tags
    with sub-tags separated by ``-``.

* docutils/writers/html4css1/__init__.py

  - Use ``<code>`` tag for inline "code",
    do not drop nested inline nodes (syntax highlight tokens).
  - Customizable MathJax URL (based on patch by Dmitry Shachnev).
  - No line break after opening inline math tag.

* docutils/writers/manpage.py

  - Apply [ 3527401 ] admonition's don't preserve indentation
  - Apply [ 3527397 ] Add indentation to literal blocks in manpage writer.

* docutils/writers/xetex/__init__.py

  - Apply [ 3555160 ] ensure order of "otherlanguages".
  - Fix section numbering by LaTeX.

* docutils/writers/s5_html/__init__.py

  - Fix [ 3556388 ] MathJax does not work with rst2s5.

* docutils/writers/docutils_xml.py

  - Fix [ 3552403 ] Prevent broken PyXML replacing stdlibs xml module.
  - Fix/improve output with `indents`_ setting.

* setup.py

  - Tag ``math.css`` stylesheet as data file (patch by Dmitry Shachnev).

* tools/test/test_buildhtml.py

  - Fix [ 3521167 ] allow running in any directory.
  - Fix [ 3521168 ] allow running with Python 3.


Release 0.9.1 (2012-06-17)
==========================

* setup.py

  - Fix [ 3527842 ]. Under Python 3, converted tests and tools were
    installed in the PYTHONPATH. Converted tests are now
    stored in ``test3/``, tools no longer need conversion.

    If you installed one of Docutils versions 0.7 ... 0.9 with
    ``setup.py install`` under Python 3, remove the spurious
    ``test/`` and ``tools/`` directories in the site library root.

* test/

  - Make tests independent from the location of the ``test/`` directory.
  - Use converted sources (from the ``build/`` directory) for tests under
    Python 3.

* tools/

  - Make tools compatible with both, Python 2 and 3 without 2to3-conversion.

* docutils/io.py

  - Fix writing binary data to sys.stdout under Python 3 (allows
    ``rst2odt.py`` to be used with output redirection).

* docutils/parsers/rst/directives/misc.py

  - Fix [ 3525847 ]. Catch and report UnicodeEncodeError with
    ``locale == C`` and 8-bit char in path argument of `include` directive.

* test/alltests.py

  - class `Tee`: catch  `UnicodeError` when writing to "ascii" stream or
    file under Python 3.


Release 0.9 (2012-05-02)
========================

* General:

  - New reStructuredText "code" role and directive and "code" option
    of the "include" directive with syntax highlighting by Pygments_.
  - Fix parse_option_marker for option arguments containing ``=``.
  - Fix [ 2993756 ] import Python Imaging Library's Image module
    via ``import PIL`` as starting with PIL 1.2,
    "PIL lives in the PIL namespace only" (announcement__).

.. _Pygments: https://pygments.org/
__ https://mail.python.org/pipermail/image-sig/2011-January/006650.html

* setup.py

  - Fix [ 2971827 ] and [ 3442827 ]
    extras/roman.py moved to docutils/utils/roman.py

* docutils/frontend.py

  - Fix [ 3481980 ] Use `os.getcwdu()` in `make_paths_absolute()`.

* docutils/io.py

  - Fix [ 3395948 ] (Work around encoding problems in Py3k).
  - `mode` argument for FileOutput avoids code replication in
    BinaryFileOutput.
  - New exceptions  `InputError` and  `OutputError` for IO errors in
    FileInput/FileOutput.

* docutils/core.py

  - No "hard" system exit on file IO errors: catch and report them in
    `Publisher.reportException` instead. Allows handling by a calling
    application if the configuration setting `traceback`_ is True.

* docutils/utils.py -> docutils/utils/__init__.py

  - docutils.utils is now a package (providing a place for sub-modules)

  - DependencyList uses io.FileOutput and 'utf-8' encoding to prevent
    errors recording non-ASCII filenames (fixes [ 3434355 ]).

  - Fix `relative_path()` with source=None and `unicode` target.

* docutils/parsers/rst/states.py

  - Fix [ 3402314 ] allow non-ASCII whitespace, punctuation
    characters and "international" quotes around inline markup.
  - Use `field_marker` pattern to look for start of a
    directive option block (fixes [ 3484857 ]).

* docutils/parsers/rst/tableparser.py

  - Fix [ 2926161 ] for simple tables.
    (Combining chars in grid tables still contribute to cell width.)

* docutils/writers/latex2e/__init__.py

  - Support the `abbreviation` and `acronym` standard roles.
  - Record only files required to generate the LaTeX source as dependencies.
  - Fix handling of missing stylesheets.
  - Use ``\setcounter{secnumdepth}{0}`` instead of ``*``-versions
    when suppressing LaTeX section numbering.
  - Use ``\DUtitle`` for unsupported section levels.
  - Apply [ 3512791 ] do not compare string literals with "is".

* docutils/writers/xetex/__init__.py

  - Avoid code duplication with latex2e writer (solves [ 3512728 ]).

* docutils/writers/html4css1/__init__.py

  - Change default for `math_output`_ setting to MathJax.
  - Fix handling of missing stylesheets.

* docutils/writers/docutils_xml.py

  - Use the visitor pattern with `default_visit()`/`default_depart()` methods
    instead of minidom to facilitate special handling of selected nodes.
  - Support raw XML (inserted as-is inside a <raw></raw> node).

* docutils/writers/manpage.py

  - Do not emit comment line with trailing blank. Problematic for VCS.


Release 0.8.1 (2011-08-30)
==========================

* General:

  - Fix [ 3364658 ] (Change last file with Apache license to BSD-2-Clause)
    and [ 3395920 ] (correct copyright info for rst.el).

* test/

  -  Apply [ 3303733 ] and [ 3365041 ] to fix tests under Py3k.

* docutils/writers/latex2e/__init__.py

  - Clean up Babel language setting. Restores Sphinx compatibility.


Release 0.8 (2011-07-07)
========================

* General:

  - Handle language codes according to `BCP 47`_.
  - If the specified language is not supported by Docutils,
    warn and fall back to English.
  - Math support: reStructuredText "math" role and directive,
    `math` and `math_block` doctree elements.
  - Decode command line arguments with the locale's preferred encoding
    (to allow, e.g., ``--title=Dornröschen``).
  - Orphaned `python` reader and `newlatex2e` writer moved to the sandbox.
  - New sub-module `error_reporting`: handle encoding/decoding errors
    when reporting exceptions.
  - Some additions to the Docutils core are released under the 2-Clause BSD
    license, see COPYING_ for details.

  .. _BCP 47: https://www.rfc-editor.org/rfc/bcp/bcp47.txt
  .. _COPYING: COPYING.html

* reStructuredText:

  - Most directives now support a "name" option that attaches a
    reference name.

  - Directive content may start on the first line also when the directive
    type accepts options.

* docs/dev/policies.txt

  - Recommend the 2-Clause BSD license
    (http://opensource.org/licenses/BSD-2-Clause)
    for code that is kept under the author's copyright.

* tools/buildhtml.py

  - Fix ``--local`` switch.

* Fix [ 3018371 ] Added Lithuanian mappings by Dalius Dobravolskas.

* docutils/writers/html4css1/__init__.py

  - Set "lang" argument for objects with class argument
    "language-<language tag>".
  - New setting `math_output`_ with support for HTML, MathML, and LaTeX.

* docutils/writers/latex2e/__init__.py

  - Fix [ 3043986 ]  `AttributeError` using :local: with table of content.
  - Place title data in the document preamble.
  - Load `babel` package only if required.
  - Update list of supported languages.
  - New config setting `hyperref_options`_.
    No hard-coded "unicode" hyperref option (clash with xetex).
  - Set language for custom roles, paragraphs, block-quotes, and
    line-quotes with class argument "language-<language tag>".
  - Fix [ 3095603 ] wrong quotes output for Russian and other languages.
  - Convert image URI to a local file path.
  - Apply [ 3148141 ] fix multicolumn support when a colspanning cell
    has more than one paragraph (Wolfgang Scherer).
  - \leavevmode before longtable only when needed (prevents spurious vspace)
  - do not advance table counter for tables without caption

* docutils/writers/xetex/__init__.py

  - New writer generating LaTeX code for compiling with ``xelatex``.

    A separate writer (inheriting from latex2e) instead of a ``--xetex``
    option allows separate config options for XeTeX vs. LaTeX2e.

* docutils/writers/manpage.py

  - Fix: BUG#3219183 - vertical space in definition lists containing markup.
  - Fix: vertical space cleaning for option group ``.``.

* tools/editors/emacs/rst.el

  - Fix [ 3001100 ] does not handle spaces in filenames.
    Thanks to Jakub Wilk.

* docutils/utils.py

  - strip whitespace from stylesheet arguments
  - exclude combining chars from column_width()
    (partial fix for [ 2926161 ])

* docutils/parsers/rst/directives/misc.py

  - Fix [ 1830389 ] Replace not breaking on getting system_messages from
    nested_parse

* docutils/io.py

  - Do not ``close()`` `sys.stdin`, `sys.stdout`, or `sys.stderr`. Prevents
    ``Exception ValueError: 'I/O operation on closed file.'`` with Python 3.


Release 0.7 (2010-07-07)
========================

* General:

  - Fix [ 2881769 ] setup configuration.
  - Fix [ 2788716 ] reporting problems in included files.

* docutils/io.py

  - FileInput opens files as text files with universal newline support
    (mode "rU", configurable with the new optional argument "mode").

* docutils/nodes.py

  - Fix [ 2975987 ] repr(Text) failed with long string (Jeffrey C. Jacobs).

* docutils/utils.py

  - Fix [ 2923723 ] let `decode_path()` tolerate ``path == None``.

* docutils/writers/html4css1/__init__.py

  - Support SVG and SWF images (thanks to Stefan Rank).
  - Generate valid XHTML for centred images with targets.
    Use CSS classes instead of "align" tags for image alignment.

* docutils/writers/latex2e/__init__.py

  - Use `transforms.writer_aux.Admonitions` to "normalize" special
    admonitions.
  - Use the ``\url`` command for URLs (breaks long URLs instead of
    writing into the margin).
  - Preserve runs of spaces in `inline literals`__.
  - Deprecate `figure_footnotes`_ setting.
  - Rename `use_latex_footnotes`_ setting to `docutils_footnotes`_.
  - New `latex_preamble`_ setting.
  - Use PDF standard fonts (Times/Helvetica/Courier) as default.
  - Fix hyperlink targets (labels) for images, figures, and tables.
  - Apply [ 2961988 ] Load babel after inputenc and fontenc.
  - Apply [ 2961991 ] Call hyperref with unicode option.
  - Drop the special `output_encoding`_ default ("latin-1").
    The Docutils wide default (usually "UTF-8") is used instead.
  - Render inline markup in document title and subtitle.
  - Fix numbering depth with LaTeX section numbering.
  - Update Unicode -> LaTeX translations.
  - Fix bug with topic directive (thanks to Alan G Isaac for reporting).

__ docs/ref/restructuredtext.html#inline-literals

* docutils/writers/manpage.py

  - Fix: supported attribute (thanks to peter2108).
  - Remove trailing blanks in code (keep in sync with mercurial version).
  - Titles level 1, that is ``.SH``, always uppercase.
  - Apply patch from mg: literal text should be bold in man-pages.

* docutils/nodes.py

  - Fix: encoding ``'ascii'`` must be lowercase to prevent problems for
    Turkish locale.

* setup.py

  - Python 3 support: copy test/ and tools/ to the build-dir
    and convert Python sources with 2to3.


Release 0.6 (2009-10-11)
========================

* General:

  - Docutils is now compatible with Python versions from 2.3 up to 2.6
    and convertible to 3.1 code.

    + Node.__nonzero__ returns True instead of 1.
    + use os.walk instead os.path.walk.
    + minimize `types` module where possible.
    + Backwards-compatible changes to remove python2.6 -3 deprecation warnings
    + Text nodes now subclass unicode rather than UserString
      (which is gone in python 3.0).
    + 3.0 compatibility module docutils._compat

    + Drop 2.2 compatibility workarounds.
    + Drop extras/optparse.py and extras/textwrap.py
      (stdlib modules since 2.3).

  - OpenOffice export: ODT writer moved from sandbox to Docutils core.
  - Unix man page export: manpage writer moved from sandbox to Docutils
    core.

  - Apply [ 1719345 ] Galician translation
  - Apply [ 1905741 ] Polish translation
  - Apply [ 1878977 ] make_id(): deaccent characters.
  - Apply [ 2029251 ] return nonzero when tests fail.
  - Fix [ 1692788 ] allow UTF-8 in style sheets.
  - Fix [ 2781629 ] support non-ASCII chars in file names.
  - Apply [ 2845002 ] let ``--no-raw`` disable raw *roles* too.
  - Fix [ 2831643 ] renaming `DirectiveError.message` to `DirectiveError.msg`
  - Fix [ 2821266 ] ``--strict`` option works now like ``--halt=info``.
  - Fix [ 2788716 ]  `DirectiveError` now correctly reports source and line.
  - Fix [ 1627229 ] hyperlink references in substitutions.

  - The `newlatex` writer is orphaned.

* reStructuredText:

  - Documented Unicode characters allowed as inline markup openers,
    closers, and delimiters.
  - Allow units for all length specifications.
  - Allow percent sign in "scale" argument of "figure" and "image" directives.
  - Bugfix: The "figalign" argument of a figure now works as intended
    (aligning the figure, not its contents).
  - Align images with class "align-[right|center|left]"
    (allows setting the alignment of an image in a figure).

* docutils/nodes.py:

  - Added `Element.__contains_()` method, for the in-operator.

* docutils/parsers/rst/states.py:

  - Apply [ 1994493 ] Patch to support all kinds of quotes in inline markup.
  - Added support for Unicode inline markup delimiters "‐ ‑ ‒ – —" and
    " " (non-breaking space), and "¡ ¿" openers.

* docutils/parsers/directives/misc.py:

  - Added ``start-line`` and ``end-line`` options to "include"
    directive to select a range of lines.
  - Hard tabs in literal inclusions are replaced by spaces. This is
    configurable via the new ``tab-width`` option of the "include" directive
    (a negative tab-width prevents tab expansion).

* docutils/utils.py:

  - Add `get_stylesheet_lis()` function.
  - Apply [ 2834836 ] print info at halt

* docutils/transforms/universal.py:

  - Raise default priority of StripClasses to exclude stripped classes from
    the ToC.

* docutils/writers/html4css1/__init__.py:

  - `stylesheet`_ and `stylesheet_path`_ settings support a comma
    separated list of stylesheets.
  - Address [ 1938891 ] Inline literal text creates "pre" span only when
    needed to prevent inter-word line wraps.
  - Use `translate()` method instead of repeated `replace()` calls.
  - Fix [ 1757105 ] New `table_style`_ setting. Added to standard table
    classes to allow CSS styling that does not interfere with other
    table-using constructs (field lists, citations, ...).

* docutils/writers/newlatex2e/__init__.py:

  - Apply [ 1612821 ] Double quotes in literal text in Italian/German

* docutils/writers/latex2e/__init__.py:

  - Add `embed_stylesheet`_ setting.
  - Apply [ 1474017 ] image vertical alignment is reversed.
  - Apply [ 2051599 ] multi-page tables in latex writer (from pabigot).
  - Change: has_key for dictionaries (not Nodes) to in-operator.
  - Merge adjacent citations into one latex cite command.
  - Failsafe implementation of custom roles. LaTeX compilation now ignores
    unknown classes instead of aborting with an error.
  - Support custom roles based on standard roles.
  - LaTeX packages can be used as `stylesheet`_ arguments without
    restriction. (A style sheet is now referenced with the ``\usepackage``
    command, if it ends with ``.sty`` or has no extension.)
  - Add ``bp`` to lengths without unit (prevents LaTeX errors).
  - Correctly write length unit ``pt`` as ``bp`` in LaTeX.
  - Do not convert ``px`` to ``pt`` (``px`` is supported by pdfTeX since
    2005-02-04 as a configurable length unit).
  - Do not use fontenc, nor the obsolete 'ae' and 'aeguill' packages
    if font-encoding is set to ''. LaTeX defaults to OT1 then.
  - Set sub- and superscript role argument in text mode not as math.
    Use a custom role based on sub-/superscript if you want italic shape.
  - Shorter preamble and less dependencies: Load packages and define macros
    only if required in the document.
  - Use the name prefix ``DU`` for all Docutils specific LaTeX macros.
  - New custom environments and commands with optional "classes" argument.
  - Simpler LaTeX encoding, e.g. "\%" instead of "{\%}".
  - Better conformance to Docutils specifications with `use_latex_toc`_.
    Support for LaTeX generated ToC also with unnumbered sections.
  - If 'sectnum_xform' is False, the 'sectnum' directive triggers
    section numbering by LaTeX.
  - Use default font in admonitions and sidebar.
  - Align of image in a figure defaults to 'center'.
  - Bugfix: Newlines around targets and references prevent run-together
    paragraphs.
  - Fix internal hyperlinks.
  - Use class defaults for page margins ('typearea' now optional).
  - Float placement made configurable, default changed to "here definitely".
  - Typeset generic topic as "quote block with title".
  - Use template (file and configuration option).
  - In the default template, load cmap.sty (fix text extraction in PDF) and
    fixltx2e.sty (LaTeX patches, \textsubscript).
  - Render doctest blocks as literal blocks (fixes [ 1586058 ]).
  - Use `translate()` instead of repeated `replace()` calls for text encoding.
  - Hyperlinked footnotes and support for symbol footnotes and
    ``--footnote-references=brackets`` with ``--use-latex-footnotes``.
  - Complete pairs of binary options
    (``--figure-footnotes, --figure-citations, --link-stylesheet``,
    ``--use-docutils-toc, --use-docutils-docinfo, --topic-abstract``)
  - New defaults:
    - font-encoding: "T1" (formerly implicitly set by 'ae').
    - use-latex-toc: true (ToC with page numbers).
    - use-latex-footnotes: true (no mixup with figures).

* docutils/writers/manpage.py

  - Do not print version at document end, this is done by the viewer.
  - Do not print date at document end, this is done by the viewer.
  - Fix storage of docinfo fields for none standard fields.

* docutils/tools/rst2man.py


Release 0.5 (2008-06-25)
========================

* docutils/languages/he.py: Added to project: Hebrew mappings by
  Meir Kriheli.

* docutils/parsers/rst/languages/he.py: Added to project: Hebrew
  mappings by Meir Kriheli.

* docutils/frontend.py:

  - Configuration files are now assumed and required to be
    UTF-8-encoded.
  - Paths of applied configuration files are now recorded in the
    runtime setting `_config_files`_ (accessible via `dump_settings`_).
  - Added `strip_elements_with_classes`_ and `strip_classes`_ settings.

* docutils/io.py:

  - Added code to determine the input encoding from data: encoding
    declarations or the presence of byte order marks (UTF-8 & UTF-16).
  - Added support for IronPython 1.0.

* docutils/nodes.py:

  - Added `document.__getstate_()` method, for pickling.

* docutils/parsers/rst/states.py:

  - Allow ``+`` and ``:`` in reference names.
  - Unquoted targets beginning with an underscore (``.. __target:
    URI``) are no longer accepted.
  - Added support for multiple attributions in a physical block quote
    (indented text block), dividing it into multiple logical block
    quotes.
  - Added support for unicode bullets in bullet lists: "•", "‣", and
    "⁃".
  - Added support for new object-oriented directive interface,
    retaining compatibility to the old functional interface.
  - Added support for throwing `DirectiveError`'s from within
    directive code.

* docutils/parsers/rst/__init__.py:

  - Added `Directive` base class.
  - Added `DirectiveError` base class.
  - Fixed `file_insertion_enabled`_ & `raw_enabled`_ setting
    definitions.

* docutils/parsers/directives/:

  - Refactored all reStructuredText directives to use the new
    object-oriented directive interface.  Errors are now (mostly)
    thrown using the new `DirectiveError` class.

* docutils/parsers/directives/misc.py:

  - Added ``start-after`` and ``end-before`` options to ``include``
    directive; thanks to Stefan Rank.

* docutils/transforms/universal.py:

  - Added `StripClassesAndElements` transform to remove from the
    document tree all elements with classes in
    `strip_elements_with_classes`_ and all "classes"
    attribute values in `strip_classes`_

* docutils/transforms/writer_aux.py:

  - Added `Admonitions` transform to transform specific admonitions
    (like "note", "warning", etc.) into generic admonitions with a
    localized title.

* docutils/writers/html4css1/__init__.py:

  - Moved template functionality from the PEP/HTML writer here.
  - Expanded the fragments available in the ``parts`` attribute.
  - Moved ``id`` attributes from titles to surrounding ``div``
    elements.
  - Dropped all ``name`` attributes of ``a`` elements (``id`` is
    universally supported now).
  - ``template.txt`` is now opened in text mode instead of binary mode
    (to ensure Windows compatibility).
  - ``a`` elements now have an "internal" or "external" class,
    depending on reference type.

* docutils/writers/html4css1/template.txt: Added to project.

* docutils/writers/pep_html/:

  - Moved template functionality to the HTML writer.

* docutils/writers/s5_html/__init__.py:

  - Added `view_mode`_ & `hidden_controls`_ settings.

* docutils/writers/latex2e/__init__.py:

  - Add `literal_block_env`_.
  - Fix: escaping ``%`` in href urls.
  - Move usepackage hyperref after stylesheet inclusion.
  - Fix: scrartcl does not have chapter but scrreprt.
  - Add newline after ``\end{verbatim}``.
  - Merge smaller differences from latex2e_adaptive_preamble.
  - Add ``use-part-section``.
  - Put leavevmode before longtable to avoid having it moved before sub/pargraph.
  - Using leavemode option_list no longer needs to check if parent
    is a definition list.
  - Append ``\leavemode`` to definition list terms.
  - No longer write visit\_/depart_definition_list_item comments to
    output.
  - Table column width with 3 decimal places.
  - Add table stubs support (boldfont).
  - Add assemble_parts to writer.
  - Add simply support for nested tables.
  - Fix verbatim in tables if use-verbatim-when-possible.
  - Use section commands down to subparagraph.
  - Put ensuremath around some latin1 chars.
  - Set ``usepackage[utf8x]{inputenc}`` for utf-8.
  - New experimental setting `use_bibtex`_.
  - New setting `reference_label`_ to allow usage of LaTeX ref for
    labels in section references.
  - Add a label after every section to support sectionnumbers as reference
    labels.
  - Fix: bug# 1605376 rst2latex: bad options group list
  - Remove inactive code for use_optionlist_for_option_list.
  - Remove latex comments from option_list output.
  - Fix: bug# 1612270 double quotes in italian literal.
  - Fix: output ``hypertarget{ node.get(refid) }{}`` from visit_target.
  - Add setting `use_latex_abstract`_.
  - Image width unit ``px`` is translated to ``pt``.
  - Add image height support.
  - Fix: image width ``70%`` is converted ``0.700\linewidth``.
    bug #1457388
  - Fix: Do not escape underscores in citation reference labels if
    use-latex-citations is set.
  - Use centering instead of center for figure contents, to avoid vertical
    space.
  - Recognize table class: borderless, nolines, booktabs, standard.
  - Fix: Renaming contents section does not work with latex writer; SF
    bug #1487405.
  - Applied patch for custom roles with classes from Edward Loper.
  - Fixed bug that caused crashes with more than 256 lists.

* docutils/writers/pep_html/__init__.py:

  - Changed to support new python.org website structure and
    pep2pyramid.py.

* docs/howto/security.txt: "Deploying Docutils Securely", added to
  project.

* tools/buildhtml.py:

  - Add `ignore`_ setting to exclude a list of shell patterns
    (default: ``.svn:CVS``).

* tools/editors/emacs/rst.el:

  - Changed license to "GPL".
  - Added ``rst-straighten-decorations`` function.
  - The ``compile`` module is now always loaded.
  - Added ``rst-toggle-line-block`` function.
  - Headings consisting only of non-ASCII characters are now
    recognized by ``rst-toc`` and ``rst-adjust``.
  - Added font-lock support for multi-line comments where the first
    comment line is empty.
  - Added ``(require 'font-lock)``.

* setup.py:

  - Provide descriptive error message if distutils is missing.


Release 0.4 (2006-01-09)
========================

* General:

  - Updated the project policies for trunk/branch development &
    version numbering.

* docutils/__init__.py:

  - Added ``__version_details__`` attribute to describe code source
    (repository/snapshot/release).
  - Replaced ``default_transforms`` attribute of ``TransformSpec`` with
    ``get_transforms()`` method.

* docutils/core.py:

  - Added ``publish_doctree`` and ``publish_from_doctree`` convenience
    functions, for document tree extraction and reprocessing.

* docutils/io.py:

  - Added ``DocTreeInput`` class, for reprocessing existing documents.
  - Added support for non-Unicode (e.g. binary) writer output.

* docutils/nodes.py:

  - Re-introduced ``Targetable.indirect_reference_name``, for
    MoinMoin/reST compatibility (removed in r3124/r3129).
  - Added ``serial_escape`` function; escapes string values that are
    elements of a list, for serialization.  Modified Docutils-XML
    writing (``Element._dom_node``) and pseudo-XML writing
    (``Element.starttag``) to use ``serial_escape``.
  - Added ``Node.deepcopy()`` method.
  - Removed the internal lists ``document.substitution_refs``,
    ``document.anonymous_refs``, and ``document.anonymous_targets``.
  - Added a "container" element.
  - Fixed bug where values of list-valued attributes of elements
    originating from custom interpreted text roles (i.e., with custom
    classes) were being shared between element instances.  Reported by
    Shmuel Zeigerman.

* docutils/statemachine.py:

  - Added trailing whitespace stripping to ``string2lines()``.
  - Added ``StringList.pad_double_width()`` & ``.replace()`` for East
    Asian double-width character support.

* docutils/utils.py:

  - Added ``east_asian_column_width()`` for double-width character
    support.

* docutils/languages/ja.py: Added to project: Japanese mappings by
  Hisashi Morita.

* docutils/languages/zh_cn.py: Added to project: Simplified Chinese
  mappings by Panjunyong.

* docutils/parsers/null.py: Added to project; a do-nothing parser.

* docutils/parsers/rst/__init__.py:

  - Added validator to "tab_width" setting, with test.  Closes SF bug
    #1212515, report from Wu Wei.

* docutils/parsers/rst/states.py:

  - Fixed bug with escaped colons indicating a literal block.
  - Fixed bug with enumerated lists (SF#1254145).
  - Backslash-escaped colons inside of field names are now allowed.
  - Targets (implicit and explicit), anonymous hyperlink references
    and auto-numbered footnote references inside of substitution
    definitions are now disallowed.
  - Fixed bug: list items with blank first lines.
  - Fixed bug: block quote attributions with indented second lines.
  - Added East Asian double-width character support (Python 2.4 only).

* docutils/parsers/rst/tableparser.py:

  - Added East Asian double-width character support (Python 2.4 only).

* docutils/parsers/rst/directives/body.py:

  - Added the "container" directive.

* docutils/parsers/rst/directives/misc.py:

  - Added the "default-role", "title", and "date" directives.
  - Added standard data file syntax to the "include" directive.
  - Added support for "class" directive content.

* docutils/parsers/rst/directives/images.py:

  - Added ``indirect_reference_name`` support for images with a target
    option.
  - Added support for image width and height units.
  - Fixed bug with image "target" options.

* docutils/parsers/rst/directives/references.py:

  - Added "class" attribute to "target-notes" directive, for
    footnote_reference classes.

* docutils/parsers/rst/include/: Directory added to project; contains
  standard data files for the "include" directive.  Initial contents:
  character entity substitution definition sets, and a set of
  definitions for S5/HTML presentations.

* docutils/parsers/rst/languages/ja.py: Added to project: Japanese
  mappings by David Goodger.

* docutils/parsers/rst/languages/zh_cn.py: Added to project:
  Simplified Chinese mappings by Panjunyong.

* docutils/readers/__init__.py:

  - Added universal.Decorations and universal.ExposeInternals
    transforms as default transforms for all readers.
  - Added ``ReReader`` base class for readers that reread an existing
    document tree.

* docutils/readers/doctree.py: Added to project; a reader for existing
  document trees.

* docutils/transforms/frontmatter.py:

  - Fixed the DocInfo transform to handle SVN-style expansion of the
    "Date" keyword.
  - In ``DocInfo.extract_authors``, treat the contents of "authors"
    fields uniformly.

* docutils/transforms/misc.py:

  - Added misc.Transitions transform, extracted from
    universal.FinalChecks.

* docutils/transforms/references.py:

  - Added references.DanglingReferences transform, extracted from
    universal.FinalChecks.
  - Fixed bug with doubly-indirect substitutions.
  - Added footnote_reference classes attribute to "TargetNotes".
  - Fixed bug with circular substitution definitions that put Docutils
    into an infinite loop.

* docutils/transforms/universal.py:

  - Added universal.ExposeInternals transform, extracted from
    universal.FinalChecks.
  - Removed universal.FinalChecks transform (logic has been moved to
    several new transforms).
  - Fixed bug with the "expose_internals" setting and Text nodes
    (exposed by the "rawsource" internal attribute).
  - Added the universal.StripComments transform, implementation of the
    "strip_comments" setting.

* docutils/transforms/writer_aux.py: Added to project; auxiliary
  transforms for writers.

  - Added ``Compound`` transform, which flattens compound paragraphs.

* docutils/writers/: Several writer modules (html4css1.py) were
  converted into packages.  Support modules and data files have been
  moved into the packages.  The stylesheets for the HTML writers are
  now installed along with the code, the code knows where to find
  them, and the default is to use them (actually, to embed them).
  Some adjustments to configuration files may be necessary.  The
  easiest way to obtain the new default behavior is to remove all
  settings whose name includes "stylesheet".

* docutils/writers/__init__.py:

  - Added universal.Messages and universal.FilterMessages transforms
    as default transforms for all writers.
  - Added ``UnfilteredWriter`` base class for writers that pass the
    document tree on unchanged.

* docutils/writers/docutils_xml.py:

  - Made ``xmlcharrefreplace`` the default output encoding error
    handler.

* docutils/writers/html4css1/:

  - Added support for image width and height units.
  - Made ``xmlcharrefreplace`` the default output encoding error
    handler.
  - Made ``--embed-stylesheet`` the default rather than
    ``--link-stylesheet``.
  - Moved "id" attribute from container (section etc.) to title's <a>
    tag, to be on the same tag as "name".
    (!!! To be reverted in Docutils 0.5.)
  - Added vertical space between fields of field lists.
  - Added ``--compact-field-lists`` option to remove vertical space in
    simple field lists.
  - Made cloaking of email addresses with ``--cloak-email-addresses``
    less obtrusive.
  - Fixed support for centered images.
  - Added support for class="compact" & class="open" lists.

* docutils/writers/latex2e/:

  - Underscores in citekeys are no longer escaped.

* docutils/writers/newlatex2e/unicode_map.py: Added to project;
  mapping of Unicode characters to LaTeX equivalents.

* docutils/writers/s5_html/: Package added to project; writer for
  S5/HTML slide shows.

* docs/dev/distributing.txt: Added to project; guide for distributors
  (package maintainers).

* docs/dev/hacking.txt: Added to project; guide for developers.

* docs/ref/doctree.txt:

  - Updated for plural attributes "classes", "ids", "names",
    "dupnames".
  - Added the "container" element.

* docs/ref/docutils.dtd:

  - Updated for plural attributes "classes", "ids", "names",
    "dupnames".

* docs/user/emacs.txt: Added to project; a document about Emacs
  support for reStructuredText and Docutils.

* docs/user/links.txt: Added to project; lists of Docutils-related
  links.

* docs/user/mailing-lists.txt: Added to project; information about
  Docutils-related mailing lists and how to access them.

* docs/user/slide-shows.txt: Added to project; example of and docs for
  the S5/HTML writer (``rst2s5.py`` front end).

* docs/ref/rst/definitions.txt: "reStructuredText Standard Definition
  Files", added to project.

* test/coverage.sh: Added to project; test coverage script.

* test/DocutilsTestSupport.py:

  - Added support for specifying runtime settings at the suite level.

* test/test_functional.py:

  - Added the ``clear_output_directory`` function.
  - Added support for ``_test_more`` functions in functional test
    config files.

* tools/rst2s5.py: Added to project; front end for the S5/HTML writer.

* tools/rstpep2html.py: Renamed from pep.py.

* tools/dev/create_unimap.py: Added to project; script to create the
  docutils/writers/unimap_latex.py mapping file.

* tools/dev/profile_docutils.py: Added to project; profiler script.

* tools/dev/unicode2rstsubs.py: Moved from tools/unicode2rstsubs.py.

* tools/editors/emacs/restructuredtext.el,
  tools/editors/emacs/rst-html.el, tools/editors/emacs/rst-mode.el:
  Removed from project; the functionality is now contained in rst.el.

* tools/editors/emacs/rst.el: Added to project.  Added many features
  and fixed many bugs.  See docs/user/emacs.txt for details.

* tools/stylesheets: Removed from project.  Stylesheets have been
  renamed and moved into writer packages.


Release 0.3.9 (2005-05-26)
==========================

* General:

  - Eliminated and replaced all uses of the old string attributes
    ``id``, ``name``, ``dupname`` and ``class`` with references to the
    new list attributes ``ids``, ``names``, ``dupnames`` and
    ``classes`` throughout the whole source tree.

* docutils/core.py:

  - Enabled ``--dump-*`` options when ``--traceback`` specified,
    allowing for easier debugging.
  - In ``Publisher.publish()``, expanded the generic top-level
    exception catching.

* docutils/examples.py:

  - Added ``internals`` function for exploration.

* docutils/io.py:

  - Fixed ``Input.decode`` method to apply heuristics only if no
    encoding is explicitly given, and to provide better reporting of
    decoding errors.
  - The ``Input.decode`` method now removes byte order marks (BOMs)
    from input streams.

* docutils/nodes.py:

  - ``image`` element class changed to subclass of Element, not
    TextElement (it's an empty element, and cannot contain text).
  - Added ``attr_defaults`` dictionary for default attribute values.
  - Added empty list as default value for the following attributes:
    ``ids``, ``names``, ``dupnames``, ``classes``, and ``backrefs``.
  - Added ``document.decoration`` attribute,
    ``document.get_decoration`` method, and ``decoration.get_header``
    & ``.get_footer`` methods.
  - Added ``Element.update_basic_atts()`` and ``Element.substitute()``
    methods.

* docutils/utils.py:

  - Removed ``docutils.utils.Reporter.categories``,
    ``docutils.utils.ConditionSet``, and all references to them, to
    simplify error reporting.

* docutils/languages/nl.py: Added to project; Dutch mappings by
  Martijn Pieters.

* docutils/parsers/rst/__init__.py:

  - Added settings: ``file_insertion_enabled`` & ``raw_enabled``.

* docutils/parsers/rst/states.py:

  - Added check for escaped at-mark to prevent email address recognition.
  - Fixed option lists to allow spaces inside ``<angle-bracketed option
    arguments>``.
  - Allowed whitespace in paths and URLs.
  - Added auto-enumerated list items.
  - Fixed bug that assumed ``.. _`` and ``.. |`` were invariably
    followed by text.
  - Added support for table stub columns.

* docutils/parsers/rst/directives/__init__.py:

  - Allowed whitespace in paths (``path`` function).
  - Added ``uri`` directive option conversion function.

* docutils/parsers/rst/directives/body.py:

  - Fixed illegal context bug with "topic" directive (allowed within
    sidebars; not within body elements).

* docutils/parsers/rst/directives/images.py:

  - Allowed whitespace (stripped) in "image" & "figure" directive URLs.
  - Added support for the ``file_insertion_enabled`` setting in the
    "figure" directive (disables "figwidth" option).
  - "image" directive: added checks for valid values of "align" option,
    depending on context.  "figure" directive: added specialized
    "align" option and attribute on "figure" element.
  - Made ":figwidth: image" option of "figure" directive work again.
  - Fixed bug with reference names containing uppercase letters
    (e.g. ``Name_``) in "target" option of "image" directive.

* docutils/parsers/rst/directives/misc.py:

  - Fixed "include" and "raw" directives to catch text decoding
    errors.
  - Allowed whitespace in "include" & "raw" directive paths.
  - Added support for ``file_insertion_enabled`` & ``raw_enabled``
    settings in "include" & "raw" directives.

* docutils/parsers/rst/directives/parts.py:

  - Added "header" & "footer" directives.
  - Fixed illegal context bug with "contents" directive (topics
    allowed within sidebars; not within body elements).

* docutils/parsers/rst/directives/tables.py:

  - Added "list-table" directive.
  - Caught empty CSV table bug.
  - Added support for the ``file_insertion_enabled`` setting in the
    "csv-table" directive.
  - Added ``stub-columns`` option to "csv-table" and "list-table"
    directives.

* docutils/parsers/rst/languages/nl.py: Added to project; Dutch
  mappings by Martijn Pieters.

* docutils/readers/standalone.py:

  - Added ``section_subtitles`` setting to activate or deactivate the
    ``SectSubTitle`` transform.

* docutils/transforms/frontmatter.py:

  - Added SectSubTitle transform to promote titles of lone
    subsections to subtitles.

* docutils/transforms/references.py:

  - Fixed mislocated internal targets bug, by propagating internal
    targets to the next node, making use of the newly added support
    for multiple names and IDs.
  - Fixed duplicate footnote label bug.
  - Replaced ``ChainedTargets`` with more generic ``PropagateTargets``
    transform.

* docutils/writers/html4css1.py:

  - Fixed unencoded stylesheet reference bug (characters like "&" in
    stylesheet references).
  - ``target`` nodes now appear as ``span`` tags (instead of ``a``
    tags).
  - Added support for multiple IDs per node by creating empty ``span``
    tags.
  - Added the ``field_name_limit`` & ``option_limit`` settings &
    support.
  - Added support for table stub columns.
  - Added support for the ``align`` attribute on ``figure`` elements.
  - Added the ``cloak_email_addresses`` setting & support.
  - Added ``html_prolog``, ``html_head``, ``html_body``,
    ``html_title``, & ``html_subtitle`` to parts dictionary exposed by
    ``docutils.core.publish_parts``.
  - Added support for section subtitles.

* docutils/writers/latex2e.py:

  - Fixed tables starting with more than one multirow cell.
  - Improved ``--use-latex-docinfo`` so that organization/contact/address
    fields are lumped with the last author field and appear on the
    titlepage.
  - Made sure the titlepage is always shown with ``--use-latex-docinfo``,
    even if the document has no title.
  - Made sure that latex doesn't fill in today's date if no date field
    was given.
  - Added support for section subtitles.

* docutils/writers/newlatex2e.py: Added to project; a new LaTeX writer
  (under development).

* docutils/writers/null.py: Added to project; a do-nothing Writer.

* docs/api/publisher.txt:

  - Added "``publish_parts`` Details" section.

* docutils/dev/repository.txt: Added to project; information about the
  Docutils Subversion repository.

* docs/ref/docutils.dtd:

  - Added a ``stub`` attribute to the ``colspec`` element via the
    ``tbl.colspec.att`` parameter entity.
  - Allowed topic elements within sidebars
  - Added an ``align`` attribute to the ``figure`` element.

* tools/rst2newlatex.py: Added to project; front end for the new LaTeX
  writer.


Release 0.3.7 (2004-12-24)
==========================

* docutils/frontend.py:

  - Added options: ``--input-encoding-error-handler``,
    ``--record-dependencies``, ``--leave-footnote-reference-space``,
    ``--strict-visitor``.
  - Added command-line and config file support for "overrides" setting
    parameter.

* docutils/io.py:

  - Added support for input encoding error handler.

* docutils/nodes.py:

  - Added dispatch_visit and dispatch_departure methods to
    NodeVisitor; useful as a hook for Visitors.
  - Changed structure of ``line_block``; added ``line``.
  - Added ``compound`` node class.
  - Added a mechanism for Visitors to transitionally ignore new node
    classes.

* docutils/utils.py:

  - Moved ``escape2null`` and ``unescape`` functions from
    docutils/parsers/rst/states.py.

* docutils/parsers/rst/roles.py:

  - Added "raw" role.
  - Changed role function API: the "text" parameter now takes
    null-escaped interpreted text content.

* docutils/parsers/rst/states.py:

  - Fixed bug where a "role" directive in a nested parse would crash
    the parser; the state machine's "language" attribute was not being
    copied over.
  - Added support for line block syntax.
  - Fixed directive parsing bug: argument-less directives didn't
    notice that arguments were present.
  - Removed error checking for transitions.
  - Added support for multiple classifiers in definition list items.
  - Moved ``escape2null`` and ``unescape`` functions to docutils/utils.py.
  - Changed role function API: the "text" parameter now takes
    null-escaped interpreted text content.
  - Empty sections and documents are allowed now.

* docutils/parsers/rst/directives/__init__.py:

  - Added ``encoding`` directive option conversion function.
  - Allow multiple class names in class_option conversion function.

* docutils/parsers/rst/directives/body.py:

  - Converted the line-block directive to use the new structure.
  - Extracted the old line-block functionality to the ``block``
    function (still used).
  - Added ``compound`` directive (thanks to Lea Wiemann).

* docutils/parsers/rst/directives/misc.py:

  - Added "encoding" option to "include" and "raw" directives.
  - Added "trim", "ltrim", and "rtrim" options to "unicode" directive.
  - Allow multiple class names in the "class" directive.

* docutils/parsers/rst/directives/parts.py:

  - Directive "sectnum" now accepts "prefix", "suffix", and "start"
    options.  Thanks to Lele Gaifax.

* docutils/parsers/rst/directives/tables.py:

  - Added "encoding" directive to "csv-table" directive.
  - Added workaround for lack of Unicode support in csv.py, for
    non-ASCII CSV input.

* docutils/transforms/misc.py:

  - Fixed bug when multiple "class" directives are applied to a single
    element.
  - Enabled multiple format names for "raw" directive.

* docutils/transforms/references.py:

  - Added support for trimming whitespace from beside substitution
    references.

* docutils/transforms/universal.py:

  - FinalChecks now checks for illegal transitions and moves
    transitions between sections.

* docutils/writers/html4css1.py:

  - HTMLTranslator.encode now converts U+00A0 to "&nbsp;".
  - "stylesheet" and "stylesheet_path" settings are now mutually
    exclusive.
  - Added support for the new line_block/line structure.
  - ``--footnote-references`` now overrides
    ``--trim-footnote-reference-space``, if applicable.
  - Added support for ``compound`` elements.
  - Enabled multiple format names for "raw" directive.
  - ``<p>`` tags of a paragraph which is the only visible child of the
    document node are no longer stripped.
  - Moved paragraph-compacting logic (for stripping ``<p>`` tags) to
    new method ``should_be_compact_paragraph()``.
  - Added class="docutils" to ``dl``, ``hr``, ``table`` and ``tt``
    elements.
  - "raw" elements are now surrounded by ``span`` or ``div`` tags in
    the output if they have their ``class`` attribute set.
  - The whole document is now surrounded by a ``<div
    class="document">`` element.
  - Body-level images are now wrapped by their own ``<div>`` elements,
    with image classes copied to the wrapper, and for images which
    have the ``:align:`` option set, the surrounding ``<div>`` now
    receives a class attribute (like ``class="align-left"``).

* docutils/writers/latex2e.py:

  - no newline after depart_term.
  - Added translations for some Unicode quotes.
  - Added option "font-encoding", made package AE the default.
  - `stylesheet`_ and `stylesheet_path`_ settings are now mutually
    exclusive.
  - ``--footnote-references`` now overrides
    ``--trim-footnote-reference-space``, if applicable.
  - The footnote label style now matches the footnote reference style
    ("brackets" or "superscript").
  - Added support for ``compound`` elements.
  - Enabled multiple format names for "raw" directive.

* docs/ref/docutils.dtd:

  - Changed structure of the ``line_block`` element; added ``line``.
  - Added ``compound`` element.
  - Added "ltrim" and "rtrim" attributes to
    ``substitution_definition`` element.
  - Enabled multiple format names for ``raw`` element.
  - Enabled multiple classifiers in ``definition_list_item`` elements.

* docs/ref/rst/directives.txt

  - Marked "line-block" as deprecated.
  - "Class" directive now allows multiple class names.
  - Added "Rationale for Class Attribute Value Conversion".
  - Added warning about "raw" overuse/abuse.

* docs/ref/rst/restructuredtext.txt:

  - Added syntax for line blocks.
  - Definition list items may have multiple classifiers.

* docs/ref/rst/roles.txt:

  - Added "raw" role.

* tools/stylesheets/default.css:

  - Added support for the new line_block structure.
  - Added "docutils" class to ``dl``, ``hr``, ``table`` and ``tt``.


Release 0.3.5 (2004-07-29)
==========================

General:

* _`Documentation cleanup/reorganization`.

  - Created new subdirectories of docs/:

    * ``docs/user/``: introductory/tutorial material for end-users
    * ``docs/dev/``: for core-developers (development notes, plans, etc.)
    * ``docs/api/``: API reference material for client-developers
    * ``docs/ref/``: reference material for all groups
    * ``docs/howto/``: for component-developers and core-developers
    * ``docs/peps/``: Python Enhancement Proposals

  - Moved ``docs/*`` to ``docs/user/``.
  - Moved ``pysource.dtd``, ``pysource.txt``, ``semantics.txt`` from
    ``spec/`` to ``docs/dev``.
  - Moved ``doctree.txt``, ``docutils.dtd``, ``soextblx.dtd``,
    ``transforms.txt`` from ``spec/`` to ``docs/ref/``.
  - Moved ``alternatives.txt``, and ``problems.txt`` from
    ``spec/rst/`` to ``docs/dev/rst/``.
  - Moved ``reStructuredText.txt``, ``directives.txt``,
    ``interpreted.txt``, and ``introduction.txt`` from ``spec/rst/``
    to ``docs/ref/rst/``.  Renamed ``interpreted.txt`` to
    ``roles.txt``, ``reStructuredText.txt`` to
    ``restructuredtext.txt``.
  - Moved ``spec/howto/`` to ``docs/howto``.

  In order to keep the CVS history of moved files, we supplied
  SourceForge with a script for modifying the Docutils CVS repository.

  After running the cleanup script:

  - Added ``docs/index.txt``.
  - Added a ``.htaccess`` file to the ``web`` module, containing
    redirects for all old paths to new paths.  They'll preserve
    fragments (the "#name" part of a URL), and won't clutter up the
    file system, and will correct the URL in the user's browser.
  - Added ``BUGS.txt``, ``docs/dev/policies.txt``,
    ``docs/dev/website.txt``, ``docs/dev/release.txt`` from all but
    the "To Do" list itself in ``docs/dev/todo.txt``.
  - Moved "Future Plans" from ``HISTORY.txt`` to new "Priorities"
    section of ``docs/dev/todo.txt``.
  - Added ``THANKS.txt`` from "Acknowledgements" in ``HISTORY.txt``.
  - Added "How To Report Bugs" to ``BUGS.txt``.
  - Went through all the sources and docs (including under web/) and
    updated links.  Mostly done by Lea Wiemann; thanks Lea!
    (Still need to update links in the sandboxes.)

Specific:

* BUGS.txt: Added to project.

* THANKS.txt: Added to project.

* docutils/__init__.py:

  - 0.3.4: Post-release.

* docutils/core.py:

  - Added special error handling & advice for UnicodeEncodeError.
  - Refactored Publisher.publish (simplified exception handling &
    extracted debug dumps).
  - Renamed "enable_exit" parameter of convenience functions to
    "enable_exit_status".
  - Enabled traceback (exception propagation) by default in
    programmatic convenience functions.
  - Now publish_file and publish_cmdline convenience functions return
    the encoded string results in addition to their regular I/O.
  - Extracted common code from publish_file, publish_string, and
    publish_parts, into new publish_programmatically.  Extracted
    settings code to ``Publisher.process_programmatic_settings``.
  - In Publisher.publish, disabled ``settings_overrides`` when
    ``settings`` is supplied; redundant.

* docutils/frontend.py:

  - Added help text for ``--output-encoding-error-handler`` and
    ``--error-encoding-error-handler``.
  - Renamed ``--exit`` to ``--exit-status``.
  - Simplified default-setting code.

* docutils/parsers/rst/__init__.py:

  - Added ``--pep-base-url`` and ``--rfc-base-url`` options.

* docutils/parsers/rst/states.py:

  - Made URI recognition more aggressive and intelligent.

* docutils/parsers/rst/directives/__init__.py:

  - Added several directive option conversion functions.

* docutils/parsers/rst/directives/body.py:

  - Moved "table" directive to tables.py.

* docutils/parsers/rst/directives/tables.py: Table-related directives,
  added to project.

* docutils/writers/latex2e.py:

  - Added ``--table-style=(standard|booktabs|nolines)``
  - figures get "here" option (LaTeX per default puts them at bottom),
    and figure content is centered.
  - Rowspan support for tables.
  - Fix: admonition titles before first section.
  - Replace ``--`` in literal by ``-{}-`` because fontencoding T1 has endash.
  - Replave ``_`` in literal by an underlined blank, because it has the correct
    width.
  - Fix: encode pdfbookmark titles, ``#`` broke pdflatex.
  - A few unicode replacements, if output_encoding != utf
  - Add `graphicx_option`_ setting.
  - Indent literal-blocks.
  - Fix: omit ``\maketitle`` when there is no document title.

* docs/index.txt: "Docutils Project Documentation Overview", added to
  project.

* docs/api/cmdline-tool.txt: "Inside A Docutils Command-Line Front-End
  Tool", added to project.

* docs/api/publisher.txt: "The Docutils Publisher", added to project.

* docs/api/runtime-settings.txt: "Docutils Runtime Settings", added to project.

* docs/dev/policies.txt: Added to project (extracted from
  ``docs/dev/todo.txt``, formerly ``spec/notes.txt``).

* docs/dev/release.txt: Added to project (extracted from
  ``docs/dev/todo.txt``, formerly ``spec/notes.txt``).

* docs/dev/testing.txt: Added to project.

* docs/dev/website.txt: Added to project (extracted from
  ``docs/dev/todo.txt``, formerly ``spec/notes.txt``).

* docs/ref/rst/directives.txt:

  - Added directives: "table", "csv-table".

* docs/user/rst/cheatsheet.txt: "The reStructuredText Cheat Sheet"
  added to project.  1 page for syntax, and a 1 page reference for
  directives and roles.  Source text to be used as-is; not meant to be
  converted to HTML.

* docs/user/rst/demo.txt: Added to project; moved from tools/test.txt
  with a change of title.

* test/functional/, contents, and test/test_functional.py: Added to
  project.

* tools/buildhtml.py: Fixed bug with config file handling.

* tools/html.py: Removed from project (duplicate of rst2html.py).

* tools/pep2html.py: Removed from project (duplicate of Python's
  nondist/peps/pep2html.py; Docutils' tools/pep.py can be used for
  Docutils-related PEPs in docs/peps/).

* tools/rst2pseudoxml.py: Renamed from publish.py.

* tools/rst2xml.py: Renamed from docutils-xml.py.

* tools/test.txt: Removed from project; moved to
  docs/user/rst/demo.txt.

* setup.py: Now also installs ``rst2latex.py``.


Release 0.3.3 (2004-05-09)
==========================

* docutils/__init__.py:

  - 0.3.1: Reorganized config file format (multiple sections); see
    docs/config.txt.
  - Added unknown_reference_resolvers attribute to TransformSpec.
  - 0.3.2: Interpreted text reorganization.
  - 0.3.3: Released.

* docutils/core.py:

  - Catch system messages to stop tracebacks from parsing errors.
  - Catch exceptions during processing report & exit without
    tracebacks, except when ``--traceback`` used.
  - Reordered components for OptionParser; application comes last.
  - Added "config_section" parameter to several methods and functions,
    allowing front ends to easily specify their config file sections.
  - Added publish_parts convenience function to allow access to individual
    parts of a document.

* docutils/examples.py: Added to project; practical examples of
  Docutils client code, to be used as-is or as models for variations.

* docutils/frontend.py:

  - Added "traceback" setting.
  - Implemented support for config file reorganization:
    ``standard_config_files`` moved from ``ConfigParser`` to
    ``OptionParser``; added
    ``OptionParser.get_config_file_settings()`` and
    ``.get_standard_config_settings()``; support for old "[options]"
    section (with deprecation warning) and mapping from old to new
    settings.
  - Reimplemented setting validation.
  - Enabled flexible boolean values: yes/no, true/false, on/off.
  - Added ``Values``, a subclass of ``optparse.Values``, with support
    for list setting attributes.
  - Added support for new ``DOCUTILSCONFIG`` environment variable;
    thanks to Beni Cherniavsky.
  - Added ``--no-section-numbering`` option.

* docutils/io.py:

  - Catch IOErrors when opening source & destination files, report &
    exit without tracebacks.  Added ``handle_io_errors`` parameter to
    ``FileInput`` & ``FileOutput`` to enable caller error handling.

* docutils/nodes.py:

  - Changed ``SparseNodeVisitor`` and ``GenericNodeVisitor`` dynamic
    method definitions (via ``exec``) to dynamic assignments (via
    ``setattr``); thanks to Roman Suzi.
  - Encapsulated visitor dynamic assignments in a function; thanks to
    Ian Bicking.
  - Added indirect_reference_name attribute to the Targetable
    class. This attribute holds the whitespace_normalized_name
    (contains mixed case) of a target.

* docutils/statemachine.py:

  - Renamed ``StringList.strip_indent`` to ``.trim_left``.
  - Added ``StringList.get_2D_block``.

* docutils/utils.py:

  - Added "level" attribute to SystemMessage exceptions.

* docutils/languages/af.py: Added to project; Afrikaans mappings by
  Jannie Hofmeyr.

* docutils/languages/cs.py: Added to project; Czech mappings by Marek
  Blaha.

* docutils/languages/eo.py: Added to project; Esperanto mappings by
  Marcelo Huerta San Martin.

* docutils/languages/pt_br.py: Added to project; Brazilian Portuguese
  mappings by Lalo Martins.

* docutils/languages/ru.py: Added to project; Russian mappings by
  Roman Suzi.

* docutils/parsers/rst/roles.py: Added to project.  Contains
  interpreted text role functions, a registry for interpreted text
  roles, and an API for adding to and retrieving from the registry.
  Contributed by Edward Loper.

* docutils/parsers/rst/states.py:

  - Updated ``RSTState.nested_parse`` for "include" in table cells.
  - Allowed true em-dash character and "``---``" as block quote
    attribution marker.
  - Added support for <angle-bracketed> complex option arguments
    (option lists).
  - Fixed handling of backslashes in substitution definitions.
  - Fixed off-by-1 error with extra whitespace after substitution
    definition directive.
  - Added inline markup parsing to field lists' field names.
  - Added support for quoted (and unindented) literal blocks.
    Driven in part by a bribe from Frank Siebenlist (thanks!).
  - Parser now handles escapes in URIs correctly.
  - Made embedded-URIs' reference text omittable.  Idea from Beni
    Cherniavsky.
  - Refactored explicit target processing code.
  - Added name attribute to references containing the reference name only
    through whitespace_normalize_name (no case changes).
  - parse_target no longer returns the refname after going through
    normalize_name. This is now handled in make_target.
  - Fixed bug relating to role-less interpreted text in non-English
    contexts.
  - Reorganized interpreted text processing; moved code into the new
    roles.py module.  Contributed by Edward Loper.
  - Refactored ``Body.parse_directive`` into ``run_directive`` and
    ``parse_directive_block``.

* docutils/parsers/rst/tableparser.py:

  - Reworked for ``StringList``, to support "include" directives in
    table cells.

* docutils/parsers/rst/directives/__init__.py:

  - Renamed ``unchanged()`` directive option conversion function to
    ``unchanged_required``, and added a new ``unchanged``.
  - Catch unicode value too high error; fixes bug 781766.
  - Beefed up directive error reporting.

* docutils/parsers/rst/directives/body.py:

  - Added basic "table" directive.

* docutils/parsers/rst/directives/images.py:

  - Added "target" option to "image" directive.
  - Added name attribute to references containing the reference name only
    through whitespace_normalize_name (no case changes).

* docutils/parsers/rst/directives/misc.py:

  - Isolated the import of the ``urllib2`` module; was causing
    problems on SourceForge (``libssl.so.2`` unavailable?).
  - Added the "role" directive for declaring custom interpreted text
    roles.

* docutils/parsers/rst/directives/parts.py:

  - The "contents" directive does more work up-front, creating the
    "topic" and "title", and leaving the "pending" node for the
    transform.  Allows earlier reference resolution; fixes subtle bug.

* docutils/parsers/rst/languages/af.py: Added to project; Afrikaans
  mappings by Jannie Hofmeyr.

* docutils/parsers/rst/languages/cs.py: Added to project; Czech
  mappings by Marek Blaha.

* docutils/parsers/rst/languages/eo.py: Added to project; Esperanto
  mappings by Marcelo Huerta San Martin.

* docutils/parsers/rst/languages/pt_br.py: Added to project; Brazilian
  Portuguese mappings by Lalo Martins.

* docutils/parsers/rst/languages/ru.py: Added to project; Russian
  mappings by Roman Suzi.

* docutils/transforms/parts.py:

  - The "contents" directive does more work up-front, creating the
    "topic" and "title", and leaving the "pending" node for the
    transform.  Allows earlier reference resolution; fixes subtle bug.
  - Added support for disabling of section numbering.

* docutils/transforms/references.py:

  - Verifying that external targets are truly targets and not indirect
    references. This is because we are now adding a "name" attribute to
    references in addition to targets. Note sure if this is correct!
  - Added code to hook into the unknown_reference_resolvers list for a
    transformer in resolve_indirect_target. This allows the
    unknown_reference_resolvers to keep around indirect targets which
    docutils doesn't know about.
  - Added specific error message for duplicate targets.

* docutils/transforms/universal.py:

  - Added FilterMessages transform (removes system messages below the
    verbosity threshold).
  - Added hook (via docutils.TransformSpec.unknown_reference_resolvers)
    to FinalCheckVisitor for application-specific handling of
    unresolvable references.
  - Added specific error message for duplicate targets.

* docutils/writers/__init__.py:

  - Added assemble_parts() method to the Writer class to allow for
    access to a documents individual parts.
  - Documented & set default for ``Writer.output`` attribute.

* docutils/writers/html4css1.py:

  - Fixed unicode handling of attribute values (bug 760673).
  - Prevent duplication of "class" attribute values (bug report from
    Kirill Lapshin).
  - Improved table grid/border handling (prompted by report from Bob
    Marshall).
  - Added support for table titles.
  - Added "<title />" for untitled docs, for XHTML conformance; thanks
    to Darek Suchojad.
  - Added functionality to keep track of individual parts of a document
    and store them in a dictionary as the "parts" attribute of the writer.
    Contributed by Reggie Dugard at the Docutils sprint at PyCon DC 2004.
  - Added proper support for the "scale" attribute of the "image"
    element.  Contributed by Brent Cook.
  - Added ``--initial-header-level`` option.
  - Fixed bug: the body_pre_docinfo segment depended on there being a
    docinfo; if no docinfo, the document title was incorporated into
    the body segment.  Adversely affected the publish_parts interface.

* docutils/writers/latex2e.py:

  - Changed default stylesheet to "no stylesheet" to avoid latex complaining
    about a missing file.
  - Added options and support: ``--compound-enumerators``,
    ``--section-prefix-for-enumerators``, and
    ``--section-enumerator-separator``.  By John F Meinel Jr (SF patch
    934322).
  - Added option ``--use-verbatim-when-possible``, to avoid
    problematic characters (eg, '~' in italian) in literal blocks.
  - It's now possible to use four section levels in the `book` and
    `report` LaTeX document classes.  The default `article` class still has
    three levels limit.

* docs/config.txt: "Docutils Configuration Files", added to project.
  Moved config file entry descriptions from tools.txt.

* docs/tools.txt:

  - Moved config file entry descriptions to config.txt.

* spec/notes.txt: Continual updates.  Added "Setting Up For Docutils
  Development".

* spec/howto/rst-roles.txt: "Creating reStructuredText Interpreted
  Text Roles", added to project.

* spec/rst/reStructuredText.txt:

  - Added description of support for <angle-bracketed> complex option
    arguments to option lists.
  - Added subsections for indented and quoted literal blocks.

* test: Continually adding & updating tests.

  - Added test/test_settings.py & test/data/config_*.txt support
    files.
  - Added test/test_writers/test_htmlfragment.py.

* test/DocutilsTestSupport.py:

  - Refactored LaTeX publisher test suite/case class names to make
    testing other writers easier.
  - Added HtmlWriterPublishTestCase and HtmlFragmentTestSuite classes
    to test the processing of HTML fragments which use the new
    publish_parts convenience function.

* tools/buildhtml.py:

  - Added support for the ``--prune`` option.
  - Removed dependency on pep2html.py; plaintext PEPs no longer
    supported.

* tools/docutils.conf:

  - Updated for configuration file reorganization.

* tools/rst2html.py:

  - copied from tools/html.py

* setup.py:

  - added a 'scripts' section to configuration
  - added 'tools/rst2html.py' to the scripts section


Release 0.3 (2003-06-24)
========================

General:

* Renamed "attribute" to "option" for directives/extensions.

* Renamed transform method "transform" to "apply".

* Renamed "options" to "settings" for runtime settings (as set by
  command-line options).  Sometimes "option" (singular) became
  "settings" (plural).  Some variations below:

  - document.options -> document.settings (stored in other objects as
    well)
  - option_spec -> settings_spec (not directives though)
  - OptionSpec -> SettingsSpec
  - cmdline_options -> settings_spec
  - relative_path_options -> relative_path_settings
  - option_default_overrides -> settings_default_overrides
  - Publisher.set_options -> Publisher.get_settings

Specific:

* COPYING.txt: Added "Public Domain Dedication".

* FAQ.txt: Frequently asked questions, added to project.

* setup.py:

  - Updated with PyPI Trove classifiers.
  - Conditional installation of third-party modules.

* docutils/__init__.py:

  - Bumped version to 0.2.1 to reflect changes to I/O classes.
  - Bumped version to 0.2.2 to reflect changes to stylesheet options.
  - Factored ``SettingsSpec`` out of ``Component``; separately useful.
  - Bumped version to 0.2.3 because of the new ``--embed-stylesheet``
    option and its effect on the PEP template & writer.
  - Bumped version to 0.2.4 due to changes to the PEP template &
    stylesheet.
  - Bumped version to 0.2.5 to reflect changes to Reporter output.
  - Added ``TransformSpec`` class for new transform system.
  - Bumped version to 0.2.6 for API changes (renaming).
  - Bumped version to 0.2.7 for new ``docutils.core.publish_*``
    convenience functions.
  - Added ``Component.component_type`` attribute.
  - Bumped version to 0.2.8 because of the internal parser switch from
    plain lists to the docutils.statemachine.StringList objects.
  - Bumped version to 0.2.9 because of the frontend.py API changes.
  - Bumped version to 0.2.10 due to changes to the project layout
    (third-party modules removed from the "docutils" package), and
    signature changes in ``io.Input``/``io.Output``.
  - Changed version to 0.3.0 for release.

* docutils/core.py:

  - Made ``publish()`` a bit more convenient.
  - Generalized ``Publisher.set_io``.
  - Renamed ``publish()`` to ``publish_cmdline()``; rearranged its
    parameters; improved its docstring.
  - Added ``publish_file()`` and ``publish_string()``.
  - Factored ``Publisher.set_source()`` and ``.set_destination()``
    out of ``.set_io``.
  - Added support for ``--dump-pseudo-xml``, ``--dump-settings``, and
    ``--dump-transforms`` hidden options.
  - Added ``Publisher.apply_transforms()`` method.
  - Added ``Publisher.set_components()`` method; support for
    ``publish_*()`` conveninece functions.
  - Moved config file processing to docutils/frontend.py.
  - Added support for exit status ("exit_level" setting &
    ``enable_exit`` parameter for Publisher.publish() and convenience
    functions).

* docutils/frontend.py:

  - Check for & exit on identical source & destination paths.
  - Fixed bug with absolute paths & ``--config``.
  - Set non-command-line defaults in ``OptionParser.__init__()``:
    ``_source`` & ``_destination``.
  - Distributed ``relative_path_settings`` to components; updated
    ``OptionParser.populate_from_components()`` to combine it all.
  - Require list of keys in ``make_paths_absolute`` (was implicit in
    global ``relative_path_settings``).
  - Added ``--expose-internal-attribute``, ``--dump-pseudo-xml``,
    ``--dump-settings``, and ``--dump-transforms`` hidden options.
  - Removed nasty internals-fiddling ``ConfigParser.get_section``
    code, replaced with correct code.
  - Added validation functionality for config files.
  - Added ``--error-encoding`` option/setting, "_disable_config"
    internal setting.
  - Added encoding validation; updated ``--input-encoding`` and
    ``--output-encoding``; added ``--error-encoding-error-handler`` and
    ``--output-encoding-error-handler``.
  - Moved config file processing from docutils/core.py.
  - Updated ``OptionParser.populate_from_components`` to handle new
    ``SettingsSpec.settings_defaults`` dict.
  - Added support for "-" => stdin/stdout.
  - Added "exit_level" setting (``--exit`` option).

* docutils/io.py:

  - Split ``IO`` classes into subclasses of ``Input`` and ``Output``.
  - Added automatic closing to ``FileInput`` and ``FileOutput``.
  - Delayed opening of ``FileOutput`` file until ``write()`` called.
  - ``FileOutput.write()`` now returns the encoded output string.
  - Try to get path/stream name automatically in ``FileInput`` &
    ``FileOutput``.
  - Added defaults for source & destination paths.
  - Allow for Unicode I/O with an explicit "unicode" encoding.
  - Added ``Output.encode()``.
  - Removed dependency on runtime settings; pass encoding directly.
  - Recognize Unicode strings in ``Input.decode()``.
  - Added support for output encoding error handlers.

* docutils/nodes.py:

  - Added "Invisible" element category class.
  - Changed ``Node.walk()`` & ``.walkabout()`` to permit more tree
    modification during a traversal.
  - Added element classes: ``line_block``, ``generated``, ``address``,
    ``sidebar``, ``rubric``, ``attribution``, ``admonition``,
    ``superscript``, ``subscript``, ``inline``
  - Added support for lists of nodes to ``Element.insert()``.
  - Fixed parent linking in ``Element.replace()``.
  - Added new abstract superclass ``FixedTextElement``; adds
    "xml:space" attribute.
  - Added support for "line" attribute of ``system_message`` nodes.
  - Added support for the observer pattern from ``utils.Reporter``.
    Added ``parse_messages`` and ``transform_messages`` attributes to
    ``document``, removed ``messages``.  Added ``note_parse_message``
    and ``note_transform_message`` methods.
  - Added support for improved diagnostics:

    - Added "document", "source", and "line" internal attributes to
      ``Node``, set by ``Node.setup_child()``.
    - Converted variations on ``node.parent = self`` to
      ``self.setup_child(node)``.
    - Added ``document.current_source`` & ``.current_line``
      attributes, and ``.note_source`` observer method.
    - Changed "system_message" output to GNU-Tools format.

  - Added a "rawsource" attribute to the ``Text`` class, for text
    before backslash-escape resolution.
  - Support for new transform system.
  - Reworked ``pending`` element.
  - Fixed XML DOM bug (SF #660611).
  - Removed the ``interpeted`` element class and added
    ``title_reference``, ``abbreviation``, ``acronym``.
  - Made substitutions case-sensitive-but-forgiving; moved some code
    from the parser.
  - Fixed Unicode bug on element attributes (report: William Dode).

* docutils/optik.py: Removed from project; replaced with
  extras/optparse.py and extras/textwrap.py.  These will be installed
  only if they're not already present in the Python installation.

* docutils/roman.py: Moved to extras/roman.py; this will be installed
  only if it's not already present in the Python installation.

* docutils/statemachine.py:

  - Factored out ``State.add_initial_transitions()`` so it can be
    extended.
  - Converted whitespace-specific "blank" and "indent" transitions
    from special-case code to ordinary transitions: removed
    ``StateMachineWS.check_line()`` & ``.check_whitespace()``, added
    ``StateWS.add_initial_transitions()`` method, ``ws_patterns`` &
    ``ws_initial_transitions`` attributes.
  - Removed ``State.match_transition()`` after merging it into
    ``.check_line()``.
  - Added ``StateCorrection`` exception.
  - Added support for ``StateCorrection`` in ``StateMachine.run()``
    (moved ``TransitionCorrection`` support there too.)
  - Changed ``StateMachine.next_line()`` and ``.goto_line()`` to raise
    ``EOFError`` instead of ``IndexError``.
  - Added ``State.no_match`` method.
  - Added support for the Observer pattern, triggered by input line
    changes.
  - Added ``strip_top`` parameter to
    ``StateMachineWS.get_first_known_indented``.
  - Made ``context`` a parameter to ``StateMachine.run()``.
  - Added ``ViewList`` & ``StringList`` classes;
    ``extract_indented()`` becomes ``StringList.get_indented()``.
  - Added ``StateMachine.insert_input()``.
  - Fixed ViewList slice handling for Python 2.3.  Patch from (and
    thanks to) Fred Drake.

* docutils/utils.py:

  - Added a ``source`` attribute to Reporter instances and
    ``system_message`` elements.
  - Added an observer pattern to ``utils.Reporter`` to keep track of
    system messages.
  - Fixed bugs in ``relative_path()``.
  - Added support for improved diagnostics.
  - Moved ``normalize_name()`` to nodes.py (``fully_normalize_name``).
  - Added support for encoding Reporter stderr output, and encoding
    error handlers.
  - Reporter keeps track of the highest level system message yet
    generated.

* docutils/languages: Fixed bibliographic field language lookups.

* docutils/languages/es.py: Added to project; Spanish mappings by
  Marcelo Huerta San Martin.

* docutils/languages/fr.py: Added to project; French mappings by
  Stefane Fermigier.

* docutils/languages/it.py: Added to project; Italian mappings by
  Nicola Larosa.

* docutils/languages/sk.py: Added to project; Slovak mappings by
  Miroslav Vasko.

* docutils/parsers/__init__.py:

  - Added ``Parser.finish_parse()`` method.

* docutils/parsers/rst/__init__.py:

  - Added options: ``--pep-references``, ``--rfc-references``,
    ``--tab-width``, ``--trim-footnote-reference-space``.

* docutils/parsers/rst/states.py:

  - Changed "title under/overline too short" system messages from INFO
    to WARNING, and fixed its insertion location.
  - Fixed enumerated list item parsing to allow paragraphs & section
    titles to begin with enumerators.
  - Converted system messages to use the new "line" attribute.
  - Fixed a substitution reference edge case.
  - Added support for ``--pep-references`` and ``--rfc-references``
    options; reworked ``Inliner`` code to make customization easier.
  - Removed field argument parsing.
  - Added support for short section title over/underlines.
  - Fixed "simple reference name" regexp to ignore text like
    "object.__method__"; not an anonymous reference.
  - Added support for improved diagnostics.
  - Reworked directive API, based on Dethe Elza's contribution.  Added
    ``Body.parse_directive()``, ``.parse_directive_options()``,
    ``.parse_directive_arguments()`` methods.
  - Added ``ExtensionOptions`` class, to parse directive options
    without parsing field bodies.  Factored
    ``Body.parse_field_body()`` out of ``Body.field()``, overridden in
    ``ExtensionOptions``.
  - Improved definition list term/classifier parsing.
  - Added warnings for unknown directives.
  - Renamed ``Stuff`` to ``Struct``.
  - Now flagged as errors: transitions at the beginning or end of
    sections, empty sections (except title), and empty documents.
  - Updated for ``statemachine.StringList``.
  - Enabled recognition of schemeless email addresses in targets.
  - Added support for embedded URIs in hyperlink references.
  - Added backslash-escapes to inline markup end-string suffix.
  - Added support for correct interpreted text processing.
  - Fixed nested title parsing (topic, sidebar directives).
  - Added special processing of backslash-escaped whitespace (idea
    from David Abrahams).
  - Made substitutions case-sensitive-but-forgiving; moved some code
    to ``docutils.nodes``.
  - Added support for block quote attributions.
  - Added a kludge to work-around a conflict between the bubble-up
    parser strategy and short titles (<= 3 char-long over- &
    underlines).  Fixes SF bug #738803 "infinite loop with multiple
    titles" submitted by Jason Diamond.
  - Added explicit interpreted text roles for standard inline markup:
    "emphasis", "strong", "literal".
  - Implemented "superscript" and "subscript" interpreted text roles.
  - Added initial support for "abbreviation" and "acronym" roles;
    incomplete.
  - Added support for ``--trim-footnote-reference-space`` option.
  - Optional space before colons in directives & hyperlink targets.

* docutils/parsers/rst/tableparser.py:

  - Fixed a bug that was producing unwanted empty rows in "simple"
    tables.
  - Detect bad column spans in "simple" tables.

* docutils/parsers/rst/directives: Updated all directive functions to
  new API.

* docutils/parsers/rst/directives/__init__.py:

  - Added ``flag()``, ``unchanged()``, ``path()``,
    ``nonnegative_int()``, ``choice()``, and ``class_option()``
    directive option helper functions.
  - Added warnings for unknown directives.
  - Return ``None`` for missing directives.
  - Added ``register_directive()``, thanks to William Dode and Paul
    Moore.

* docutils/parsers/rst/directives/admonitions.py:

  - Added "admonition" directive.

* docutils/parsers/rst/directives/body.py: Added to project.  Contains
  the "topic", "sidebar" (from Patrick O'Brien), "line-block",
  "parsed-literal", "rubric", "epigraph", "highlights" and
  "pull-quote" directives.

* docutils/parsers/rst/directives/images.py:

  - Added an "align" attribute to the "image" & "figure" directives
    (by Adam Chodorowski).
  - Added "class" option to "image", and "figclass" to "figure".

* docutils/parsers/rst/directives/misc.py:

  - Added "include", "raw", and "replace" directives, courtesy of
    Dethe Elza.
  - Added "unicode" and "class" directives.

* docutils/parsers/rst/directives/parts.py:

  - Added the "sectnum" directive; by Dmitry Jemerov.
  - Added "class" option to "contents" directive.

* docutils/parsers/rst/directives/references.py: Added to project.
  Contains the "target-notes" directive.

* docutils/parsers/rst/languages/__init__.py:

  - Return ``None`` from get_language() for missing language modules.

* docutils/parsers/rst/languages/de.py: Added to project; German
  mappings by Engelbert Gruber.

* docutils/parsers/rst/languages/en.py:

  - Added interpreted text roles mapping.

* docutils/parsers/rst/languages/es.py: Added to project; Spanish
  mappings by Marcelo Huerta San Martin.

* docutils/parsers/rst/languages/fr.py: Added to project; French
  mappings by William Dode.

* docutils/parsers/rst/languages/it.py: Added to project; Italian
  mappings by Nicola Larosa.

* docutils/parsers/rst/languages/sk.py: Added to project; Slovak
  mappings by Miroslav Vasko.

* docutils/readers/__init__.py:

  - Added support for the observer pattern from ``utils.Reporter``, in
    ``Reader.parse`` and ``Reader.transform``.
  - Removed ``Reader.transform()`` method.
  - Added default parameter values to ``Reader.__init__()`` to make
    instantiation easier.
  - Removed bogus aliases: "restructuredtext" is *not* a Reader.

* docutils/readers/pep.py:

  - Added the ``peps.TargetNotes`` transform to the Reader.
  - Removed PEP & RFC reference detection code; moved to
    parsers/rst/states.py as options (enabled here by default).
  - Added support for pre-acceptance PEPs (no PEP number yet).
  - Moved ``Inliner`` & made it a class attribute of ``Reader`` for
    easy subclassing.

* docutils/readers/python: Python Source Reader subpackage added to
  project, including preliminary versions of:

  - __init__.py
  - moduleparser.py: Parser for Python modules.

* docutils/transforms/__init__.py:

  - Added ``Transformer`` class and completed transform reform.
  - Added unknown_reference_resolvers list for each transformer.
    This list holds the list of functions provided by each component
    of the transformer that help resolve references.

* docutils/transforms/frontmatter.py:

  - Improved support for generic fields.
  - Fixed bibliographic field language lookups.

* docutils/transforms/misc.py: Added to project.  Miscellaneous
  transforms.

* docutils/transforms/parts.py:

  - Moved the "id" attribute from TOC list items to the references
    (``Contents.build_contents()``).
  - Added the ``SectNum`` transform; by Dmitry Jemerov.
  - Added "class" attribute support to ``Contents``.

* docutils/transforms/peps.py:

  - Added ``mask_email()`` function, updating to pep2html.py's
    functionality.
  - Linked "Content-Type: text/x-rst" to PEP 12.
  - Added the ``TargetNotes`` PEP-specific transform.
  - Added ``TargetNotes.cleanup_callback``.
  - Added title check to ``Headers``.

* docutils/transforms/references.py:

  - Added the ``TargetNotes`` generic transform.
  - Split ``Hyperlinks`` into multiple transforms.
  - Fixed bug with multiply-indirect references (report: Bruce Smith).
  - Added check for circular indirect references.
  - Made substitutions case-sensitive-but-forgiving.

* docutils/transforms/universal.py:

  - Added support for the ``--expose-internal-attributes`` option.
  - Removed ``Pending`` transform classes & data.

* docutils/writers/__init__.py:

  - Removed ``Writer.transform()`` method.

* docutils/writers/docutils-xml.py:

  - Added XML and doctype declarations.
  - Added ``--no-doctype`` and ``--no-xml-declaration`` options.

* docutils/writers/html4css1.py:

  - "name" attributes only on these tags: a, applet, form, frame,
    iframe, img, map.
  - Added "name" attribute to <a> in section titles for Netscape 4
    support (bug report: Pearu Peterson).
  - Fixed targets (names) on footnote, citation, topic title,
    problematic, and system_message nodes (for Netscape 4).
  - Changed field names from "<td>" to "<th>".
  - Added "@" to "&#64;" encoding to thwart address harvesters.
  - Improved the vertical whitespace optimization; ignore "invisible"
    nodes (targets, comments, etc.).
  - Improved inline literals with ``<span class="pre">`` around chunks
    of text and ``&nbsp;`` for runs of spaces.
  - Improved modularity of output; added ``self.body_pre_docinfo`` and
    ``self.docinfo`` segments.
  - Added support for "line_block", "address" elements.
  - Improved backlinks (footnotes & system_messages).
  - Improved system_message output.
  - Redefined ``--stylesheet`` as containing an invariant URL, used
    verbatim.  Added ``--stylesheet-path``, interpreted w.r.t. the
    working directory.
  - Added ``--footnote-references`` option (superscript or brackets).
  - Added ``--compact-lists`` and ``--no-compact-lists`` options.
  - Added ``--embed-stylesheet`` and ``--link-stylesheet`` options;
    factored out ``HTMLTranslator.get_stylesheet_reference()``.
  - Improved field list rendering.
  - Added Docutils version to "generator" meta tag.
  - Fixed a bug with images; they must be inline, so wrapped in <p>.
  - Improved layout of <pre> HTML source.
  - Fixed attribute typo on <colspec>.
  - Refined XML prologue.
  - Support for no stylesheet.
  - Removed "interpreted" element support.
  - Added support for "title_reference", "sidebar", "attribution",
    "rubric", and generic "admonition" elements.
  - Added ``--attribution`` option.
  - Added support for "inline", "subscript", "superscript" elements.
  - Added initial support for "abbreviation" and "acronym";
    incomplete.

* docutils/writers/latex2e.py: LaTeX Writer, added by Engelbert Gruber
  (from the sandbox).

  - Added french.
  - Double quotes in literal blocks (special treatment for de/ngerman).
  - Added ``--hyperlink-color`` option ('0' turns off coloring of links).
  - Added ``--attribution`` option.
  - Right align attributions.

* docutils/writers/pep_html.py:

  - Parameterized output encoding in PEP template.
  - Reworked substitutions from ``locals()`` into ``subs`` dict.
  - Redefined ``--pep-stylesheet`` as containing an invariant URL, used
    verbatim.  Added ``--pep-stylesheet-path``, interpreted w.r.t. the
    working directory.
  - Added an override on the ``--footnote-references`` option.
  - Factored out ``HTMLTranslator.get_stylesheet_reference()``.
  - Added Docutils version to "generator" meta tag.
  - Added a "DO NOT EDIT THIS FILE" comment to generated HTML.

* docs/tools.txt:

  - Added a "silent" setting for ``buildhtml.py``.
  - Added a "Getting Help" section.
  - Rearranged the structure.
  - Kept up to date, with new settings, command-line options etc.
  - Added section for ``rst2latex.py`` (Engelbert Gruber).
  - Converted settings table into a definition list.

* docs/rst/quickstart.txt:

  - Added a table of contents.
  - Added feedback information.
  - Added mention of minimum section title underline lengths.
  - Removed the 4-character minimum for section title underlines.

* docs/rst/quickref.html:

  - Added a "Getting Help" section.
  - Added a style to make section title backlinks more subtle.
  - Added mention of minimum section title underline lengths.
  - Removed the 4-character minimum for section title underlines.

* extras: Directory added to project; contains third-party modules
  that Docutils depends on (optparse, textwrap, roman).  These are
  only installed if they're not already present.

* licenses: Directory added to project; contains copies of license
  files for non-public-domain files.

* spec/doctree.txt:

  - Changed the focus.  It's about DTD elements:  structural
    relationships, semantics, and external (public) attributes.  Not
    about the element class library.
  - Moved some implementation-specific stuff into ``docutils.nodes``
    docstrings.
  - Wrote descriptions of all common attributes and parameter
    entities.  Filled in introductory material.
  - Working through the element descriptions: 55 down, 37 to go.
  - Removed "Representation of Horizontal Rules" to
    spec/rst/alternatives.txt.

* spec/docutils.dtd:

  - Added "generated" inline element.
  - Added "line_block" body element.
  - Added "auto" attribute to "title".
  - Changed content models of "literal_block" and "doctest_block" to
    ``%text.model``.
  - Added ``%number;`` attribute type parameter entity.
  - Changed ``%structural.elements;`` to ``%section.elements``.
  - Updated attribute types; made more specific.
  - Added "address" bibliographic element.
  - Added "line" attribute to ``system_message`` element.
  - Removed "field_argument" element; "field_name" may contain
    multiple words and whitespace.
  - Changed public identifier to docutils.sf.net.
  - Removed "interpreted" element; added "title_reference",
    "abbreviation", "acronym".
  - Removed "refuri" attribute from "footnote_reference" and
    "citation_reference".
  - Added "sidebar", "rubric", "attribution", "admonition",
    "superscript", "subscript", and "inline" elements.

* spec/pep-0256.txt: Converted to reStructuredText & updated.

* spec/pep-0257.txt: Converted to reStructuredText & updated.

* spec/pep-0258.txt: Converted to reStructuredText & updated.

* spec/semantics.txt: Updated with text from a Doc-SIG response to
  Dallas Mahrt.

* spec/transforms.txt: Added to project.

* spec/howto: Added subdirectory, for developer how-to docs.

* spec/howto/rst-directives.txt: Added to project.  Original by Dethe
  Elza, edited & extended by David Goodger.

* spec/howto/i18n.txt: Docutils Internationalization.  Added to
  project.

* spec/rst/alternatives.txt:

  - Added "Doctree Representation of Transitions" from
    spec/doctree.txt.
  - Updated "Inline External Targets" & closed the debate.
  - Added ideas for interpreted text syntax extensions.
  - Added "Nested Inline Markup" section.

* spec/rst/directives.txt:

  - Added directives: "topic", "sectnum", "target-notes",
    "line-block", "parsed-literal", "include", "replace", "sidebar",
    "admonition", "rubric", "epigraph", "highlights", "unicode" and
    "class".
  - Formalized descriptions of directive details.
  - Added an "align" attribute to the "image" & "figure" directives
    (by Adam Chodorowski).
  - Added "class" options to "topic", "sidebar", "line-block",
    "parsed-literal", "contents", and "image"; and "figclass" to
    "figure".

* spec/rst/interpreted.txt: Added to project.  Descriptions of
  interpreted text roles.

* spec/rst/introduction.txt:

  - Added pointers to material for new users.

* spec/rst/reStructuredText.txt:

  - Disambiguated comments (just add a newline after the "::").
  - Updated enumerated list description; added a discussion of the
    second-line validity checking.
  - Updated directive description.
  - Added a note redirecting newbies to the user docs.
  - Expanded description of inline markup start-strings in non-markup
    contexts.
  - Removed field arguments and made field lists a generic construct.
  - Removed the 4-character minimum for section title underlines.
  - Clarified term/classifier delimiter & inline markup ambiguity
    (definition lists).
  - Added "Embedded URIs".
  - Updated "Interpreted Text" section.
  - Added "Character-Level Inline Markup" section.

* test: Continually adding & updating tests.

  - Moved test/test_rst/ to test/test_parsers/test_rst/.
  - Moved test/test_pep/ to test/test_readers/test_pep/.
  - Added test/test_readers/test_python/.
  - Added test/test_writers/ (Engelbert Gruber).

* tools:

  - Made the ``locale.setlocale()`` calls in front ends
    fault-tolerant.

* tools/buildhtml.py:

  - Added ``--silent`` option.
  - Fixed bug with absolute paths & ``--config``.
  - Updated for new I/O classes.
  - Added some exception handling.
  - Separated publishers' setting defaults; prevents interference.
  - Updated for new ``publish_file()`` convenience function.

* tools/pep-html-template:

  - Allow for ``--embed-stylesheet``.
  - Added Docutils version to "generator" meta tag.
  - Added a "DO NOT EDIT THIS FILE" comment to generated HTML.
  - Conform to XHTML spec.

* tools/pep2html.py:

  - Made ``argv`` a parameter to ``main()``.
  - Added support for "Content-Type:" header & arbitrary PEP formats.
  - Linked "Content-Type: text/plain" to PEP 9.
  - Files skipped (due to an error) are not pushed onto the server.
  - Updated for new I/O classes.
  - Added ``check_requirements()`` & ``pep_type_error()``.
  - Added some exception handling.
  - Updated for new ``publish_string()`` convenience function.
  - Added a "DO NOT EDIT THIS FILE" comment to generated HTML.

* tools/quicktest.py:

  - Added ``-V``/``--version`` option.

* tools/rst2latex.py: LaTeX front end, added by Engelbert Gruber.

* tools/unicode2rstsubs.py: Added to project.  Produces character
  entity files (reSructuredText substitutions) from the MathML master
  unicode.xml file.

* tools/editors: Support code for editors, added to project.  Contains
  ``emacs/restructuredtext.el``.

* tools/stylesheets/default.css: Moved into the stylesheets directory.

  - Added style for chunks of inline literals.
  - Removed margin for first child of table cells.
  - Right-aligned field list names.
  - Support for auto-numbered section titles in TOCs.
  - Increased the size of inline literals (<tt>) in titles.
  - Restored the light gray background for inline literals.
  - Added support for "line_block" elements.
  - Added style for "address" elements.
  - Removed "a.footnote-reference" style; doing it with ``<sup>`` now.
  - Improved field list rendering.
  - Vertical whitespace improvements.
  - Removed "a.target" style.

* tools/stylesheets/pep.css:

  - Fixed nested section margins.
  - Other changes parallel those of ``../default.css``.


Release 0.2 (2002-07-31)
========================

General:

- The word "component" was being used ambiguously.  From now on,
  "component" will be used to mean "Docutils component", as in Reader,
  Writer, Parser, or Transform.  Portions of documents (Table of
  Contents, sections, etc.)  will be called "document parts".
- Did a grand renaming: a lot of ``verylongnames`` became
  ``very_long_names``.
- Cleaned up imports: no more relative package imports or
  comma-separated lists of top-level modules.
- Added support for an option values object which carries default
  settings and overrides (from command-line options and library use).
- Added internal Unicode support, and support for both input and
  output encodings.
- Added support for the ``docutils.io.IO`` class & subclasses.

Specific:

* docutils/__init__.py:

  - Added ``ApplicationError`` and ``DataError``, for use throughout
    the package.
  - Added ``Component`` base class for Docutils components; implements
    the ``supports`` method.
  - Added ``__version__`` (thus, ``docutils.__version__``).

* docutils/core.py:

  - Removed many keyword parameters to ``Publisher.__init__()`` and
    ``publish()``; bundled into an option values object.  Added
    "argv", "usage", "description", and "option_spec" parameters for
    command-line support.
  - Added ``Publisher.process_command_line()`` and ``.set_options()``
    methods.
  - Reworked I/O model for ``docutils.io`` wrappers.
  - Updated ``Publisher.set_options()``; now returns option values
    object.
  - Added support for configuration files (/etc/docutils.conf,
    ./docutils.conf, ~/.docutils).
  - Added ``Publisher.setup_option_parser()``.
  - Added default usage message and description.

* docutils/frontend.py: Added to project; support for front-end
  (command-line) scripts.  Option specifications may be augmented by
  components.  Requires Optik (http://optik.sourceforge.net/) for option
  processing (installed locally as docutils/optik.py).

* docutils/io.py: Added to project; uniform API for a variety of input
  output mechanisms.

* docutils/nodes.py:

  - Added ``TreeCopyVisitor`` class.
  - Added a ``copy`` method to ``Node`` and subclasses.
  - Added a ``SkipDeparture`` exception for visitors.
  - Renamed ``TreePruningException`` from ``VisitorException``.
  - Added docstrings to ``TreePruningException``, subclasses, and
    ``Nodes.walk()``.
  - Improved docstrings.
  - Added ``SparseNodeVisitor``, refined ``NodeVisitor``.
  - Moved ``utils.id()`` to ``nodes.make_id()`` to avoid circular
    imports.
  - Added ``decoration``, ``header``, and ``footer`` node classes, and
    ``PreDecorative`` mixin.
  - Reworked the name/id bookkeeping; to ``document``, removed
    ``explicit_targets`` and ``implicit_targets`` attributes, added
    ``nametypes`` attribute and ``set_name_id_map`` method.
  - Added ``NodeFound`` exception, for use with ``NodeVisitor``
    traversals.
  - Added ``document.has_name()`` method.
  - Fixed DOM generation for list-attributes.
  - Added category class ``Labeled`` (used by footnotes & citations).
  - Added ``Element.set_class()`` method (sets "class" attribute).

* docutils/optik.py: Added to project.  Combined from the Optik
  package, with added option groups and other modifications.  The use
  of this module is probably only temporary.

* docutils/statemachine.py:

  - Added ``runtime_init`` method to ``StateMachine`` and ``State``.
  - Added underscores to improve many awkward names.
  - In ``string2lines()``, changed whitespace normalizing translation
    table to regexp; restores Python 2.0 compatibility with Unicode.

* docutils/urischemes.py:

  - Filled in some descriptions.
  - Added "shttp" scheme.

* docutils/utils.py:

  - Added ``clean_rcs_keywords`` function (moved from
    docutils/transforms/frontmatter.py
    ``DocInfo.filter_rcs_keywords``).
  - Added underscores to improve many awkward names.
  - Changed names of Reporter's thresholds:
    warning_level -> report_level; error_level -> halt_level.
  - Moved ``utils.id()`` to ``nodes.make_id()``.
  - Added ``relative_path(source, target)``.

* docutils/languages/de.py: German mappings; added to project.  Thanks
  to Gunnar Schwant for the translations.

* docutils/languages/en.py: Added "Dedication" bibliographic field
  mappings.

* docutils/languages/sv.py: Swedish mappings; added to project by Adam
  Chodorowski.

* docutils/parsers/rst/states.py:

  - Added underscores to improve many awkward names.
  - Added RFC-2822 header support.
  - Extracted the inline parsing code from ``RSTState`` to a separate
    class, ``Inliner``, which will allow easy subclassing.
  - Made local bindings for ``memo`` container & often-used contents
    (reduces code complexity a lot).  See ``RSTState.runtime_init()``.
  - ``RSTState.parent`` replaces ``RSTState.statemachine.node``.
  - Added ``MarkupMismatch`` exception; for late corrections.
  - Added ``-/:`` characters to inline markup's start string prefix,
    ``/`` to end string suffix.
  - Fixed a footnote bug.
  - Fixed a bug with literal blocks.
  - Applied patch from Simon Budig: simplified regexps with symbolic
    names, removed ``Inliner.groups`` and ``Body.explicit.groups``.
  - Converted regexps from ``'%s' % var`` to ``'%(var)s' % locals()``.
  - Fixed a bug in ``Inliner.interpreted_or_phrase_ref()``.
  - Allowed non-ASCII in "simple names" (directive names, field names,
    references, etc.).
  - Converted ``Inliner.patterns.initial`` to be dynamically built
    from parts with ``build_regexp()`` function.
  - Changed ``Inliner.inline_target`` to ``.inline_internal_target``.
  - Updated docstrings.
  - Changed "table" to "grid_table"; added "simple_table" support.

* docutils/parsers/rst/tableparser.py:

  - Changed ``TableParser`` to ``GridTableParser``.
  - Added ``SimpleTableParser``.
  - Refactored naming.

* docutils/parsers/rst/directives/__init__.py: Added "en" (English) as
  a fallback language for directive names.

* docutils/parsers/rst/directives/html.py: Changed the ``meta``
  directive to use a ``pending`` element, used only by HTML writers.

* docutils/parsers/rst/directives/parts.py: Renamed from
  components.py.

  - Added "backlinks" attribute to "contents" directive.

* docutils/parsers/rst/languages/sv.py: Swedish mappings; added to
  project by Adam Chodorowski.

* docutils/readers/__init__.py: Gave Readers more control over
  choosing and instantiating Parsers.

* docutils/readers/pep.py: Added to project; for PEP processing.

* docutils/transforms/__init__.py: ``Transform.__init__()`` now
  requires a ``component`` parameter.

* docutils/transforms/components.py: Added to project; transforms
  related to Docutils components.

* docutils/transforms/frontmatter.py:

  - In ``DocInfo.extract_authors``, check for a single "author" in an
    "authors" group, and convert it to a single "author" element.
  - Added support for "Dedication" and generic bibliographic fields.

* docutils/transforms/peps.py: Added to project; PEP-specific.

* docutils/transforms/parts.py: Renamed from old components.py.

  - Added filter for ``Contents``, to use alt-text for inline images,
    and to remove inline markup that doesn't make sense in the ToC.
  - Added "name" attribute to TOC topic depending on its title.
  - Added support for optional TOC backlinks.

* docutils/transforms/references.py: Fixed indirect target resolution
  in ``Hyperlinks`` transform.

* docutils/transforms/universal.py:

  - Changed ``Messages`` transform to properly filter out system
    messages below the warning threshold.
  - Added ``Decorations`` transform (support for ``--generator``,
    ``--date``, ``--time``, ``--source-link`` options).

* docutils/writers/__init__.py: Added "pdf" alias in anticipation of
  Engelbert Gruber's PDF writer.

* docutils/writers/html4css1.py:

  - Made XHTML-compatible (switched to lowercase element & attribute
    names; empty tag format).
  - Escape double-dashes in comment text.
  - Improved boilerplate & modularity of output.
  - Exposed modular output in Writer class.
  - Added a "generator" meta tag to <head>.
  - Added support for the ``--stylesheet`` option.
  - Added support for ``decoration``, ``header``, and ``footer``
    elements.
  - In ``HTMLTranslator.attval()``, changed whitespace normalizing
    translation table to regexp; restores Python 2.0 compatibility
    with Unicode.
  - Added the translator class as instance variable to the Writer, to
    make it easily subclassable.
  - Improved option list spacing (thanks to Richard Jones).
  - Modified field list output.
  - Added backlinks to footnotes & citations.
  - Added percentage widths to "<col>" tags (from colspec).
  - Option lists: "<code>" changed to "<kbd>", ``option_argument``
    "<span>" changed to "<var>".
  - Inline literals: "<code>" changed to "<tt>".
  - Many changes to optimize vertical space: compact simple lists etc.
  - Add a command-line options & directive attributes to control TOC
    and footnote/citation backlinks.
  - Added support for optional footnote/citation backlinks.
  - Added support for generic bibliographic fields.
  - Identify backrefs.
  - Relative URLs for stylesheet links.

* docutils/writers/pep_html.py: Added to project; HTML Writer for
  PEPs (subclass of ``html4css1.Writer``).

* docutils/writers/pseudoxml.py: Renamed from pprint.py.

* docutils/writers/docutils_xml.py: Added to project; trivial writer
  of the Docutils internal doctree in XML.

* docs/tools.txt: "Docutils Front-End Tools", added to project.

* spec/doctree.txt:

  - Changed the title to "The Docutils Document Tree".
  - Added "Hyperlink Bookkeeping" section.

* spec/docutils.dtd:

  - Added ``decoration``, ``header``, and ``footer`` elements.
  - Brought ``interpreted`` element in line with the parser: changed
    attribute "type" to "role", added "position".
  - Added support for generic bibliographic fields.

* spec/notes.txt: Continual updates.  Added "Project Policies".

* spec/pep-0256.txt:  Updated.  Added "Roadmap to the Doctring PEPs"
  section.

* spec/pep-0257.txt: Clarified prohibition of signature repetition.

* spec/pep-0258.txt: Updated.  Added text from pysource.txt and
  mailing list discussions.

* spec/pep-0287.txt:

  - Renamed to "reStructuredText Docstring Format".
  - Minor edits.
  - Reworked Q&A as an enumerated list.
  - Converted to reStructuredText format.

* spec/pysource.dtd:

  - Reworked structural elements, incorporating ideas from Tony Ibbs.

* spec/pysource.txt: Removed from project.  Moved much of its contents
  to pep-0258.txt.

* spec/rst/alternatives.txt:

  - Expanded auto-enumerated list idea; thanks to Fred Bremmer.
  - Added "Inline External Targets" section.

* spec/rst/directives.txt:

  - Added "backlinks" attribute to "contents" directive.

* spec/rst/problems.txt:

  - Updated the Enumerated List Markup discussion.
  - Added new alternative table markup syntaxes.

* spec/rst/reStructuredText.txt:

  - Clarified field list usage.
  - Updated enumerated list description.
  - Clarified purpose of directives.
  - Added ``-/:`` characters to inline markup's start string prefix,
    ``/`` to end string suffix.
  - Updated "Authors" bibliographic field behavior.
  - Changed "inline hyperlink targets" to "inline internal targets".
  - Added "simple table" syntax to supplement the existing but
    newly-renamed "grid tables".
  - Added cautions for anonymous hyperlink use.
  - Added "Dedication" and generic bibliographic fields.

* test: Made test modules standalone (subdirectories became packages).

* test/DocutilsTestSupport.py:

  - Added support for PEP extensions to reStructuredText.
  - Added support for simple tables.
  - Refactored naming.

* test/package_unittest.py: Renamed from UnitTestFolder.py.

  - Now supports true packages containing test modules
    (``__init__.py`` files required); fixes duplicate module name bug.

* test/test_pep/: Subpackage added to project; PEP testing.

* test/test_rst/test_SimpleTableParser.py: Added to project.

* tools:

  - Updated html.py and publish.py front-end tools to use the new
    command-line processing facilities of ``docutils.frontend``
    (exposed in ``docutils.core.Publisher``), reducing each to just a
    few lines of code.
  - Added ``locale.setlocale()`` calls to front-end tools.

* tools/buildhtml.py: Added to project; batch-generates .html from all
  the .txt files in directories and subdirectories.

* tools/default.css:

  - Added support for ``header`` and ``footer`` elements.
  - Added styles for "Dedication" topics (biblio fields).

* tools/docutils.conf: A configuration file; added to project.

* tools/docutils-xml.py: Added to project.

* tools/pep.py: Added to project; PEP to HTML front-end tool.

* tools/pep-html-template: Added to project.

* tools/pep2html.py: Added to project from Python (nondist/peps).
  Added support for Docutils (reStructuredText PEPs).

* tools/quicktest.py:

  - Added the ``--attributes`` option, hacked a bit.
  - Added a second command-line argument (output file); cleaned up.

* tools/stylesheets/: Subdirectory added to project.

* tools/stylesheets/pep.css: Added to project; stylesheet for PEPs.


Release 0.1 (2002-04-20)
========================

This is the first release of Docutils, merged from the now inactive
reStructuredText__ and `Docstring Processing System`__ projects.  For
the pre-Docutils history, see the `reStructuredText HISTORY`__ and the
`DPS HISTORY`__ files.

__ http://structuredtext.sourceforge.net/
__ http://docstring.sourceforge.net/
__ http://structuredtext.sourceforge.net/HISTORY.html
__ http://docstring.sourceforge.net/HISTORY.html

General changes: renamed 'dps' package to 'docutils'; renamed
'restructuredtext' subpackage to 'rst'; merged the codebases; merged
the test suites (reStructuredText's test/test_states renamed to
test/test_rst); and all modifications required to make it all work.

* docutils/parsers/rst/states.py:

  - Improved diagnostic system messages for missing blank lines.
  - Fixed substitution_reference bug.

.. References
   ==========

.. _RELEASE-NOTES: RELEASE-NOTES.html
.. _`_config_files`: docs/user/config.html#config-files
.. _auto_id_prefix: docs/user/config.html#auto-id-prefix
.. _detailled:
.. _detailed: docs/user/config.html#detailed
.. _docutils_footnotes: docs/user/config.html#docutils-footnotes
.. _dump_settings: docs/user/config.html#dump-settings
.. _embed_images: docs/user/config.html#embed-images
.. _embed_stylesheet: docs/user/config.html#embed-stylesheet
.. _figure_footnotes: docs/user/config.html#figure-footnotes
.. _file_insertion_enabled: docs/user/config.html#file-insertion-enabled
.. _graphicx_option: docs/user/config.html#graphicx-option
.. _hidden_controls: docs/user/config.html#hidden-controls
.. _html_writer: docs/user/config.html#html-writer
.. _hyperref_options: docs/user/config.html#hyperref-options
.. _id_prefix: docs/user/config.html#id-prefix
.. _ignore: docs/user/config.html#ignore
.. _image_loading: docs/user/config.html#image-loading
.. _indents: docs/user/config.html#indents
.. _initial_header_level: docs/user/config.html#initial-header-level
.. _input_encoding: docs/user/config.html#input-encoding
.. _input_encoding_error_handler: docs/user/config.html#input-encoding-error-handler
.. _language: docs/user/config.html#language
.. _latex_preamble: docs/user/config.html#latex-preamble
.. _legacy_class_functions: docs/user/config.html#legacy-class-functions
.. _legacy_column_widths: docs/user/config.html#legacy-column-widths
.. _literal_block_env: docs/user/config.html#literal-block-env
.. _math_output: docs/user/config.html#math-output
.. _output: docs/user/config.html#output
.. _output_encoding: docs/user/config.html#output-encoding
.. _prune: docs/user/config.html#prune
.. _raw_enabled: docs/user/config.html#raw-enabled
.. _reference_label: docs/user/config.html#reference-label
.. _root_prefix: docs/user/config.html#root-prefix
.. _smart_quotes: docs/user/config.html#smart-quotes
.. _sources: docs/user/config.html#sources
.. _strip_classes: docs/user/config.html#strip-classes
.. _strip_elements_with_classes: docs/user/config.html#strip-elements-with-classes
.. _stylesheet: docs/user/config.html#stylesheet
.. _stylesheet_dirs: docs/user/config.html#stylesheet-dirs
.. _stylesheet_path: docs/user/config.html#stylesheet-path
.. _syntax_highlight: docs/user/config.html#syntax-highlight
.. _table_style: docs/user/config.html#table-style
.. _text_references: docs/user/config.html#text_references
.. _theme: docs/user/config.html#theme
.. _theme_url: docs/user/config.html#theme-url
.. _toc_backlinks: docs/user/config.html#toc-backlinks
.. _traceback: docs/user/config.html#traceback
.. _use_bibtex: docs/user/config.html#use-bibtex
.. _use_latex_abstract: docs/user/config.html#use-latex-abstract
.. _use_latex_footnotes: docs/user/config.html#use-latex-footnotes
.. _use_latex_toc: docs/user/config.html#use-latex-toc
.. _view_mode: docs/user/config.html#view-mode

.. _<meta>: docs/ref/doctree.html#meta
.. _<image>: docs/ref/doctree.html#image
.. _<inline>: docs/ref/doctree.html#inline
.. _<literal>: docs/ref/doctree.html#literal


.. Emacs settings

   Local Variables:
   mode: indented-text
   mode: rst
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 70
   End:

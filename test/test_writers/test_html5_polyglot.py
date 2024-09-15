#! /usr/bin/env python3

# $Id$
# Author: reggie dugard <reggie@users.sourceforge.net>
# Maintainer: docutils-develop@lists.sourceforge.net
# Copyright: This module has been placed in the public domain.

"""Test HTML5 writer output ("fragment"/"body" part).

This is the document body (not HTML <body>).
"""

from pathlib import Path
import re
import sys
import unittest

if __name__ == '__main__':
    # prepend the "docutils root" to the Python library path
    # so we import the local `docutils` package.
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import docutils
import docutils.core
from docutils.parsers.rst.directives.images import PIL
from docutils.utils.code_analyzer import with_pygments
from docutils.writers import html5_polyglot

if with_pygments:
    import pygments
    _pv = re.match(r'^([0-9]+)\.([0-9]*)', pygments.__version__)
    if (int(_pv[1]), int(_pv[2])) >= (2, 14):
        # pygments output changed in version 2.14
        with_pygments = False

# TEST_ROOT is ./test/ from the docutils root
TEST_ROOT = Path(__file__).parents[1]
DATA_ROOT = TEST_ROOT / 'data'
ROOT_PREFIX = (TEST_ROOT / 'functional/input').as_posix()

# Pillow/PIL is optional:
if PIL:
    REQUIRES_PIL = ''
    ONLY_LOCAL = 'Can only read local images.'
    DUMMY_PNG_NOT_FOUND = "[Errno 2] No such file or directory: 'dummy.png'"
    # Pillow reports the absolute path since version 10.3.0 (cf. [bugs: 485])
    if (tuple(int(i) for i in PIL.__version__.split('.')) >= (10, 3)):
        DUMMY_PNG_NOT_FOUND = ("[Errno 2] No such file or directory: '%s'"
                               % Path('dummy.png').resolve())
    HEIGHT_ATTR = 'height="32" '
    WIDTH_ATTR = 'width="32" '
    NO_PIL_SYSTEM_MESSAGE = ''
else:
    REQUIRES_PIL = '\n  Requires Python Imaging Library.'
    ONLY_LOCAL = 'Requires Python Imaging Library.'
    DUMMY_PNG_NOT_FOUND = 'Requires Python Imaging Library.'
    HEIGHT_ATTR = ''
    WIDTH_ATTR = ''
    NO_PIL_SYSTEM_MESSAGE = (
        '<aside class="system-message">\n'
        '<p class="system-message-title">System Message:'
        ' WARNING/2 (<span class="docutils literal">'
        '&lt;string&gt;</span>, line 1)</p>\n'
        '<p>Cannot scale image!\n'
        '  Could not get size from &quot;/data/blue%20square.png&quot;:\n'
        '  Requires Python Imaging Library.</p>\n'
        '</aside>\n')


class Html5WriterPublishPartsTestCase(unittest.TestCase):
    """Test case for HTML5 writer via the publish_parts() interface."""

    maxDiff = None

    def test_publish(self):
        if not with_pygments:
            del totest['syntax_highlight']
        for name, (settings_overrides, cases) in totest.items():
            for casenum, (case_input, case_expected) in enumerate(cases):
                with self.subTest(id=f'totest[{name!r}][{casenum}]'):
                    parts = docutils.core.publish_parts(
                        source=case_input,
                        writer=html5_polyglot.Writer(),
                        settings_overrides={
                            '_disable_config': True,
                            'strict_visitor': True,
                            'stylesheet_path': '',
                            'section_self_link': True,
                            **settings_overrides,
                        }
                    )
                    self.assertEqual(case_expected, parts['body'])


totest = {}  # expected samples contain only the "body" part of the HMTL output

totest['standard'] = ({}, [
["""\
Simple String
""",
'<p>Simple String</p>\n',
],
["""\
Simple String with *markup*
""",
'<p>Simple String with <em>markup</em></p>\n',
],
["""\
Simple String with an even simpler ``inline literal``
""",
'<p>Simple String with an even simpler <span class="docutils literal">inline literal</span></p>\n',
],
["""\
A simple `anonymous reference`__

__ http://www.test.com/test_url
""",
'<p>A simple <a class="reference external" href="http://www.test.com/test_url">anonymous reference</a></p>\n',
],
["""\
One paragraph.

Two paragraphs.
""",
"""\
<p>One paragraph.</p>
<p>Two paragraphs.</p>
""",
],
["""\
A simple `named reference`_ with stuff in between the
reference and the target.

.. _`named reference`: http://www.test.com/test_url
""",
"""\
<p>A simple <a class="reference external" href="http://www.test.com/test_url">named reference</a> with stuff in between the
reference and the target.</p>
""",
],
["""\
.. [CIT2022] A citation.
""",
"""\
<div role="list" class="citation-list">
<div class="citation" id="cit2022" role="doc-biblioentry">
<span class="label"><span class="fn-bracket">[</span>CIT2022<span class="fn-bracket">]</span></span>
<p>A citation.</p>
</div>
</div>
""",
],
[f"""\
.. image:: {DATA_ROOT.as_uri()}/circle.svg
   :loading: embed
   :width: 50%
   :height: 30
   :align: left
""",
"""\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10" style="width: 50%;" height="30" class="align-left">
  <circle cx="5" cy="5" r="4" fill="lightblue" />
</svg>
"""],
])


totest['no_title_promotion'] = ({'doctitle_xform': False}, [
["""\
+++++
Title
+++++

Not A Subtitle
==============

Some stuff

Section
-------

Some more stuff

Another Section
...............

And even more stuff
""",
"""\
<section id="title">
<h2>Title<a class="self-link" title="link to this section" href="#title"></a></h2>
<section id="not-a-subtitle">
<h3>Not A Subtitle<a class="self-link" title="link to this section" href="#not-a-subtitle"></a></h3>
<p>Some stuff</p>
<section id="section">
<h4>Section<a class="self-link" title="link to this section" href="#section"></a></h4>
<p>Some more stuff</p>
<section id="another-section">
<h5>Another Section<a class="self-link" title="link to this section" href="#another-section"></a></h5>
<p>And even more stuff</p>
</section>
</section>
</section>
</section>
""",
],
["""\
* bullet
* list
""",
"""\
<ul class="simple">
<li><p>bullet</p></li>
<li><p>list</p></li>
</ul>
""",
],
["""\
.. table::
   :align: right
   :width: 320

   +-----+-----+
   |  1  |  2  |
   +-----+-----+
   |  3  |  4  |
   +-----+-----+
""",
"""\
<table class="align-right" style="width: 320px;">
<tbody>
<tr><td><p>1</p></td>
<td><p>2</p></td>
</tr>
<tr><td><p>3</p></td>
<td><p>4</p></td>
</tr>
</tbody>
</table>
""",
],
["""\
Not a docinfo.

:This: .. _target:

       is
:a:
:simple:
:field: list
""",
"""\
<p>Not a docinfo.</p>
<dl class="field-list simple">
<dt>This<span class="colon">:</span></dt>
<dd><p id="target">is</p>
</dd>
<dt>a<span class="colon">:</span></dt>
<dd><p></p></dd>
<dt>simple<span class="colon">:</span></dt>
<dd><p></p></dd>
<dt>field<span class="colon">:</span></dt>
<dd><p>list</p>
</dd>
</dl>
""",
],
["""\
Not a docinfo.

:This is: a
:simple field list with loooong field: names
""",
"""\
<p>Not a docinfo.</p>
<dl class="field-list simple">
<dt>This is<span class="colon">:</span></dt>
<dd><p>a</p>
</dd>
<dt>simple field list with loooong field<span class="colon">:</span></dt>
<dd><p>names</p>
</dd>
</dl>
""",
],
["""\
Not a docinfo.

.. class:: field-indent-200

:This: is a
:simple: field list with custom indent.
""",
"""\
<p>Not a docinfo.</p>
<dl class="field-list simple" style="--field-indent: 200px;">
<dt>This<span class="colon">:</span></dt>
<dd><p>is a</p>
</dd>
<dt>simple<span class="colon">:</span></dt>
<dd><p>field list with custom indent.</p>
</dd>
</dl>
""",
],
["""\
Not a docinfo.

.. class:: field-indent-200uf

:This: is a
:simple: field list without custom indent,
         because the unit "uf" is invalid.
""",
"""\
<p>Not a docinfo.</p>
<dl class="field-indent-200uf field-list simple">
<dt>This<span class="colon">:</span></dt>
<dd><p>is a</p>
</dd>
<dt>simple<span class="colon">:</span></dt>
<dd><p>field list without custom indent,
because the unit &quot;uf&quot; is invalid.</p>
</dd>
</dl>
""",
],
["""\
.. figure:: dummy.png

   The figure's caption.

   A legend.

   The legend's second paragraph.
""",
"""\
<figure>
<img alt="dummy.png" src="dummy.png" />
<figcaption>
<p>The figure's caption.</p>
<div class="legend">
<p>A legend.</p>
<p>The legend's second paragraph.</p>
</div>
</figcaption>
</figure>
""",
],
["""\
.. figure:: dummy.png

   The figure's caption, no legend.
""",
"""\
<figure>
<img alt="dummy.png" src="dummy.png" />
<figcaption>
<p>The figure's caption, no legend.</p>
</figcaption>
</figure>
""",
],
["""\
.. figure:: dummy.png

   ..

   A legend without caption.
""",
"""\
<figure>
<img alt="dummy.png" src="dummy.png" />
<figcaption>
<div class="legend">
<p>A legend without caption.</p>
</div>
</figcaption>
</figure>
""",
],
["""\
.. figure:: dummy.png

No caption nor legend.
""",
"""\
<figure>
<img alt="dummy.png" src="dummy.png" />
</figure>
<p>No caption nor legend.</p>
""",
],
[f"""\
.. include:: {DATA_ROOT}/multiple-term-definition.xml
   :parser: xml
""",
"""\
<dl>
<dt>New in Docutils 0.22</dt>
<dd><p>A definition list item may contain several
terms with optional classifier(s).</p>
<p>However, there is currently no corresponding
reStructuredText syntax.</p>
</dd>
<dt>term 2a</dt>
<dt>term 2b</dt>
<dd><p>definition 2</p>
</dd>
<dt>term 3a<span class="classifier">classifier 3a</span><span class="classifier">classifier 3aa</span><dt>term 3b<span class="classifier">classifier 3b</span></dt>
<dd><p>definition 3</p>
</dd>
</dl>
""",
],
])


totest['lazy_loading'] = ({'image_loading': 'lazy',
                           'report_level': 4}, [
["""\
Lazy loading by default, overridden by :loading: option
("cannot embed" warning ignored).

.. image:: dummy.png
.. image:: dummy.png
   :loading: link
.. figure:: dummy.png
.. figure:: dummy.png
   :loading: embed
""",
"""\
<p>Lazy loading by default, overridden by :loading: option
(&quot;cannot embed&quot; warning ignored).</p>
<img alt="dummy.png" loading="lazy" src="dummy.png" />
<img alt="dummy.png" src="dummy.png" />
<figure>
<img alt="dummy.png" loading="lazy" src="dummy.png" />
</figure>
<figure>
<img alt="dummy.png" src="dummy.png" />
</figure>
""",
],
])


totest['root_prefix'] = ({'root_prefix': ROOT_PREFIX,
                          'image_loading': 'embed',
                          'warning_stream': '',
                          }, [
["""\
.. image:: /data/blue%20square.png
   :scale: 100%
.. figure:: /data/blue%20square.png
""",
f'<img alt="/data/blue%20square.png" {HEIGHT_ATTR}src="data:image/png;base64,'
'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAALElEQVR4nO3NMQ'
'EAMAjAsDFjvIhHFCbgSwU0kdXvsn96BwAAAAAAAAAAAIsNnEwBk52VRuMAAAAA'
'SUVORK5CYII="'
f' {WIDTH_ATTR}/>\n{NO_PIL_SYSTEM_MESSAGE}'
'<figure>\n'
'<img alt="/data/blue%20square.png" src="data:image/png;base64,'
'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAALElEQVR4nO3NMQ'
'EAMAjAsDFjvIhHFCbgSwU0kdXvsn96BwAAAAAAAAAAAIsNnEwBk52VRuMAAAAA'
'SUVORK5CYII=" />\n'
'</figure>\n',
],
])


totest['no_backlinks'] = ({'footnote_backlinks': False}, [

["""\
Two footnotes [#f1]_ [#f2]_ and two citations [once]_ [twice]_.

The latter are referenced a second time [#f2]_ [twice]_.

.. [#f1] referenced once
.. [#f2] referenced twice
.. [once] citation referenced once
.. [twice] citation referenced twice
""",
"""\
<p>Two footnotes <a class="brackets" href="#f1" id="footnote-reference-1" role="doc-noteref"><span class="fn-bracket">[</span>1<span class="fn-bracket">]</span></a> <a class="brackets" href="#f2" id="footnote-reference-2" role="doc-noteref"><span class="fn-bracket">[</span>2<span class="fn-bracket">]</span></a> and two citations <a class="citation-reference" href="#once" id="citation-reference-1" role="doc-biblioref">[once]</a> <a class="citation-reference" href="#twice" id="citation-reference-2" role="doc-biblioref">[twice]</a>.</p>
<p>The latter are referenced a second time <a class="brackets" href="#f2" id="footnote-reference-3" role="doc-noteref"><span class="fn-bracket">[</span>2<span class="fn-bracket">]</span></a> <a class="citation-reference" href="#twice" id="citation-reference-3" role="doc-biblioref">[twice]</a>.</p>
<aside class="footnote-list brackets">
<aside class="footnote brackets" id="f1" role="doc-footnote">
<span class="label"><span class="fn-bracket">[</span>1<span class="fn-bracket">]</span></span>
<p>referenced once</p>
</aside>
<aside class="footnote brackets" id="f2" role="doc-footnote">
<span class="label"><span class="fn-bracket">[</span>2<span class="fn-bracket">]</span></span>
<p>referenced twice</p>
</aside>
</aside>
<div role="list" class="citation-list">
<div class="citation" id="once" role="doc-biblioentry">
<span class="label"><span class="fn-bracket">[</span>once<span class="fn-bracket">]</span></span>
<p>citation referenced once</p>
</div>
<div class="citation" id="twice" role="doc-biblioentry">
<span class="label"><span class="fn-bracket">[</span>twice<span class="fn-bracket">]</span></span>
<p>citation referenced twice</p>
</div>
</div>
""",
],
])


totest['syntax_highlight'] = ({'syntax_highlight': 'short',
                               }, [
["""\
.. code:: shell

    cat <<EOF
    Hello World
    EOF
""",
"""\
<pre class="code shell literal-block"><code>cat <span class="s">&lt;&lt;EOF
Hello World
EOF</span></code></pre>
""",
],
["""\
.. role:: shell(code)
   :language: shell

:shell:`cat <<EOF Hello World EOF`
""",
"""\
<p><code class="shell">cat <span class="s">&lt;&lt;EOF Hello World EOF</span></code></p>
""",
],
])


totest['system_messages'] = ({'math_output': 'mathml',
                              'warning_stream': '',
                              }, [
["""\
.. image:: https://dummy.png
   :loading: embed
""",
"""\
<img alt="https://dummy.png" src="https://dummy.png" />
<aside class="system-message">
<p class="system-message-title">System Message: ERROR/3 \
(<span class="docutils literal">&lt;string&gt;</span>, line 1)</p>
<p>Cannot embed image &quot;https://dummy.png&quot;:
  Can only read local images.</p>
</aside>
""",
],
[f"""\
.. image:: {DATA_ROOT.as_uri()}/circle-broken.svg
   :loading: embed
""",
f"""\
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 10 10">
  <circle cx="5" cy="5" r="4" fill="lightblue" x/>
</svg>

<aside class="system-message">
<p class="system-message-title">System Message: ERROR/3 (<span class="docutils literal">&lt;string&gt;</span>, line 1)</p>
<p>Cannot parse SVG image &quot;{DATA_ROOT.as_uri()}/circle-broken.svg&quot;:
  not well-formed (invalid token): line 3, column 48</p>
</aside>
"""
],
[r"""Broken :math:`\sin \my`.
""",
"""\
<p>Broken <span class="math problematic">\\sin \\my</span>.</p>
<aside class="system-message">
<p class="system-message-title">System Message: WARNING/2 (<span class="docutils literal">&lt;string&gt;</span>, line 1)</p>
<p>Unknown LaTeX command &quot;\\my&quot;.</p>
</aside>
"""],
])

totest['system_messages-PIL'] = ({'math_output': 'mathml',
                                  'warning_stream': '',
                                  }, [
["""\
.. image:: dummy.png
   :scale: 100%
   :loading: embed
""",
f"""\
<img alt="dummy.png" src="dummy.png" />
<aside class="system-message">
<p class="system-message-title">System Message: WARNING/2 \
(<span class="docutils literal">&lt;string&gt;</span>, line 1)</p>
<p>Cannot scale image!
  Could not get size from &quot;dummy.png&quot;:
  {DUMMY_PNG_NOT_FOUND}</p>
</aside>
<aside class="system-message">
<p class="system-message-title">System Message: ERROR/3 \
(<span class="docutils literal">&lt;string&gt;</span>, line 1)</p>
<p>Cannot embed image &quot;dummy.png&quot;:
  [Errno 2] No such file or directory: 'dummy.png'</p>
</aside>
""",
],
["""\
.. image:: dummy.mp4
   :scale: 100%
""",
f"""\
<video src="dummy.mp4" title="dummy.mp4">
<a href="dummy.mp4">dummy.mp4</a>
</video>
<aside class="system-message">
<p class="system-message-title">System Message: WARNING/2 \
(<span class="docutils literal">&lt;string&gt;</span>, line 1)</p>
<p>Cannot scale image!
  Could not get size from &quot;dummy.mp4&quot;:{REQUIRES_PIL}
  PIL cannot read video images.</p>
</aside>
""",
],
["""\
.. image:: https://dummy.png
   :scale: 100%
   :loading: embed
""",
f"""\
<img alt="https://dummy.png" src="https://dummy.png" />
<aside class="system-message">
<p class="system-message-title">System Message: WARNING/2 \
(<span class="docutils literal">&lt;string&gt;</span>, line 1)</p>
<p>Cannot scale image!
  Could not get size from &quot;https://dummy.png&quot;:
  {ONLY_LOCAL}</p>
</aside>
<aside class="system-message">
<p class="system-message-title">System Message: ERROR/3 \
(<span class="docutils literal">&lt;string&gt;</span>, line 1)</p>
<p>Cannot embed image &quot;https://dummy.png&quot;:
  Can only read local images.</p>
</aside>
""",
],
])

totest['no_system_messages'] = ({'math_output': 'mathml',
                                 'report_level': 4,
                                 'warning_stream': '',
                                 }, [
["""\
.. image:: dummy.png
   :scale: 100%
   :loading: embed

.. image:: dummy.mp4
   :scale: 100%
""",
"""\
<img alt="dummy.png" src="dummy.png" />
<video src="dummy.mp4" title="dummy.mp4">
<a href="dummy.mp4">dummy.mp4</a>
</video>
""",
],
[f"""\
.. image:: {DATA_ROOT.as_uri()}/circle-broken.svg
   :loading: embed
""",
"""\
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 10 10">
  <circle cx="5" cy="5" r="4" fill="lightblue" x/>
</svg>

"""],
[r'Broken :math:`\sin \my`.',
'<p>Broken <tt class="math">\\sin \\my</tt>.</p>\n'
],
])


if __name__ == '__main__':
    unittest.main()

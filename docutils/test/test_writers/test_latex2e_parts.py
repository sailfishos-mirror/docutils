#! /usr/bin/env python3
# $Id$
# Author: Günter Milde
# Maintainer: docutils-develop@lists.sourceforge.net
# :Copyright: 2024 Günter Milde,
# :License: Released under the terms of the `2-Clause BSD license`_, in short:
#
#    Copying and distribution of this file, with or without modification,
#    are permitted in any medium without royalty provided the copyright
#    notice and this notice are preserved.
#    This file is offered as-is, without any warranty.
#
# .. _2-Clause BSD license: https://opensource.org/licenses/BSD-2-Clause

"""
Test `core.publish_parts()`__ with the LaTeX writer.

__ https://docutils.sourceforge.io/docs/api/publisher.html#publish-parts
"""

from pathlib import Path
import os
import sys
import unittest


if __name__ == '__main__':
    # prepend the "docutils root" to the Python library path
    # so we import the local `docutils` package.
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import docutils
from docutils.core import publish_parts
from docutils.writers import latex2e

# DATA_ROOT is ./test/data from the docutils root
DATA_ROOT = Path(__file__).resolve().parents[1] / 'data'

ham = os.path.relpath(DATA_ROOT/'ham.tex').replace('\\', '/')
spam = os.path.relpath(DATA_ROOT/'spam').replace('\\', '/')
# workaround for PyPy (cf. https://sourceforge.net/p/docutils/bugs/471/)
if sys.implementation.name == "pypy" and sys.version_info < (3, 10):
    spampath = f"PosixPath('{spam}.sty')"
else:
    spampath = f"'{spam}.sty'"

DEFAULT_PARTS = {
    'abstract': '',
    'body': '',
    'body_pre_docinfo': '',
    'dedication': '',
    'docinfo': '',
    'encoding': 'utf-8',
    'errors': 'strict',
    'fallbacks': '',
    'head_prefix': '\\documentclass[a4paper]{article}\n',
    'latex_preamble': '% PDF Standard Fonts\n'
                      '\\usepackage{mathptmx} % Times\n'
                      '\\usepackage[scaled=.90]{helvet}\n'
                      '\\usepackage{courier}\n',
    'pdfsetup': r"""% hyperlinks:
\ifdefined\hypersetup
\else
  \usepackage[hyperfootnotes=false,
              colorlinks=true,linkcolor=blue,urlcolor=blue]{hyperref}
  \usepackage{bookmark}
  \urlstyle{same} % normal text font (alternatives: tt, rm, sf)
\fi
""",
    'requirements': '\\usepackage[T1]{fontenc}\n',
    'stylesheet': '',
    'subtitle': '',
    'template': """\
$head_prefix% generated by Docutils <https://docutils.sourceforge.io/>
\\usepackage{cmap} % fix search and cut-and-paste in Acrobat
$requirements
%%% Custom LaTeX preamble
$latex_preamble
%%% User specified packages and stylesheets
$stylesheet
%%% Fallback definitions for Docutils-specific commands
$fallbacks
$pdfsetup
%%% Body
\\begin{document}
$titledata$body_pre_docinfo$docinfo$dedication$abstract$body
\\end{document}
""",
    'title': '',
    'titledata': '',
    'version': f'{docutils.__version__}',
    }


REQUIREMENTS_TABLE = r"""\usepackage{longtable,ltcaption,array}
\setlength{\extrarowheight}{2pt}
\newlength{\DUtablewidth} % internal use in tables
"""


class LaTeXWriterPublishPartsTestCase(unittest.TestCase):
    """Test LaTeX writer `publish_parts()` interface."""

    maxDiff = None
    settings = {'_disable_config': True,
                'strict_visitor': True,
                # avoid latex writer future warnings:
                'use_latex_citations': False,
                'legacy_column_widths': True,
                }

    def test_publish_parts(self):
        for name, (settings_overrides, cases) in samples.items():
            for casenum, (case_input, expected) in enumerate(cases):
                parts = publish_parts(
                    source=case_input,
                    writer=latex2e.Writer(),
                    settings_overrides=self.settings|settings_overrides,
                    )
                expected = DEFAULT_PARTS | expected
                with self.subTest(id=f'samples[{name!r}][{casenum}]'):
                    for key in parts.keys():
                        if key == 'whole':
                            continue  # assembly tested in functional tests
                        self.assertEqual(f'{expected[key]}', f'{parts[key]}',
                                         msg=f'Differences in part "{key}"!')


samples = {}

samples['default'] = ({}, [
['',  # empty input string
 {}   # results in default parts
 ],
['2 µm is just 2/1000000 m',
 {'body': '\n2 µm is just 2/1000000 m\n',
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  '\\usepackage{textcomp} % text symbol macros\n',
  }
 ],
# load "babel" if there is a text part in a foreign language
["""\
.. role:: language-es

Und damit :language-es:`basta`!
""",
 {'body': r"""
Und damit \foreignlanguage{spanish}{basta}!
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  '\\usepackage[spanish,main=english]{babel}\n'
                  '\\AtBeginDocument{\\shorthandoff{.<>}}\n'
  }],
# load requirements for code syntax higlight
[':code:`x=1`',
 {'body': '\n\\texttt{\\DUrole{code}{x=1}}\n',
  'fallbacks': r"""
% basic code highlight:
\providecommand*\DUrolecomment[1]{\textcolor[rgb]{0.40,0.40,0.40}{#1}}
\providecommand*\DUroledeleted[1]{\textcolor[rgb]{0.40,0.40,0.40}{#1}}
\providecommand*\DUrolekeyword[1]{\textbf{#1}}
\providecommand*\DUrolestring[1]{\textit{#1}}

% custom inline roles: \DUrole{#1}{#2} tries \DUrole#1{#2}
\providecommand*{\DUrole}[2]{%
  \ifcsname DUrole#1\endcsname%
    \csname DUrole#1\endcsname{#2}%
  \else%
    #2%
  \fi%
}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  '\\usepackage{color}\n'
  }],
# footnote text
["""\
.. [1] paragraph

.. [2] 1. enumeration
""",
 {'body': r"""%
\DUfootnotetext{footnote-1}{footnote-1}{1}{%
paragraph
}
%
\DUfootnotetext{footnote-2}{footnote-2}{2}{
\begin{enumerate}
\item enumeration
\end{enumerate}
}
""",
  'fallbacks': r"""
% numerical or symbol footnotes with hyperlinks and backlinks
\providecommand*{\DUfootnotemark}[3]{%
  \raisebox{1em}{\hypertarget{#1}{}}%
  \hyperlink{#2}{\textsuperscript{#3}}%
}
\providecommand{\DUfootnotetext}[4]{%
  \begingroup%
  \renewcommand{\thefootnote}{%
    \protect\raisebox{1em}{\protect\hypertarget{#1}{}}%
    \protect\hyperlink{#2}{#3}}%
  \footnotetext{#4}%
  \endgroup%
}
""",
  }],
# no section numbering: switch off section numbering in requirements
["""\
.. contents::

unnumbered section
------------------
""",
 {'body': r"""
\phantomsection\label{contents}
\pdfbookmark[1]{Contents}{contents}
\tableofcontents


\section{unnumbered section%
  \label{unnumbered-section}%
}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  '\\setcounter{secnumdepth}{0}\n',
  }],
# Docutils section numbering: switch off section numbering in requirements
["""\
.. contents::
.. sectnum::

first section
-------------
""",
 {'body': r"""
\phantomsection\label{contents}
\pdfbookmark[1]{Contents}{contents}
\tableofcontents


\section{1   first section%
  \label{first-section}%
}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  '\\setcounter{secnumdepth}{0}\n',
  }],
# LaTeX ToC with limited depth, no section numbers
["""\
.. contents::
    :depth: 1

first section
-------------
""",
 {'body': r"""
\phantomsection\label{contents}
\pdfbookmark[1]{Contents}{contents}
\setcounter{tocdepth}{1}
\tableofcontents


\section{first section%
  \label{first-section}%
}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  '\\setcounter{secnumdepth}{0}\n',
  }],
# local ToC reqires "minitoc" and \tableofcontents or \faketableofcontents
["""\
section with local ToC
======================

.. contents::
   :local:

section not in local toc
========================
""",
 {'body': r"""

\section{section with local ToC%
  \label{section-with-local-toc}%
}

\phantomsection\label{contents}
\mtcsettitle{secttoc}{}
\secttoc


\section{section not in local toc%
  \label{section-not-in-local-toc}%
}

\faketableofcontents % for local ToCs
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  '%% local table of contents\n'
                  '\\usepackage{minitoc}\n'
                  '\\dosecttoc\n'
                  '\\mtcsetdepth{secttoc}{5}\n'
                  '\\setcounter{secnumdepth}{0}\n'
  }],
# include images with "\includegraphics", load "graphicx" package
["""\
.. image:: blue%20square.png
.. image:: /images/vectors.svg
""",
 {'body': r"""
\includegraphics{blue square.png}

\includegraphics{/images/vectors.svg}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  '\\usepackage{graphicx}\n',
  }],
# table with caption
["""\
.. table:: Foo

   +-----+-----+
   |     |     |
   +-----+-----+
   |     |     |
   +-----+-----+
""",
 {'body': r"""
\setlength{\DUtablewidth}{\linewidth}%
\begin{longtable}{|p{0.075\DUtablewidth}|p{0.075\DUtablewidth}|}
\caption{Foo}\\
\hline
 &  \\
\hline
 &  \\
\hline
\end{longtable}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  + REQUIREMENTS_TABLE,
  }],
# borderless table
["""\
.. table::
   :class: borderless

   +-----+-----+
   |  1  |  2  |
   +-----+-----+
   |  3  |  4  |
   +-----+-----+
""",
 {'body': """
\\setlength{\\DUtablewidth}{\\linewidth}%
\\begin{longtable*}{p{0.075\\DUtablewidth}p{0.075\\DUtablewidth}}

1
 & \n\
2
 \\\\

3
 & \n\
4
 \\\\
\\end{longtable*}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  + REQUIREMENTS_TABLE
  }],
# table style "booktabs"
["""\
.. table::
   :class: booktabs

   +-----+-+
   |  1  |2|
   +-----+-+
""",
 {'body': """
\\setlength{\\DUtablewidth}{\\linewidth}%
\\begin{longtable*}{p{0.075\\DUtablewidth}p{0.028\\DUtablewidth}}
\\toprule

1
 & \n\
2
 \\\\
\\bottomrule
\\end{longtable*}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  '\\usepackage{booktabs}\n'
                  + REQUIREMENTS_TABLE
  }],
# collumn widths determined by LaTeX (via class argument)
["""\
.. table::
   :class: colwidths-auto

   +-----+-+
   |  1  |2|
   +-----+-+
""",
 {'body': r"""
\begin{longtable*}{|l|l|}
\hline
1 & 2 \\
\hline
\end{longtable*}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  + REQUIREMENTS_TABLE
  }],
# collumn widths determined by LaTeX (via "width" option)
["""\
.. table::
   :widths: auto

   +-----+-+
   |  1  |2|
   +-----+-+
""",
 {'body': r"""
\begin{longtable*}{|l|l|}
\hline
1 & 2 \\
\hline
\end{longtable*}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  + REQUIREMENTS_TABLE
  }],
# collumn widths specified via "width" option
["""\
.. table::
   :widths: 15, 30

   +-----+-----+
   |  1  |  2  |
   +-----+-----+
""",
 {'body': """
\\setlength{\\DUtablewidth}{\\linewidth}%
\\begin{longtable*}{|p{0.191\\DUtablewidth}|p{0.365\\DUtablewidth}|}
\\hline

1
 & \n\
2
 \\\\
\\hline
\\end{longtable*}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  + REQUIREMENTS_TABLE
  }],
# table alignment
["""\
.. table::
   :align: right

   +-----+-----+
   |  1  |  2  |
   +-----+-----+
""",
 {'body': """
\\setlength{\\DUtablewidth}{\\linewidth}%
\\begin{longtable*}[r]{|p{0.075\\DUtablewidth}|p{0.075\\DUtablewidth}|}
\\hline

1
 & \n\
2
 \\\\
\\hline
\\end{longtable*}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  + REQUIREMENTS_TABLE
  }],
# table with title row and empty cell
["""\
===== ======
Title
===== ======
entry value1
===== ======
""",
 {'body': """
\\setlength{\\DUtablewidth}{\\linewidth}%
\\begin{longtable*}{|p{0.075\\DUtablewidth}|p{0.086\\DUtablewidth}|}
\\hline
\\textbf{%
Title
} &  \\\\
\\hline
\\endfirsthead
\\hline
\\textbf{%
Title
} &  \\\\
\\hline
\\endhead
\\multicolumn{2}{p{0.16\\DUtablewidth}}{\\raggedleft\\ldots continued on next page}\\\\
\\endfoot
\\endlastfoot

entry
 & \n\
value1
 \\\\
\\hline
\\end{longtable*}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  + REQUIREMENTS_TABLE
  }],
# table with emtpy rowspanning cell
["""\
+----+----+
| c3 | c4 |
+----+----+
|         |
+---------+
""",
 {'body': """
\\setlength{\\DUtablewidth}{\\linewidth}%
\\begin{longtable*}{|p{0.063\\DUtablewidth}|p{0.063\\DUtablewidth}|}
\\hline

c3
 & \n\
c4
 \\\\
\\hline
\\multicolumn{2}{|p{0.13\\DUtablewidth}|}{} \\\\
\\hline
\\end{longtable*}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  + REQUIREMENTS_TABLE
  }],
# table with custom class value
["""\
.. table::
   :class: my-class

   +-----+-----+
   |  1  |  2  |
   +-----+-----+
   |  3  |  4  |
   +-----+-----+
""",
 {'body': """
\\begin{DUclass}{my-class}
\\setlength{\\DUtablewidth}{\\linewidth}%
\\begin{longtable*}{|p{0.075\\DUtablewidth}|p{0.075\\DUtablewidth}|}
\\hline

1
 & \n\
2
 \\\\
\\hline

3
 & \n\
4
 \\\\
\\hline
\\end{longtable*}
\\end{DUclass}
""",
  'fallbacks': r"""
% class handling for environments (block-level elements)
% \begin{DUclass}{spam} tries \DUCLASSspam and
% \end{DUclass}{spam} tries \endDUCLASSspam
\ifdefined\DUclass
\else % poor man's "provideenvironment"
  \newenvironment{DUclass}[1]%
    {% "#1" does not work in end-part of environment.
     \def\DocutilsClassFunctionName{DUCLASS#1}
     \csname \DocutilsClassFunctionName \endcsname}%
    {\csname end\DocutilsClassFunctionName \endcsname}%
\fi
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  + REQUIREMENTS_TABLE
  }],
# literal block
["""\
Test special characters { [ \\\\ ] } in literal block::

  { [ ( \\macro

  } ] )
""",
 {'body': r"""
Test special characters \{ {[} \textbackslash{} {]} \} in literal block:

\begin{quote}
\begin{alltt}
\{ [ ( \textbackslash{}macro

\} ] )
\end{alltt}
\end{quote}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  '\\usepackage{alltt}\n'
  }],
# raw block in compound directive
["""\
.. compound::

  Compound paragraph

  .. raw:: LaTeX

     raw LaTeX block

  compound paragraph continuation.
""",
 {'body': r"""
\begin{DUclass}{compound}
Compound paragraph
raw LaTeX block
compound paragraph continuation.
\end{DUclass}
""",
  'fallbacks': r"""
% class handling for environments (block-level elements)
% \begin{DUclass}{spam} tries \DUCLASSspam and
% \end{DUclass}{spam} tries \endDUCLASSspam
\ifdefined\DUclass
\else % poor man's "provideenvironment"
  \newenvironment{DUclass}[1]%
    {% "#1" does not work in end-part of environment.
     \def\DocutilsClassFunctionName{DUCLASS#1}
     \csname \DocutilsClassFunctionName \endcsname}%
    {\csname end\DocutilsClassFunctionName \endcsname}%
\fi
""",
  }],
# titles with inline markup
["""\
This is the *Title*
===================

This is the *Subtitle*
----------------------

This is a *section title*
~~~~~~~~~~~~~~~~~~~~~~~~~

This is the *document*.
""",
 {'body': r"""

\section{This is a \emph{section title}%
  \label{this-is-a-section-title}%
}

This is the \emph{document}.
""",
  'body_pre_docinfo': '\\maketitle\n',
  'fallbacks': r"""
% subtitle (in document title)
\providecommand*{\DUdocumentsubtitle}[1]{{\large #1}}
""",
  'pdfsetup': DEFAULT_PARTS['pdfsetup'] + r"""\hypersetup{
  pdftitle={This is the Title},
}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  '\\setcounter{secnumdepth}{0}\n',
  'subtitle': 'This is the \\emph{Subtitle}',
  'title': 'This is the \\emph{Title}',
  'titledata': r"""\title{This is the \emph{Title}%
  \label{this-is-the-title}%
  \\%
  \DUdocumentsubtitle{This is the \emph{Subtitle}}%
  \label{this-is-the-subtitle}}
\author{}
\date{}
"""
  }],
# template
["""\
""",
 {'body': '',
  'requirements': '\\usepackage[T1]{fontenc}\n'
  }],
# bibliographic fields
["""
:contact: here@home
:organization: Example & Cie.
:author:  Mr. Smith
:date:    yesterday
:address: 0231 Abendglanz
          Milky Way 23 b
""",
 {'requirements': '\\usepackage[T1]{fontenc}\n'
                  '\\usepackage{tabularx}\n',
  'fallbacks': r"""
% Provide a length variable and set default, if it is new
\providecommand*{\DUprovidelength}[2]{%
  \ifdefined#1
  \else
    \newlength{#1}\setlength{#1}{#2}%
  \fi
}

% width of docinfo table
\DUprovidelength{\DUdocinfowidth}{0.9\linewidth}
""",
  'pdfsetup': DEFAULT_PARTS['pdfsetup']
  + '\\hypersetup{\n  pdfauthor={Mr. Smith}\n}\n',
  'docinfo': r"""
% Docinfo
\begin{center}
\begin{tabularx}{\DUdocinfowidth}{lX}
\textbf{Contact}: & \href{mailto:here@home}{here@home} \\
\textbf{Organization}: & Example \& Cie. \\
\textbf{Author}: & Mr. Smith \\
\textbf{Date}: & yesterday \\
\textbf{Address}: & {\raggedright
0231 Abendglanz\\
Milky Way 23 b} \\
\end{tabularx}
\end{center}
""",
  }],
["""
:authors: * \\A. *Smith*
          * \\B. Miller
:organization: Example & Cie.
:author: C. Baker
:organization: Another Example
""",
 {'requirements': '\\usepackage[T1]{fontenc}\n'
                  '\\usepackage{tabularx}\n',
  'fallbacks': r"""
% Provide a length variable and set default, if it is new
\providecommand*{\DUprovidelength}[2]{%
  \ifdefined#1
  \else
    \newlength{#1}\setlength{#1}{#2}%
  \fi
}

% width of docinfo table
\DUprovidelength{\DUdocinfowidth}{0.9\linewidth}
""",
  'pdfsetup': DEFAULT_PARTS['pdfsetup']
  + '\\hypersetup{\n  pdfauthor={A. Smith; B. Miller; C. Baker}\n}\n',
  'docinfo': r"""
% Docinfo
\begin{center}
\begin{tabularx}{\DUdocinfowidth}{lX}
\textbf{Authors}: & A. \emph{Smith}, B. Miller \\
\textbf{Organization}: & Example \& Cie. \\
\textbf{Author}: & C. Baker \\
\textbf{Organization}: & Another Example \\
\end{tabularx}
\end{center}
""",
  }],
])

samples['book'] = ({'documentclass': 'book'}, [
# Top section level in LaTeX "book" class is 0 (chapter)
["""\
.. contents::
    :depth: 1

first chapter
-------------
""",
 {'body': r"""
\phantomsection\label{contents}
\pdfbookmark[1]{Contents}{contents}
\setcounter{tocdepth}{0}
\tableofcontents


\chapter{first chapter%
  \label{first-chapter}%
}
""",
  'head_prefix': '\\documentclass[a4paper]{book}\n',
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  '\\setcounter{secnumdepth}{-1}\n',
  }],
])

samples['booktabs'] = ({'table_style': ['booktabs']}, [
# column width determined by LaTeX
["""\
.. table::
   :widths: auto

   +-----+-+
   |  1  |2|
   +-----+-+
""",
 {'body': r"""
\begin{longtable*}{ll}
\toprule
1 & 2 \\
\bottomrule
\end{longtable*}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  '\\usepackage{booktabs}\n'
                  + REQUIREMENTS_TABLE
  }],
# column widhts specified via option
["""\
.. table::
   :widths: 15, 30

   +-----+-----+
   |  1  |  2  |
   +-----+-----+
""",
 {'body': """
\\setlength{\\DUtablewidth}{\\linewidth}%
\\begin{longtable*}{p{0.191\\DUtablewidth}p{0.365\\DUtablewidth}}
\\toprule

1
 & \n\
2
 \\\\
\\bottomrule
\\end{longtable*}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  '\\usepackage{booktabs}\n'
                  + REQUIREMENTS_TABLE
  }],
# borderless overrides "booktabs" table_style
["""\
.. table::
   :class: borderless

   +-----+-----+
   |  1  |  2  |
   +-----+-----+
   |  3  |  4  |
   +-----+-----+
""",
 {'body': """
\\setlength{\\DUtablewidth}{\\linewidth}%
\\begin{longtable*}{p{0.075\\DUtablewidth}p{0.075\\DUtablewidth}}

1
 & \n\
2
 \\\\

3
 & \n\
4
 \\\\
\\end{longtable*}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  + REQUIREMENTS_TABLE
  }],

])


samples['colwidths_auto'] = ({'table_style': ['colwidths-auto']}, [
# borderless table with auto-width columns
["""\
.. table::
   :class: borderless

   +-----+-----+
   |  1  |  2  |
   +-----+-----+
   |  3  |  4  |
   +-----+-----+
""",
 {'body': r"""
\begin{longtable*}{ll}
1 & 2 \\
3 & 4 \\
\end{longtable*}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  + REQUIREMENTS_TABLE
  }],
# booktabs style table with auto-width columns
["""\
.. table::
   :class: booktabs

   +-----+-+
   |  1  |2|
   +-----+-+
""",
 {'body': r"""
\begin{longtable*}{ll}
\toprule
1 & 2 \\
\bottomrule
\end{longtable*}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  '\\usepackage{booktabs}\n'
                  + REQUIREMENTS_TABLE
  }],
# given width overrides "colwidth-auto"
["""\
.. table::
   :widths: 15, 30

   +-----+-----+
   |  1  |  2  |
   +-----+-----+
""",
 {'body': """
\\setlength{\\DUtablewidth}{\\linewidth}%
\\begin{longtable*}{|p{0.191\\DUtablewidth}|p{0.365\\DUtablewidth}|}
\\hline

1
 & \n\
2
 \\\\
\\hline
\\end{longtable*}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  + REQUIREMENTS_TABLE
  }],
])

samples['Docutils ToC and sectnum'] = ({'use_latex_toc': False}, [
["""\
.. contents:: Table of Contents

Title 1
=======
Paragraph 1.

Title 2
-------
Paragraph 2.
""",
 {'body': r"""
\phantomsection\label{table-of-contents}
\pdfbookmark[1]{Table of Contents}{table-of-contents}

\begin{DUclass}{contents}

\DUtitle{Table of Contents}

\begin{itemize}
\item \hyperref[title-1]{Title 1}

\begin{itemize}
\item \hyperref[title-2]{Title 2}
\end{itemize}
\end{itemize}
\end{DUclass}


\section{Title 1%
  \label{title-1}%
}

Paragraph 1.


\subsection{Title 2%
  \label{title-2}%
}

Paragraph 2.
""",
  'fallbacks': r"""
% class handling for environments (block-level elements)
% \begin{DUclass}{spam} tries \DUCLASSspam and
% \end{DUclass}{spam} tries \endDUCLASSspam
\ifdefined\DUclass
\else % poor man's "provideenvironment"
  \newenvironment{DUclass}[1]%
    {% "#1" does not work in end-part of environment.
     \def\DocutilsClassFunctionName{DUCLASS#1}
     \csname \DocutilsClassFunctionName \endcsname}%
    {\csname end\DocutilsClassFunctionName \endcsname}%
\fi

% title for topics, admonitions, unsupported section levels, and sidebar
\providecommand*{\DUtitle}[1]{%
  \smallskip\noindent\textbf{#1}\smallskip}

\providecommand*{\DUCLASScontents}{%
  \renewenvironment{itemize}%
    {\begin{list}{}{\setlength{\partopsep}{0pt}
                    \setlength{\parsep}{0pt}}
                   }%
    {\end{list}}%
}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  '\\setcounter{secnumdepth}{0}\n',
  }],
])

samples['LaTeX docinfo'] = ({'use_latex_docinfo': True}, [
# bibliographic fields
["""
:contact: here@home
:organization: Example & Cie.
:author:  Mr. Smith
:date:    yesterday
:address: 0231 Abendglanz
          Milky Way 23 b
""",
 {'pdfsetup': DEFAULT_PARTS['pdfsetup']
  + '\\hypersetup{\n  pdfauthor={Mr. Smith}\n}\n',
  'titledata': r"""\title{}
\author{Mr. Smith\\
\href{mailto:here@home}{here@home}\\
Example \& Cie.\\
0231 Abendglanz\\
Milky Way 23 b}
\date{yesterday}
""",
  'body_pre_docinfo': '\\maketitle\n',
  }],
["""
:authors: * \\A. *Smith*
          * \\B. Miller
:organization: Example & Cie.
:author: C. Baker
:organization: Another Example
""",
 {'pdfsetup': DEFAULT_PARTS['pdfsetup']
  + '\\hypersetup{\n  pdfauthor={A. Smith; B. Miller; C. Baker}\n}\n',
  'titledata': r"""\title{}
\author{A. \emph{Smith} \quad B. Miller\\
Example \& Cie. \and
C. Baker\\
Another Example}
\date{}
""",
  'body_pre_docinfo': '\\maketitle\n',
  }],
["""
:keywords: custom, docinfo, field
""",
 {'requirements': '\\usepackage[T1]{fontenc}\n'
                  '\\usepackage{tabularx}\n',
  'fallbacks': r"""
% Provide a length variable and set default, if it is new
\providecommand*{\DUprovidelength}[2]{%
  \ifdefined#1
  \else
    \newlength{#1}\setlength{#1}{#2}%
  \fi
}

% width of docinfo table
\DUprovidelength{\DUdocinfowidth}{0.9\linewidth}
""",
  'docinfo': r"""
% Docinfo
\begin{center}
\begin{tabularx}{\DUdocinfowidth}{lX}
\textbf{keywords}: &
custom, docinfo, field
\\
\end{tabularx}
\end{center}
""",
  }],
])


samples['embed_stylesheet'] = ({'stylesheet_path': f'{spam},{ham}',
                                'embed_stylesheet': True,
                                'warning_stream': ''}, [
['two stylesheets embedded in the header',
 {'body': '\ntwo stylesheets embedded in the header\n',
  'stylesheet': f"""\
% Cannot embed stylesheet:
%  [Errno 2] No such file or directory: {spampath}
% embedded stylesheet: {ham}
\\newcommand{{\\ham}}{{wonderful ham}}

""",
  }],
])


# section numbering by LaTeX
samples['sectnum_xform False'] = ({'sectnum_xform': False,
                                   # ignore str values of internal settings:
                                   'sectnum_start': '42',
                                   'sectnum_depth': '3'
                                   }, [
["""\
no sectnum directive -> suppress section numbers

section
-------
""",
 {'body': r"""
no sectnum directive -> suppress section numbers


\section{section%
  \label{section}%
}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  '\\setcounter{secnumdepth}{0}\n',
  }],
['no sectnum directive and no section -> no requirements',
 {'body': '\nno sectnum directive and no section -> no requirements\n'
  }],

["""\
default section numbers -> no requirements

.. sectnum::

section
-------
""",
 {'body': r"""
default section numbers -> no requirements


\section{section%
  \label{section}%
}
""",
  }],
["""\
section numbers with custom start and depth

.. sectnum::
   :start: 7
   :depth: 2

section
-------
""",
 {'body': r"""
section numbers with custom start and depth


\section{section%
  \label{section}%
}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  '\\setcounter{secnumdepth}{2}\n'
                  '\\setcounter{section}{6}\n',
  }],
])

samples['stylesheet_path'] = ({'stylesheet_path': f'{spam},{ham}'}, [
['two stylesheet links in the header',
 {'body': '\ntwo stylesheet links in the header\n',
  'stylesheet': f'\\usepackage{{{spam}}}\n'
                f'\\input{{{ham}}}\n'
  }],
])

# if "svg" package is listed, include SVG images with "\includesvg"
samples['svg-image'] = ({'stylesheet': 'svg'}, [
["""\
.. image:: blue%20square.png
.. image:: /images/vectors.svg
""",
 {'body': r"""
\includegraphics{blue square.png}

\includesvg{/images/vectors.svg}
""",
  'requirements': '\\usepackage[T1]{fontenc}\n'
                  '\\usepackage{graphicx}\n',
  'stylesheet': '\\usepackage{svg}\n'
  }],
])

# TODO: test for quote replacing if the language uses "ASCII-quotes"
# as active character (e.g. de (ngerman)).


if __name__ == '__main__':
    unittest.main()

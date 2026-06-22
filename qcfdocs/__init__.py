"""qcfinancial-docs: notebook -> markdown -> branded static-site toolchain.

Two stages, exposed via the ``qcf-docs`` CLI:

* ``notebooks`` -- regenerate ``docs/*.md`` from the chapter ``.ipynb`` with nbconvert.
* ``build``     -- convert ``docs/*.md`` into the branded static site under ``site/``.

The site converter (:mod:`qcfdocs.convert`) is a 1:1 port of
``new-site/transform.reference.js`` and depends only on the standard library.
"""

__version__ = "0.1.0"

==================
bgetem.praevention
==================

Contenttypes and Browserviews for Knowledge-Management

Installation
============

Please clone this repo to your src-directory of your buildout and then do the following changes in your buildout.cfg.

::

    [buildout]

    find-links +=
               ...
               http://dev.bg-kooperation.de/pypi/simple

    eggs +=
         ...
         uvc.plone
         uvc.api
         bgetem.praevention

    zcml +=
         ...
         uvc.plone
         uvc.api
         bgetem.praevention

    develop +=
         ...
         src/bgetem.praevention

    [versions]
    ...
    zeam.form.base = 1.2.3
    zeam.form.ztk = 1.2.3


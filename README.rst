######################################################################
pyradiri: a pyramid of metadata for directories
######################################################################

:release:       0.0.0.dev0
:date:          2017-03-20 22:43:32
:home:          https://github.com/JRCSTU/pyradiri/
:keywords:      metadata, filesystem, database, hierarchical
:copyright:     2017 European Commission (`JRC <https://ec.europa.eu/jrc/>`_)
:license:       `EUPL 1.1+ <https://joinup.ec.europa.eu/software/page/eupl>`_

*pyradiri* is a CRUD application for hierarchical folder metadata based on a JSON-schema & YAML.

At the momment, validating a schema is the only capability supported by main-command
``pyradiri [file-1] ...``.  Provide no arguments or `-` to process *STDIN*.
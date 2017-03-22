# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright 2017 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl


import sys


__package__ = 'pyradiri'  # @ReservedAssignment pep-366


def main(args=sys.argv):
    from . import validate_yaml_files
    files = args[1:]

    validate_yaml_files(*files)


if __name__ == '__main__':
    main()

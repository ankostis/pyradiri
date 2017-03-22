# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright 2017 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl

import sys

import jsonschema
import pkg_resources

from ruamel import yaml  # @UnresolvedImport


def parse_yaml(finp, drop_comments=False):
    return yaml.load(finp, yaml.Loader if drop_comments else yaml.RoundTripLoader)


def validate_yaml_files(*files):
    with pkg_resources.resource_stream(__name__, 'schema.yaml') as finp:  # @UndefinedVariable
        schema_dict = parse_yaml(finp, True)
    schema = jsonschema.Draft4Validator(schema_dict)

    ## When no files given,. parse STDIN.
    #
    if not files:
        files = ('-', )

    for f in files:
        if f == '-':
            txt = parse_yaml(sys.stdin)
        else:
            with open(f, 'rt') as fp:
                txt = parse_yaml(fp)

        if not txt:
            raise ValueError('Empty file!')

        err_header = '#' * 72
        print(('\n\n%s\n' % err_header).join(str(s) for s in schema.iter_errors(txt)))

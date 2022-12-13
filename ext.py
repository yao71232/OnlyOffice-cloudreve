#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File    : ext.py
from os.path import abspath, dirname, join
from sanic.response import html
from jinja2 import Environment, FileSystemLoader

base_dir = abspath(dirname(__file__))
templates_dir = join(base_dir, 'templates')
jinja_env = Environment(loader=FileSystemLoader(templates_dir), autoescape=True)


def render_template(template_name: str, **context):
    template = jinja_env.get_template(template_name)
    return html(template.render(**context))

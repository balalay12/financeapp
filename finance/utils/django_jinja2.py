# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals

import datetime
import time

import six
from compressor.contrib.jinja2ext import CompressorExtension
from django.conf import settings
from django.core.urlresolvers import NoReverseMatch
from django.core.urlresolvers import reverse
from django.template import defaultfilters
from django.templatetags.static import static
from django.utils.translation import ugettext_lazy
from jinja2 import Environment, PackageLoader, ChoiceLoader
from jinja2.exceptions import TemplateNotFound


def _(text):
    return ugettext_lazy(unicode(text))


def url(*args, **kwargs):
    try:
        path = reverse(*args, **kwargs)
    except NoReverseMatch:
        path = "#"
    return path


class ExtensionLoader(PackageLoader):
    def __init__(self, *args, **kwargs):
        self.extensions = kwargs.pop("extensions", [])
        self.excludes = kwargs.pop("exclude", [])
        if self.extensions and self.excludes:
            raise EnvironmentError("Extensions or exclude, not together")
        super(ExtensionLoader, self).__init__(*args, **kwargs)

    def get_source(self, environment, template):
        extension = template.rsplit(".", 1)[-1]
        if not extension:
            raise TemplateNotFound(template)
        if self.extensions and extension not in self.extensions:
            raise TemplateNotFound(template)
        if self.excludes and extension in self.excludes:
            raise TemplateNotFound(template)
        return super(ExtensionLoader, self).get_source(environment, template)


def environment(**options):
    loaders = []

    for app in getattr(settings, 'INSTALLED_APPS', []):
        loaders.append(ExtensionLoader(app, exclude=["html"]))

    env_kwargs = {
        'extensions': ['jinja2.ext.loopcontrols', 'jinja2.ext.with_', CompressorExtension],
        'line_comment_prefix': '# ',
        'loader': ChoiceLoader(loaders),
        'trim_blocks': True,
        'autoescape': True,
        'auto_reload': True,
        'cache_size': 1024
    }
    env_kwargs.update(getattr(settings, 'JINJA_ENVIRONMENT', {}))
    env = Environment(**env_kwargs)
    env.globals = {
        'url': url,
        'range': six.moves.range,
        'static': static,
        "_": _,
        "enumerate": enumerate,
        "utc_now": datetime.datetime.utcnow(),
        "timestamp": time.mktime(datetime.datetime.utcnow().timetuple())
    }

    env.globals.update(dict(
        all=all,
        unicode=str,
        isinstance=isinstance,
        format=format,
        sorted=sorted,
        min=min,
        max=max,
        zip=zip,
        pow=pow,
        divmod=divmod,
        map=map,
        str=str,
    ))

    env.globals.update(getattr(settings, 'JINJA_GLOBALS', {}))

    for f in ('capfirst', 'linebreaks', 'linebreaksbr', 'linenumbers',
              'pluralize', 'slugify', 'striptags',
              'timesince', 'timeuntil', 'title', 'truncatewords',
              'truncatewords_html', 'unordered_list', 'urlize',
              'urlizetrunc', 'yesno'):
        env.filters[f] = getattr(defaultfilters, f)
    env.filters['format_date'] = defaultfilters.date
    env.filters.update(getattr(settings, 'JINJA_FILTERS', {}))
    return env


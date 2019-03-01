"""Markdown Exporter class"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from traitlets import default
from traitlets.config import Config

from .templateexporter import TemplateExporter


class MarkdownExporter(TemplateExporter):
    """
    Exports to a markdown document (.md)
    """
    export_from_notebook = "markdown"

    @default('file_extension')
    def _file_extension_default(self):
        return '.md'

    @default('template_file')
    def _template_file_default(self):
        return 'markdown.tpl'

    output_mimetype = 'text/markdown'

    @default('raw_mimetypes')
    def _raw_mimetypes_default(self):
        return ['text/markdown', 'text/html', '']

    @property
    def default_config(self):
        c = Config({
            'ExtractOutputPreprocessor': {'enabled': True},
            'NbConvertBase': {
                'display_data_priority': ['text/html',
                                          'text/markdown',
                                          'image/svg+xml',
                                          'text/latex',
                                          'image/png',
                                          'image/jpeg',
                                          'text/plain'
                                          ]
            },
            'HighlightMagicsPreprocessor': {
                'enabled':True
                },
        })
        c.merge(super(MarkdownExporter, self).default_config)
        return c

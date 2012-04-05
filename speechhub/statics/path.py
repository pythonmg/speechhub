"""
    Speechhub - A static blog engine
    Copyright (C) 2012  Antonio Ribeiro

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os


STATIC_PATH = os.path.dirname(os.path.abspath( __file__ ))

EMPTY_INDEX_TEMPLATE = os.path.join(STATIC_PATH,'empty-index.mustache')
INDEX_TEMPLATE = os.path.join(STATIC_PATH,'index.mustache')
INITIAL_CONFIG_FILE = os.path.join(STATIC_PATH,'initial_config_file.json')
PAGINATOR_TEMPLATE = os.path.join(STATIC_PATH,'paginator.mustache')
BASIC_CSS = os.path.join(STATIC_PATH,'basic_style.css')
DISQUS_TEMPLATE = os.path.join(STATIC_PATH,'disqus.mustache')
RAINBOW_JS = os.path.join(STATIC_PATH,'rainbow-custom.min.js')
RAINBOW_GITHUB_THEME = os.path.join(STATIC_PATH,'rainbow_github_theme.css')

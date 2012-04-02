import os


STATIC_PATH = os.path.dirname(os.path.abspath( __file__ ))

EMPTY_INDEX_TEMPLATE = os.path.join(STATIC_PATH,'empty-index.mustache')
INDEX_TEMPLATE = os.path.join(STATIC_PATH,'index.mustache')
INITIAL_CONFIG_FILE = os.path.join(STATIC_PATH,'initial_config_file.json')
PAGINATOR_TEMPLATE = os.path.join(STATIC_PATH,'paginator.mustache')
BASIC_CSS = os.path.join(STATIC_PATH,'basic_style.css')
DISQUS_TEMPLATE = os.path.join(STATIC_PATH,'disqus.mustache')

import os
import shutil

import pystache

from statics import path
from exceptions import *


def create_blog_structure(blog_path,blog_config):

    """ Initial blog structure:
        .
        ├── config
        ├── index.html
        ├── pages
        ├── posts
        └── static
            └── css
    """
    
    if not os.listdir(blog_path):
        raise NotEmptyFolderError()

    os.makedirs(os.path.join(blog_path,'posts'))
    os.makedirs(os.path.join(blog_path,'static'))
    os.makedirs(os.path.join(blog_path,'statc/css'))
    os.makedirs(os.path.join(blog_path,'pages'))
    os.makedirs(os.path.join(blog_path,'config'))

    create_empty_index(blog_path,blog_config)


def create_empty_index(blog_path,blog_config):

    index_template = open(path.EMPTY_INDEX_TEMPLATE).read()

    with open(os.path.join(blog_path,'index.html'),'w') as index_file:
        index_content = pystache.render(index_template,blog_config)
        index_file.write(index_content)

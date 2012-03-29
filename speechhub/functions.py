# -*- coding: utf-8 -*-

import os
import shutil
import json

import pystache

from statics import path
from exceptions import *


def create_blog(args):
    path = args['path'] or os.getcwd()
    args['path'] = path
    config_struct = get_initial_config_file(args)
    create_blog_structure(path,config_struct)



def create_blog_structure(blog_path,config_struct):

    """ Initial blog structure:
        .
        ├── config
        ├── index.html
        ├── pages
        ├── posts
        └── static
            └── css
    """
    os.makedirs(os.path.join(blog_path,'posts'))
    os.makedirs(os.path.join(blog_path,'static'))
    os.makedirs(os.path.join(blog_path,os.path.join('static','css')))
    os.makedirs(os.path.join(blog_path,'pages'))
    os.makedirs(os.path.join(blog_path,'config'))
    create_empty_index(blog_path,config_struct)

    with open(os.path.join(os.path.join(blog_path,'config'),'config.json'),'w') as config_file:
        json.dump(config_struct,config_file)


def create_empty_index(blog_path,config_struct):

    index_template = open(path.EMPTY_INDEX_TEMPLATE).read()

    with open(os.path.join(blog_path,'index.html'),'w') as index_file:
        index_content = pystache.render(index_template,config_struct)
        index_file.write(index_content)


def get_initial_config_file(args):
    config_struct = json.load(open(path.INITIAL_CONFIG_FILE))
    config_struct['path'] = args['path']
    config_struct['url'] = args['blog_url']
    config_struct['blog_name'] = args['blog_name']
    config_struct['username'] = args['username']
    config_struct['email'] = args['email']
    return config_struct


def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug.
    Originally from:
    http://flask.pocoo.org/snippets/5/
    Generating Slugs
    By Armin Ronacher filed in URLs
    """
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))

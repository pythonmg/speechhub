# -*- coding: utf-8 -*-
import re
import os
import sys
import time
import json
import shutil

import pystache
from markdown import markdown

from statics import path
from exc import DuplicatedPostNameError, NotASpeechhubProjectFolderErro, PostNotFoundError

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
FOLDER_SEPARATOR = os.sep


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
    config_struct['url'] = args['blog_url'][0] if args['blog_url'] else None
    config_struct['blog_name'] = args['blog_name'][0] if args['blog_name'] else None
    config_struct['username'] = args['username'][0] if args['username'] else None
    config_struct['email'] = args['email'][0] if args['email'] else None
    return config_struct


def new_post(args):
    post_title = args['post_title'][0]

    LOCAL_PATH = os.getcwd()

    try:
        config_file = open(os.path.join(LOCAL_PATH,'config/config.json'))
    except IOError:
        sys.stderr.write('You are not inside a SpeechHub project directory.\n')
        return

    post_file_name = slugify(post_title) + time.strftime("%Y-%b-%d")
    author = json.load(config_file)['username']

    if os.path.exists(os.path.join(LOCAL_PATH,'posts%s%s.md' % (FOLDER_SEPARATOR,post_file_name))):
        raise DuplicatedPostNameError()

    with open(os.path.join(LOCAL_PATH,'posts%s%s.md' % (FOLDER_SEPARATOR,post_file_name)),'w') as post_file:
        post_file.write("Fill it!")

    with open(os.path.join(LOCAL_PATH,'posts%s%s.meta.json' % (FOLDER_SEPARATOR,post_file_name)),'w') as post_meta:
        meta = {"date":time.asctime(),
                "post_title":post_title,
                "post_file_name":post_file_name + '.md',
                "post_author":author,
                "published":False,
                }
        json.dump(meta,post_meta)

    print "Post '%s' created. To fill it with something brillant please edit the file '%s'" % (post_title,post_file_name)


def parse_post(post_file_name):

    meta_file_name = '.'.join(post_file_name.split('.')[:-1]) + '.meta.json'

    post_content = open(post_file_name).read()
    meta_content = json.load(open(meta_file_name))

    parsed_post = markdown(post_content)

    return {'date':meta_content['date'],
            'post':parsed_post,
            'author':meta_content['post_author'],
            'title':meta_content['post_title'],
            }


def get_posts_for_page(posts_folder,page=1,posts_per_page=5):

    meta_posts = [os.path.join(posts_folder,f) for f in os.listdir(posts_folder) if f.endswith('.meta.json')]
    meta_posts = [(json.load(open(f))['date'],json.load(open(f))['post_file_name']) for f in meta_posts if json.load(open(f))['published']]

    meta_posts.sort(key=lambda f : time.strptime(f[0]),reverse=True)

    return [f[1] for f in meta_posts[(page-1)*posts_per_page:page*posts_per_page]]


def create_index(config):

    posts_folder = os.path.join(config['path'],'posts')
    posts_at_index = get_posts_for_page(posts_folder,posts_per_page=config['posts_per_page'])
    
    posts = [parse_post(os.path.join(posts_folder,post_file_name)) for post_file_name in posts_at_index]

    paginator = create_paginator(0)

    page_content = {'posts':posts,
                    'blog_name':config['blog_name'],
                    # 'blog_description':config['blog_description'], #TODO!
                    'paginator':paginator,
                    }

    index_template = open(path.INDEX_TEMPLATE).read()
    with open(os.path.join(config['path'],'index.html'),'w') as index_file:
        index_content = pystache.render(index_template,page_content)
        index_file.write(index_content)


def create_paginator(page):
    
    numbers = filter(lambda n : n >= 1, range(page-5,page+6))
    content = {'pages':[{'number':n,'link':'page/page%s.html' % n} for n in numbers if n > 1]}

    if 1 in numbers:
        content['pages'].insert(0,{'number':1,'link':'/blog'})
        
    paginator_template = open(path.PAGINATOR_TEMPLATE).read()
    paginator = pystache.render(paginator_template,content)

    return paginator


def rebuild_blog():

    config = get_config()
    create_index(config)


def publish_post(path):

    config = get_config()
    full_path = os.path.join(config['path'],path)

    if not os.path.exists(full_path):
        raise PostNotFoundError()

    if full_path.endswith('.md'):
        full_path = full_path[:-3] + '.meta.json'
    elif full_path.endswith('.meta.json'):
        pass #Dont worry, it is correct that way!
    else:
        raise PostNotFoundError()

    meta = json.load(open(full_path))
    meta['published'] = True
    json.dump(meta,open(full_path,'w'))

    rebuild_blog()


def get_config():
    LOCAL_PATH = os.getcwd()
    config_file_path = os.path.join(LOCAL_PATH,'config%sconfig.json' % FOLDER_SEPARATOR)

    if not os.path.exists(config_file_path):
        raise NotASpeechhubProjectFolderErro()

    config = json.load(open(config_file_path))

    return config


def update_config(config):
    LOCAL_PATH = os.getcwd()
    config_file_path = os.path.join(LOCAL_PATH,'config%sconfig.json' % FOLDER_SEPARATOR)

    if not os.path.exists(config_file_path):
        raise NotASpeechhubProjectFolderErro()

    json.dump(config,open(config_file_path,'w'))


def manage(args):
    if args['publish_post']:
        publish_post(args['publish_post'][0])


def admin(args):
    if args['update_path']:
        update_path(args['update_path'][0])


def update_path(path):
    config = get_config()
    config['path'] = os.path.abspath(os.path.expanduser(path))
    update_config(config)


def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug.
    Originally from:
    http://flask.pocoo.org/snippets/5/
    Generating Slugs
    By Armin Ronacher filed in URLs
    """
    result = []
    for word in _punct_re.split(text.lower()):
        word = word.encode('ascii')
        if word:
            result.append(word)
    return unicode(delim.join(result))


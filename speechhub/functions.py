# -*- coding: utf-8 -*-
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

import re
import os
import sys
import time
import math
import json
import shutil
import codecs

import pystache
from markdown import markdown
from unidecode import unidecode

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
    os.makedirs(os.path.join(blog_path,os.path.join('pages','permalinks')))
    os.makedirs(os.path.join(blog_path,'config'))
    copy_static_files(blog_path)
    create_empty_index(blog_path,config_struct)

    with open(os.path.join(os.path.join(blog_path,'config'),'config.json'),'w') as config_file:
        json.dump(config_struct,config_file)

def copy_static_files(blog_path):
    shutil.copy2(path.RAINBOW_JS,os.path.join(blog_path,'static'))
    shutil.copy2(path.BASIC_CSS,os.path.join(blog_path,os.path.join('static','css')))
    shutil.copy2(path.RAINBOW_GITHUB_THEME,os.path.join(blog_path,os.path.join('static','css')))

def create_empty_index(blog_path,config_struct):

    index_template = open(path.EMPTY_INDEX_TEMPLATE).read()

    with open(os.path.join(blog_path,'index.html'),'w') as index_file:
        index_content = pystache.render(index_template,config_struct)
        index_file.write(index_content)


def get_initial_config_file(args):
    config_struct = json.load(open(path.INITIAL_CONFIG_FILE))
    config_struct['path'] = args['path']
    config_struct['url'] = args['url'][0] if args['url'] else None
    config_struct['blog_name'] = args['blog_name'][0] if args['blog_name'] else None
    config_struct['username'] = args['username'][0] if args['username'] else None
    config_struct['email'] = args['email'][0] if args['email'] else None
    return config_struct


def new_post(args):
    post_title = args['title'][0].decode('utf-8')

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

    print u"Post '%s' created. To fill it with something brillant please edit the file '%s'" % (post_title,post_file_name)


def parse_post(config,post_file_name):

    meta_file_name = '.'.join(post_file_name.split('.')[:-1]) + '.meta.json'

    post = codecs.open(post_file_name,'r',encoding='utf-8')
    meta_content = json.load(open(meta_file_name))
    post_content = unicode(post.read())
    parsed_post = markdown(post_content)

    if config['debug']:
        url = config['path']
    else:
        url = config['url']

    return {'date':time.strftime(config['datetime-format'], time.strptime(meta_content['date'], "%a %b %d %H:%M:%S %Y")),
            'post':parsed_post,
            'author':meta_content['post_author'],
            'title':meta_content['post_title'],
            'relative_permalink':'pages/permalinks/'+meta_content['post_file_name'][:-3]+'.html',
            'url':url,
            }


def get_posts_for_page(published_posts,page=1,posts_per_page=5):

    return [f[1] for f in published_posts[(page-1)*posts_per_page:page*posts_per_page]]


def create_index(config):

    posts_folder = os.path.join(config['path'],'posts')
    posts_at_index = get_posts_for_page(config['published_posts'],posts_per_page=config['posts_per_page'])
    
    posts = [parse_post(config,os.path.join(posts_folder,post_file_name)) for post_file_name in posts_at_index]

    if config['debug']:
        url = config['path']
    else:
        url = config['url']

    paginator = create_paginator(0,len(config['published_posts']),config['posts_per_page'],url=url)

    page_content = {'posts':posts,
                    'blog_name':config['blog_name'],
                    'blog_description':config['blog_description'], #TODO!
                    'paginator':paginator,
                    'url':url,
                    'about_author':config['about_author'],
                    'contacts':config['contacts'],
                    'links':config['links'],
                    'css_file':config['css_file'],
                    'old_posts':get_permalinks_list(config),
                    'footage_content':config['footage_content'],
                    }

    index_template = open(path.INDEX_TEMPLATE).read()
    with codecs.open(os.path.join(config['path'],'index.html'),'w',encoding='utf-8') as index_file:
        index_content = pystache.render(index_template,page_content)
        index_file.write(unicode(index_content))


def create_paginator(page,number_of_posts,posts_per_page,url=''):

    last_page = int(math.ceil(float(number_of_posts) / posts_per_page))
    
    numbers = filter(lambda n : n >= 1, range(page-5,page+6))
    content = {'pages':[{'number':n,'link':'%s/pages/page%s.html' % (url,n)} for n in numbers if n > 1 and n <= last_page]}

    if 1 in numbers:
        content['pages'].insert(0,{'number':1,'link':'%s/index.html' % url})
        
    paginator_template = open(path.PAGINATOR_TEMPLATE).read()
    paginator = pystache.render(paginator_template,content)

    return paginator


def get_published_posts(posts_path):

    published_posts = []
    for f in os.listdir(posts_path):
        if f.endswith('.meta.json'):
            meta = json.load(open(os.path.join(posts_path,f)))
            if meta['published']:
                published_posts.append((meta['date'],meta['post_file_name'],meta['post_title']))
    
    published_posts.sort(key=lambda f : time.strptime(f[0]),reverse=True)

    return published_posts


def create_pages(config):

    number_of_pages = int(math.ceil(float(len(config['published_posts'])) / config['posts_per_page']))

    for n in range(2,number_of_pages+1):
        create_page(config,n)


def create_page(config,page_number):

    posts_folder = os.path.join(config['path'],'posts')
    posts_at_page = get_posts_for_page(config['published_posts'],posts_per_page=config['posts_per_page'],page=page_number)
    
    posts = [parse_post(config,os.path.join(posts_folder,post_file_name)) for post_file_name in posts_at_page]

    if config['debug']:
        url = config['path']
    else:
        url = config['url']

    paginator = create_paginator(page_number,len(config['published_posts']),config['posts_per_page'],url=url)

    page_content = {'posts':posts,
                    'blog_name':config['blog_name'],
                    'blog_description':config['blog_description'],
                    'paginator':paginator,
                    'url':url,
                    'about_author':config['about_author'],
                    'contacts':config['contacts'],
                    'links':config['links'],
                    'css_file':config['css_file'],
                    'old_posts':get_permalinks_list(config),
                    'footage_content':config['footage_content'],
                    }

    template = open(path.INDEX_TEMPLATE).read()
    
    with codecs.open(os.path.join(config['path'],'pages%spage%s.html' % (FOLDER_SEPARATOR,page_number)),'w',encoding='utf-8') as page:
        content = pystache.render(template,page_content)
        page.write(unicode(content))


def rebuild_blog(args={}):

    if args:
        if 'debug' in args or '--debug' in args:
            set_debug(True)
            print 'Your blog was built on debug mode!'
    else:
        set_debug(False)

    config = get_config()
    copy_static_files(config['path'])
    posts_path = os.path.join(config['path'],'posts')
    published_posts = get_published_posts(posts_path)
    config['published_posts'] = published_posts

    create_permalinks(config)
    create_index(config)
    create_pages(config)


def create_permalinks(config):
    for post in config['published_posts']:
        page_content = create_post_page(config,post[1])
        post_name = post[1][:-3] + '.html'
        with codecs.open(os.path.join(config['path'],'pages%spermalinks%s%s' % (FOLDER_SEPARATOR,FOLDER_SEPARATOR,post_name)),'w',encoding='utf-8') as page:
            page.write(unicode(page_content))


def get_permalinks_list(config):
    
    if config['debug']:
        url = config['path']
    else:
        url = config['url']

    base_url = url + '/pages/permalinks/'
    return [{'url':base_url+post[1][:-3]+'.html','title':post[2]} for post in config['published_posts']]


def create_post_page(config,post_file_name):
    project_path = config['path']
    posts_folder = os.path.join(project_path,'posts')
    
    post = [parse_post(config,os.path.join(posts_folder,post_file_name))]

    if config['debug']:
        url = config['path']
    else:
        url = config['url']

    if config['disqus']['enabled']:
        disqus_template = open(path.DISQUS_TEMPLATE).read()
        disqus_variables = config['disqus']
        disqus_variables.update({'disqus_url':url + '/pages/permalinks/' + post_file_name[:-3] + '.html',
                                 'disqus_identifier':post_file_name[:-3]})
        disqus = pystache.render(disqus_template,disqus_variables)
        disqus = unicode(disqus)
    else:
        disqus = ''
    page_content = {'posts':post,
                    'blog_name':config['blog_name'],
                    'blog_description':config['blog_description'],
                    'url':url,
                    'about_author':config['about_author'],
                    'contacts':config['contacts'],
                    'links':config['links'],
                    'css_file':config['css_file'],
                    'old_posts':get_permalinks_list(config),
                    'disqus':disqus,
                    'footage_content':config['footage_content'],
                    }

    template = open(path.INDEX_TEMPLATE).read()
    return pystache.render(template,page_content)
    

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
    if args['path']:
        update_path(args['path'][0])
    if args['url']:
        update_url(args['url'][0])


def update_url(url):
    config = get_config()
    config['url'] = url
    update_config(config)


def update_path(path):
    config = get_config()
    config['path'] = os.path.abspath(os.path.expanduser(path))
    update_config(config)


def set_debug(_debug):
    config = get_config()
    config['debug'] = _debug
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
        result.extend(unidecode(word).split())
    return unicode(delim.join(result))


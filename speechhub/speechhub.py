import os
import sys
import argparse

def admin_blog(args):
    parser = argparse.ArgumentParser(description='Speechhub is a simple command line static blog engine.')
    parser.add_argument('--username', metavar='username',
                                       type=str, 
                                       nargs='?',
                                       help='User name.',)
    parser.add_argument('--email', metavar='E-mail',
                                       type=str,
                                       nargs='?',
                                       help='User E-mail')
    parser.add_argument('--posts-per-page', metavar='posts-per-page.',
                                            type=int,
                                            nargs=1,
                                            default=5,
                                            help='How many posts by page you want to see.')
    parser.add_argument('--datetime-format', metavar='posts-per-page.',
                                             type=int,
                                             nargs=1,
                                             default='%D/%M/%A - %h%m%s',
                                             help='Date and time format. Use capitalized for date and not capitalized for time.')

    parsed_args = parser.parse_args(args)
    

def create_new_blog(args):
    parser = argparse.ArgumentParser(description='Speechhub is a simple command line static blog engine.')
    parser.add_argument('--blog-name', metavar='username',
                                       type=str, 
                                       nargs=1,
                                       help='Blog name.')
    parser.add_argument('--path', metavar='username',
                                       type=str, 
                                       nargs=1,
                                       help='Blog name.',)
    parser.add_argument('--blog-url', metavar='username',
                                       type=str, 
                                       nargs='?',
                                       help='User name.',)
    parser.add_argument('--username', metavar='username',
                                       type=str, 
                                       nargs='?',
                                       help='User name.',)
    parser.add_argument('--email', metavar='E-mail',
                                       type=str,
                                       nargs='?',
                                       help='User E-mail')
    
    parsed_args = parser.parse_args(args)
    print parsed_args


def create_new_post(args):
    parser = argparse.ArgumentParser(description='Speechhub is a simple command line static blog engine.')
    parser.add_argument('--post-title', metavar='title',
                                       type=str, 
                                       nargs=1,
                                       help='The title of your post.',)
    parsed_args = parser.parse_args(args)
    

def manage_blog(args):
    parser = argparse.ArgumentParser(description='Manage your posts.')
    parser.add_argument('--publish-post', metavar='path',
                                       type=str, 
                                       nargs='?',
                                       help='Publish the related post.',)
    parser.add_argument('--publish-post', metavar='path',
                                       type=str, 
                                       nargs='?',
                                       help='Publish the related post.',)
    parser.add_argument('--unpublish-post', metavar='path',
                                       type=str, 
                                       nargs='?',
                                       help='Unblish the related post.',)
    parser.add_argument('--delete-post', metavar='path',
                                       type=str, 
                                       nargs='?',
                                       help='Delete the related post.',)
    parsed_args = parser.parse_args(args)
    

def rebuild_blog():
    """ Rebuild the entire blog """
    pass


def main():

    if len(sys.argv) < 2:
        print 'usage:'
        return

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == 'create-blog':
        create_new_blog(args)
    elif command == 'admin':
        admin_blog(args)
    elif command == 'new-post':
        create_new_post(args)
    elif command == 'manage':
        manage_blog(args)
    elif command == 'rebuild':
        rebuild_blog()
    else:
        print 'usage:'
        return


if __name__=='__main__':
    main()

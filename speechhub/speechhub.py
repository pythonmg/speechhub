import sys
import argparse

def create_parser():
    parser = argparse.ArgumentParser(description='Speechhub is a simple command line static blog engine.')
    parser.add_argument('--create-blog', metavar='path', 
                                         type=str, 
                                         nargs='?',
                                         default=local_path,
                                         help='create a blog in a path')
    return parser
    

def main():
    parser = create_parser()
    parser.parse_args(sys.argv[1:])


if __name__=='__main__':
    local_path = os.path.abspath( sys.argv )
    main()
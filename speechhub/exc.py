
class SpeechhubException(BaseException):
    """ Parent class of all exceptions in Speechhub """

class NotEmptyFolderError(SpeechhubException):
    """ For this operation the folder must be empty """

class DuplicatedPostNameError(SpeechhubException):
    """ Already exists a post with this name today """

class NotASpeechhubProjectFolderErro(SpeechhubException):
    """ You are not on a Speechhub project folder """

class PostNotFoundError(SpeechhubException):
    """ This post was not found """
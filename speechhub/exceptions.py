
class SpeechhubException(BaseException):
    """ Parent class of all exceptions in Speechhub """

class NotEmptyFolderError(SpeechhubException):
    """ For this operation the folder must be empty """
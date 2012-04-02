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

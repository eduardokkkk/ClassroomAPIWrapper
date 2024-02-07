from typing import List
from discord import Embed, Color


class Post:
    """type for posts, including courseworks, materials and announcements."""
    def __init__(self, title: str, alternateLink: str, description: str=None, topicId: int=None, dueDate: dict=None):
        self.title = title
        self.description = description
        self.alternateLink = alternateLink
        self.topicId = topicId
        self.dueDate = dueDate


class Course:
    """type for courses/creating a course-like object from a dict."""
    def __init__(self, name: str = None, id: str=None, alternateLink: str = None):
        self.name = name
        self.__id = id
        self.alternateLink = alternateLink
    
    def getId(self) -> int:
        return self.__id
    
    def toEmbed(self):
        return Embed(
            title=self.name,
            color=Color.green()
        )
class Topic:
    """type for topics/course fields"""
    def __init__(self, name, id):
        self.name = name
        self.__id = id

    def getId(self) -> int:
        return self.__id


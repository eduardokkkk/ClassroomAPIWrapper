import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List
from ._types import Post, Course, Topic


        
"""
    quick tips
    
    1. If you want to change accounts/change the scopes, just delete the token.json file and run the script again
    
    2. In case you're still confused on how to use the API, here's an extremely useful video i found: https://www.youtube.com/watch?v=1WwLPcVaYxY

"""




class Classroom:
    def __init__(self, scopes = ['https://www.googleapis.com/auth/classroom.courses.readonly', 'https://www.googleapis.com/auth/classroom.course-work.readonly', 'https://www.googleapis.com/auth/classroom.coursework.me', 'https://www.googleapis.com/auth/classroom.topics.readonly', 'https://www.googleapis.com/auth/classroom.announcements.readonly', 'https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly', 'https://www.googleapis.com/auth/classroom.topics.readonly']):
        """
        Wrapper object for the Classroom API.

        Quickstart avaliable at https://github.com/googleworkspace/python-samples/blob/master/classroom/quickstart/quickstart.py
        """
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', scopes) 
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', scopes)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('classroom', 'v1', credentials=creds)
            self.service = service
        except HttpError as error:
            print('An error occurred: ' + error)
    

    def getCourses(self) -> List[Course] | None:
        """Returns all the courses the user is in."""
        results = self.service.courses().list(pageSize=10).execute()
        courses = results.get('courses', [])

        if not courses:
            return None
        
        final = []

        for course in courses:
            final.append(Course(name = course['name'], id = course['id'], alternateLink = course['alternateLink']))
            

        return final

    def getCourse(self, courseId) -> Course | None:
        """return course according to the ID provided."""
        course = self.service.courses().get(
        id = courseId).execute()
        return Course(name= course['name'], id = course['id'], alternateLink=course['alternateLink'])
    def getCourseTopics(self, course_id : int, page_token=None) -> List[Topic]:
        """Returns all topics within the course and their respective id."""
        final, topics = [], []
        while True:
            response = self.service.courses().topics().list(
            pageToken=page_token,
            pageSize=30,
            courseId=course_id).execute()
            topics.extend(response.get('topic', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break
        if not topics:
            return None
        for topic in topics:
            topic = Topic(name=topic['name'], id=topic['topicId'])
            final.append(topic)
        return final
    
    def getTopic(self, topic_id: int, course_id: int) -> Topic:
        """Returns a specific field from the course."""
        response = self.service.courses().topics().get(
            id=topic_id,
            courseId=course_id).execute()
        topic = Topic(name=response['name'], id=response['topicId'])
        return topic

    def getAnnouncements(self, course_id : int, page_token = None) -> List[Post]:
        """Returns the latest 5 announcements on the classroom."""
        posts, final = [], []
        while True:
            response = self.service.courses().announcements().list(
            pageToken=page_token,
            pageSize=1,
            courseId=course_id).execute()
            posts.extend(response.get('announcements', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break
        if not posts:
            return None
        
        while not len(final <= 5):
            for post in posts:
                post = Post(title=post['text'], id=post['id'])
                final.append(post)
            break
        return final
    

    def getCourseworks(self, course_id : int, page_token = None):
        """Returns the latest 5 courseworks on the classroom."""
        courseworks, final = [], []
        while True:
            response = self.service.courses().courseWork().list(
            pageToken=page_token,
            pageSize=1,
            courseId=course_id).execute() 
            courseworks.extend(response.get('courseWork', [])) 
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break

        if not courseworks:
            return None
        
        for coursework in courseworks:
            coursework = self.service.courses().courseWork().get(
            id = coursework['id'],
            courseId=course_id).execute()
            coursework = Post(title=coursework['title'], description=coursework['description'], link=coursework['alternateLink'], id=coursework['id'], dueDate=coursework['dueDate'] if 'dueDate' in coursework else None) 
            final.append(coursework)

        return final

    def getCoursework(self, coursework_id : int, course_id : int) -> Post:
        """Returns a specific coursework, according to the id."""
        response = self.service.courses().courseWork().get(
        id = coursework_id,
        courseId=course_id).execute() 
        return response

    def getMaterial(self, material_id: int, course_id: int) -> Post:
        material = self.service.courses().courseWorkMaterials().get(
            id = material_id,
            courseId = course_id
        ).execute()
        material= Post(title=material['title'], alternateLink=material['alternateLink'], description=material['description'], topicId=int(material['topicId']) if 'topicId' in material else None )
        return material   
    

    def getMaterials(self, course_id : int, topicId: int =None, page_token = None) -> List[Post]:
        """Returns the material-type courseworks on the course."""
        posts, final, has_topicId= [], [], []
        while True:
            response = self.service.courses().courseWorkMaterials().list(
            pageToken=page_token,
            pageSize=1,
            courseId=course_id).execute()
            posts.extend(response.get('courseWorkMaterial', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break

        if not posts:
            return None

        for post in posts:
            post = cr.getMaterial(material_id=post['id'], course_id=course_id)   
            if post.topicId == topicId and topicId:
                has_topicId.append(post)
            final.append(post)

        
        return has_topicId if topicId else final


cr = Classroom()


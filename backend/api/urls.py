
from django.urls import path
from .views import codingQuestionList,getcodingQuestion,\
    codeResult,getMcqQuestion,getMcqSubject,getLevel,registerUser,\
    loginUser,userCheck,run1stTestCase,mcqSession,mcqSessionGet,getSpecifiedUser
urlpatterns = [
# path('add/', run_code, name='add'),
path('codingQuestions/', codingQuestionList, name='codingQuestions'),
path('topic/', getMcqSubject, name='topic'),
path('codingQuestions/<str:pk>/', getcodingQuestion, name='codingQuestion'),
path('codingQuestions/<str:pk>/output/', codeResult, name='output'),
path('codingQuestions/<str:pk>/selfInput/', userCheck, name='selfInput'),
path('codingQuestions/<str:pk>/run1stTestCase/', run1stTestCase, name='run1stTestCase'),
path('signUp/', registerUser, name='signUp'),
path('login/', loginUser, name='signIn'),
path('mcq/<str:language>/<str:level>', getMcqQuestion, name='mcq'),
path('mcq/<str:bb>/<str:pk>/sessionStore', mcqSession, name='sessionstore'),
path('mcq/<str:language>/<str:level>/sessionget/<str:email>', mcqSessionGet, name='mcqSessionGet'),
path('mcq/<str:language>/', getLevel, name='level'),
path('user/<str:email>/<str:language>', getSpecifiedUser, name='getSpecifiedUser'),

]

from .views import ReadCertifcationSession, RetreiveSessionParticipantsForProtector, CertificationSessionView, CertificationSessionViewForProtector, CertificationSessionViewForStudent, RUDCertifcationSession, SessionStudentParticipationView, GetStudentSessions
from django.urls import path


urlpatterns = [
  
    path('', CertificationSessionView.as_view(), name='certificationsessions'),
    path('<int:pk>/', RUDCertifcationSession.as_view(), name='rud_sessions'),
    path('student/', CertificationSessionViewForStudent.as_view(), name='certificationsessions_student'),
    path('participate/<int:pk>/', SessionStudentParticipationView.as_view(), name="session_participation"),
    path('studentsessions/', GetStudentSessions.as_view(), name="student_sessions"),
    path('sessionsprot/', CertificationSessionViewForProtector.as_view(), name='certification_sessions_for_portector'),
    path('readsess/<int:pk>/', ReadCertifcationSession.as_view(), name='single_certification_session'),
    path('participants/<int:pk>/', RetreiveSessionParticipantsForProtector.as_view(), name='partcipants_on_sessions')
]
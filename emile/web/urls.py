from django.conf.urls import url, include
#from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.urls import static
from django.contrib.auth import views as auth_views

app_name = 'web'

urlpatterns = [
    url(r'^home/$', views.wall_messages_list, name='home'),
    url(r'^wall_messages_list/$', views.wall_messages_list, name='wall_messages_list'),
    url(r'^wall_message_create/(?P<id>[0-9]+)/$', views.WallMessageCreateView.as_view(), name='wall_messages_create'),
    url(r'^users/$', views.GetAllUsersWithDetails.as_view()),
    url(r'^update_user/$', views.UpdateUserWithDetails.as_view()),
    url(r'^webapp/$', auth_views.login, {'template_name': 'web/login.html'}, name='login2'),
    url(r'^login/$', views.GetUserWithDetails.as_view()),
    url(r'^logout2/$', auth_views.logout,{'template_name': 'web/logout.html'}, name='logout2'),
    url(r'^course_sections/$', views.GetUserCurseSections.as_view()),
    url(r'^token_register/$', views.RegistrarToken.as_view()),
    url(r'^sendMessageToStudentsOfACourseSection/$', views.SendWallMessagesToStudentsOfACourseSection.as_view()),
    url(r'^sendMessagesToStudentsOfATeacher/$', views.SendWallMessagesToStudentsOfATeacher.as_view()),
    url(r'^sendMessagesToTeachersOfAProgram/$', views.SendWallMessagesToTeachersOfAProgram.as_view()),
    url(r'^sendMessagesToStudentsOfAProgram/$', views.SendWallMessagesToStudentsOfAProgram.as_view()),
    url(r'^messages/(?P<id>[0-9]+)/$', views.GetAllWallMessagesOfUser.as_view()),
    url(r'^program/(?P<id>[0-9]+)/$', views.GetProgramOfACoordinator.as_view()),
    url(r'^searchMessage/(?P<id>[0-9]+)/(?P<seachstring>[^/]+)/$', views.SearchWallMessagesOfUser.as_view()),
    url(r'^imageUpload/(?P<id>[0-9]+)/$', views.AtualizarImagemPerfil.as_view()),
    url(r'^recoverPassword/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.PasswordRecover.as_view()),
    #url(r'^select2/', include('django_select2.urls')),
    #url(r'^user_details/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<password>[^/]+)/$', views.GetUserWithDetails.as_view()),
    #url(r'^teachers/$', views.GetAllTeachersWithDetails.as_view()),
    #url(r'^coordinators/$', views.GetAllCoordinatorsWithDetails.as_view()),
    #url(r'^login/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<password>[^/]+)/$', views.GetUserWithDetails.as_view()),
    #url(r'^programs/$', views.GetAllProgramsWithDetails.as_view()),
    #url(r'^programs_courses/(?P<id>[0-9]+)/$', views.GetAllProgramsCourses.as_view()),
    #url(r'^programs_course_sections/(?P<id>[0-9]+)/$', views.GetAllProgramsCourseSections.as_view()),
    #url(r'^programs_course_sections_teachers/(?P<id>[0-9]+)/$', views.GetAllTeachersPrograms.as_view()),
    #url(r'^course_section_details/(?P<id>[0-9]+)/$', views.GetCourseSectionWithDetails.as_view()),
    #url(r'^course_sections_students/(?P<course_section_id>[0-9]+)/$', views.GetAllStudentsInCourseSections.as_view()),
    ]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns = [
#    url(r'^admin/', admin.site.urls),
#    url(r'^', include('administracao.urls')),
#]

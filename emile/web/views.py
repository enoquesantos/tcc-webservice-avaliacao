from django.shortcuts import render
from .serializers import WallMessagesSerializer, InstitutionsSerializer, CourseSectionStudentsSerializer,UsersSerializer, StudentsSerializer, TeachersSerializer, ProgramSerializer, CourseSerializer, CourseSectionsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.pagination import PageNumberPagination
from django.http import Http404
from .models import WallMessages, Institution, Users, Students, Teachers, Program, CourseSections, Courses, CourseSectionStudents, Destinations
from django.db.models import Count
from django.conf import settings
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser, JSONParser
from pyfcm import FCMNotification
import random, os, json, requests
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from django.core.urlresolvers import reverse_lazy
from web import forms
from django.shortcuts import redirect
from rest_framework.renderers import JSONRenderer
from PIL import Image

def getUserMobile(request):
    try:
        usermobile = Teachers.objects.get(siape=request.user.username)
    except Teachers.DoesNotExist:
        try:
            usermobile = Students.objects.get(enrollment=request.user.username)
        except Students.DoesNotExist:
            raise Http404
    return usermobile

@login_required
def DefaultHomeApp(request):
    #print(request.user.username)
    try:
        usermobile = getUserMobile(request)
        #print(usermobile)
    except Users.DoesNotExist:
        raise Http404
    return render(request, 'web/base.html', {'permission':str(usermobile.user.permission), 'usermobile':usermobile})

@login_required
def wall_messages_list(request):
    try:
        usermobile = getUserMobile(request)
    except Users.DoesNotExist:
        raise Http404
    #print(usermobile.user.id)
    page = request.GET.get('page', 1)
    messages = WallMessages.objects.filter(destination=usermobile.user).order_by('-date')
    paginator = Paginator(messages, 5)
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    return render(request, 'web/wall_messages_list.html', {'messages':results,'usermobile':usermobile, 'permission':str(usermobile.user.permission)})


class WallMessageCreateView(View):
    template_name = 'web/wall_message_create.html'
    success_url = reverse_lazy('web:wall_messages_list')
    form_class = forms.MessageForm

    def get_object(self, id):
        try:
            return Users.objects.get(id=id)
        except Users.DoesNotExist:
            raise Http404

    def getAllStudentsOfAProgram(self, id): # Todos os Alunos de um Curso
        try:
            studends = Students.objects.filter(program=Program.objects.get(id=id))
            users = [student.user for student in studends]
            return users
        except Exception as e:
            print(e)

    def getAllTeachersOfAProgram(self, id): # Todos os Professores de um Curso
        try:
            programa=Program.objects.get(id=id)
            courses = Courses.objects.filter(program=programa)
            #students = [course_section_students.student for course_section_students in CourseSectionStudents.objects.filter(course_section=coursesections).annotate(Count('student'))]
            users = [coursesections.teacher.user for coursesections in CourseSections.objects.filter(course__in=courses)]
            my_list = list(set(users))
            #print(my_list)
            return my_list
        except Exception as e:
            print(e)

    def getStudentsOfACourseSection(self, course_section_id): # Alunos de uma Turma
        try:
            selected_course_section = CourseSections.objects.get(id=course_section_id)
            coursesectionstudents = CourseSectionStudents.objects.filter(course_section=selected_course_section)
            users = [course_section_students.student.user for course_section_students in coursesectionstudents]
            return users
        except Exception as e:
            print(e)

    def getStudentsOfATeacher(self, id): # Todos os meus alunos
        usuario = self.get_object(id)
        try:
            teacher  = Teachers.objects.get(user=usuario)
            coursesections =  CourseSections.objects.filter(teacher = teacher)
            users = [course_section_students.student.user for course_section_students in CourseSectionStudents.objects.filter(course_section=coursesections).annotate(Count('student'))]
            return users
        except Exception as e:
            print("Erro aqui no Teachers")
            print(e)

    def get(self, request,  id):
        usuario = Users.objects.get(id=id)
        destination_list = []
        for destination in usuario.permission.messagedestinations.all():
           destination_list.append((destination.id, destination.name),)

        teacher  = Teachers.objects.get(user=usuario)
        coursesections =  CourseSections.objects.filter(teacher = teacher)
        coursesections_list = []
        for coursesection in coursesections:
           coursesections_list.append((coursesection.id, coursesection.name),)
        form = self.form_class(destination_list,coursesections_list)
        return render(request, self.template_name, { 'form' : form, 'usermobile':teacher, 'permission':str(teacher.user.permission)})

    def post(self, request, id):
        usuario = Users.objects.get(id=id)
        destination_list = []
        for destination in usuario.permission.messagedestinations.all():
           destination_list.append((destination.id, destination.name),)

        teacher  = Teachers.objects.get(user=usuario)
        coursesections =  CourseSections.objects.filter(teacher = teacher)
        coursesections_list = []
        for coursesection in coursesections:
           coursesections_list.append((coursesection.id, coursesection.name),)
        form = self.form_class(destination_list,coursesections_list,request.POST)

        #print("obj.message")
        if form.is_valid():
            newWallMessage = WallMessages()
            #newWallMessage.title = form.cleaned_data['title']
            newWallMessage.message = form.cleaned_data['message']
            newWallMessage.sender = usuario
            destination = Destinations.objects.get(id=form.cleaned_data['destination'])
            users = None
            if destination.url_service == "sendMessageToStudentsOfACourseSection":
                selected_course_section = CourseSections.objects.get(id=form.cleaned_data['coursesections'])
                newWallMessage.title = "Todos os alunos de " + selected_course_section.course.code +" " +selected_course_section.code
                users= self.getStudentsOfACourseSection(form.cleaned_data['coursesections'])
            elif destination.url_service == "sendMessagesToStudentsOfATeacher":
                names = usuario.name.split(" ")
                newWallMessage.title = "Todos os alunos de " + names[0] + " " + names[-1]
                users= self.getStudentsOfATeacher(usuario.id)
            elif destination.url_service == "sendMessagesToTeachersOfAProgram":
                professor =Teachers.objects.get(user=usuario)
                cursos = Program.objects.filter(coordinator=professor)
                newWallMessage.title = "Todos os Professores de " + cursos[0].abbreviation
                users = self.getAllTeachersOfAProgram(cursos[0].id)
            elif destination.url_service == "sendMessagesToStudentsOfAProgram":
                professor =Teachers.objects.get(user=usuario)
                cursos = Program.objects.filter(coordinator=professor)
                newWallMessage.title = "Todos os Alunos de " + cursos[0].abbreviation
                users = self.getAllStudentsOfAProgram(cursos[0].id)
            newWallMessage.save()
            users.append(usuario)
            newWallMessage.destination = users
            serializer = WallMessagesSerializer(newWallMessage)
            send_message([user.push_notification_token for user in users],form.cleaned_data['message'],usuario,serializer.data)
            return redirect('web:wall_messages_list')
        usermobile = getUserMobile(request)
        return render(request, self.template_name, { 'form' : form, 'usermobile':usermobile, 'permission':str(usuario.permission)})

class PasswordRecover(APIView):
    def get_object(self, email):
        try:
            return Users.objects.filter(email=email)
        except Users.DoesNotExist:
            raise Http404

    def get(self, request, email, format=None):
        usuario = self.get_object(email)
        if not usuario:
            raise Http404
        else:
            self.eviar_email_senha(email, usuario[0].password)
            serializer = UsersSerializer(usuario[0])
            return Response(serializer.data, status=status.HTTP_200_OK)

    def eviar_email_senha(self, email, senha):
        msg_html = render_to_string('template_email.html', {'senha': senha})
        send_mail('EMILE - REENVIO DE SENHA', 'A sua senha no Aplicativo está descrita abaixo', settings.EMAIL_HOST, [email], html_message=msg_html)

class  GetAllUsersWithDetails(APIView):
      permission_classes = (permissions.IsAdminUser,)

      def get(self, request, format=None):
          usuarios = Users.objects.all()
          paginator = PageNumberPagination()
          result_page = paginator.paginate_queryset(usuarios, request)
          serializer = UsersSerializer(result_page, many=True)
          return paginator.get_paginated_response(serializer.data)

class  GetUserWithDetails(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, format=None):
        login = request.data['login']
        password = request.data['password']
        try:
            usuario = Teachers.objects.get(siape=login)
            if usuario:
                if usuario.user.password==password:
                    serializer = TeachersSerializer(usuario)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
        except Teachers.DoesNotExist:
            try:
                usuario = Students.objects.get(enrollment=login)
                if usuario is not None:
                    if usuario.user.password==password:
                        serializer = StudentsSerializer(usuario)
                        return Response(serializer.data, status=status.HTTP_200_OK)
            except Students.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class  GetUserCurseSections(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get_object(self, id):
        try:
            return Users.objects.get(id=id)
        except Users.DoesNotExist:
            raise Http404


    def post(self, request, format=None):
        id = request.data['id']
        usuario = self.get_object(id)
        permissions = usuario.permission
        #print(permissions)
        try:
            if(permissions.description == 'student'):
                #print('Student')
                student  = Students.objects.get(user=usuario)
                coursesections = [course_section_students.course_section for course_section_students in CourseSectionStudents.objects.filter(student=student)]
                serializer = CourseSectionsSerializer(coursesections, many=True)
            else:
                #print('teacher')
                teacher  = Teachers.objects.get(user=usuario)
                coursesections =  CourseSections.objects.filter(teacher = teacher)
                serializer = CourseSectionsSerializer(coursesections, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class  UpdateUserWithDetails(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get_object(self, id):
        try:
            return Users.objects.get(id=id)
        except Users.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        id = request.data['id']
        usuario = self.get_object(id)
        try:
            email =request.data['email']
            senha =request.data['password']
            if (email!=""):
                usuario.email = email
                usuario.save()
            if (senha!=""):
                usuario.password = senha
                usuario.save()
            if(email!="") or (senha!=""):
                serializer = UsersSerializer(usuario)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class RegistrarToken(APIView):
    #Registro de token para realização de push notification
    permission_classes = (permissions.IsAdminUser,)

    def get_object(self, usuario):
        try:
            return Users.objects.get(id=usuario)
        except Users.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        usuario = self.get_object(request.data['id'])
        token = request.data['push_notification_token']
        #print(request.data)
        try:
            usuario.push_notification_token = token
            usuario.save()
            serializer = UsersSerializer(usuario)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class  GetAllWallMessagesOfUser(APIView):
      permission_classes = (permissions.IsAdminUser,)

      def get_object(self, user_id):
          try:
              return Users.objects.get(id=user_id)
          except Users.DoesNotExist:
              raise Http404

      def get(self, request, id, format=None):
          #id = request.data['id']
          usuario = self.get_object(id)
          try:
              messages = WallMessages.objects.filter(destination=usuario).order_by('-date')
              paginator = PageNumberPagination()
              result_page = paginator.paginate_queryset(messages, request)
              serializer = WallMessagesSerializer(result_page, many=True)
              return paginator.get_paginated_response(serializer.data)
          except Exception as e:
              print(e)
              return Response(status=status.HTTP_400_BAD_REQUEST)

class  SearchWallMessagesOfUser(APIView):
      permission_classes = (permissions.IsAdminUser,)

      def get_object(self, user_id):
          try:
              return Users.objects.get(id=user_id)
          except Users.DoesNotExist:
              raise Http404

      def get(self, request, id, seachstring, format=None):
          #id = request.data['id']
          usuario = self.get_object(id)
          try:
              messages = WallMessages.objects.filter(destination=usuario, message__contains=seachstring)
              paginator = PageNumberPagination()
              result_page = paginator.paginate_queryset(messages, request)
              serializer = WallMessagesSerializer(result_page, many=True)
              return paginator.get_paginated_response(serializer.data)
          except Exception as e:
              print(e)
              return Response(status=status.HTTP_400_BAD_REQUEST)

def send_message(users_tokens, body, sender, data_message=None):
    push_service = FCMNotification(api_key=settings.PUSH_NOTIFICATIONS_SETTINGS['GCM_API_KEY'])
    try:
        registration_ids = users_tokens
        #message_title = 'Nova mensagem de {0}'.format(sender.name)
        message_body = body
        icon="icon_transparent"
        serialized_data = data_message
        #serialized_data['title']= message_title
        serialized_data['body'] = message_body
        #print(serialized_data)
        #result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title,message_icon=icon,message_body=message_body, data_message=serialized_data)
        result = push_service.notify_multiple_devices(registration_ids=registration_ids, data_message=serialized_data)
        #print("PushMessage %s" % result)
        return True
    except Exception as e:
        print(e)
        return False

class  SendWallMessagesToStudentsOfATeacher(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get_object(self, id):
        try:
            return Users.objects.get(id=id)
        except Users.DoesNotExist:
            print("Erro aqui no Users")
            raise Http404

    def getStudentsOfATeacher(self, id): # Todos os meus alunos
        usuario = self.get_object(id)
        try:
            teacher  = Teachers.objects.get(user=usuario)
            coursesections =  CourseSections.objects.filter(teacher = teacher)
            users = [course_section_students.student.user for course_section_students in CourseSectionStudents.objects.filter(course_section=coursesections).annotate(Count('student'))]
            return users
        except Exception as e:
            print("Erro aqui no Teachers")
            print(e)
            #return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        try:
            users = self.getStudentsOfATeacher(request.data['sender'])
            sender = self.get_object(request.data['sender'])
            #return Response(status=status.HTTP_200_OK)
            message = request.data['message']
            device = request.data['device']
            title = request.data['title']
            wallmessage = WallMessages()
            wallmessage.sender = sender
            wallmessage.message = message
            wallmessage.title = title
            wallmessage.save()
            users.append(sender)
            wallmessage.destination = users
            serializer = WallMessagesSerializer(wallmessage)
            send_message([user.push_notification_token for user in users],message,sender,serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class  SendWallMessagesToStudentsOfACourseSection(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get_object(self, id):
        try:
            return Users.objects.get(id=id)
        except Users.DoesNotExist:
            raise Http404

    def getStudentsOfACourseSection(self, course_section_id): # Alunos de uma Turma
        try:
            selected_course_section = CourseSections.objects.get(id=course_section_id)
            coursesectionstudents = CourseSectionStudents.objects.filter(course_section=selected_course_section)
            users = [course_section_students.student.user for course_section_students in coursesectionstudents]
            return users
        except Exception as e:
            print(e)

    def post(self, request, format=None):
        try:
            users = self.getStudentsOfACourseSection(request.data['course_section_id'])
            sender = self.get_object(request.data['sender'])
            message = request.data['message']
            device = request.data['device']
            title = request.data['title']
            wallmessage = WallMessages()
            wallmessage.sender = sender
            wallmessage.message = message
            wallmessage.title = title
            wallmessage.save()
            users.append(sender)
            wallmessage.destination = users
            serializer = WallMessagesSerializer(wallmessage)
            send_message([user.push_notification_token for user in users],
                          message,
                          sender,
                          serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class  SendWallMessagesToTeachersOfAProgram(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get_object(self, id):
        try:
            return Users.objects.get(id=id)
        except Users.DoesNotExist:
            raise Http404

    def getAllTeachersOfAProgram(self, id): # Todos os Professores de um Curso
        try:
            programa=Program.objects.get(id=id)
            courses = Courses.objects.filter(program=programa)
            #students = [course_section_students.student for course_section_students in CourseSectionStudents.objects.filter(course_section=coursesections).annotate(Count('student'))]
            users = [coursesections.teacher.user for coursesections in CourseSections.objects.filter(course__in=courses)]
            my_list = list(set(users))
            #print(my_list)
            return my_list
        except Exception as e:
            print(e)

    def post(self, request, format=None):
        try:
            program_id = request.data['program_id']
            users = self.getAllTeachersOfAProgram(program_id)
            sender = self.get_object(request.data['sender'])
            message = request.data['message']
            device = request.data['device']
            title = request.data['title']
            wallmessage = WallMessages()
            wallmessage.sender = sender
            wallmessage.message = message
            wallmessage.title = title
            wallmessage.save()
            users.append(sender)
            wallmessage.destination = users
            serializer = WallMessagesSerializer(wallmessage)
            send_message([user.push_notification_token for user in users],
                          message,
                          sender,
                          serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class  SendWallMessagesToStudentsOfAProgram(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get_object(self, id):
        try:
            return Users.objects.get(id=id)
        except Users.DoesNotExist:
            raise Http404

    def getAllStudentsOfAProgram(self, id): # Todos os Alunos de um Curso
        try:
            studends = Students.objects.filter(program=Program.objects.get(id=id))
            users = [student.user for student in studends]
            return users
        except Exception as e:
            print(e)

    def post(self, request, format=None):
        try:
            program_id = request.data['program_id']
            users = self.getAllStudentsOfAProgram(program_id)
            sender = self.get_object(request.data['sender'])
            message = request.data['message']
            device = request.data['device']
            title = request.data['title']
            wallmessage = WallMessages()
            wallmessage.sender = sender
            wallmessage.message = message
            wallmessage.title = title
            wallmessage.save()
            users.append(sender)
            wallmessage.destination = users
            serializer = WallMessagesSerializer(wallmessage)
            send_message([user.push_notification_token for user in users],
                          message,
                          sender,
                          serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class AtualizarImagemPerfil(APIView):
    permission_classes = (permissions.IsAdminUser,)
    parser_classes = (MultiPartParser, FormParser,FileUploadParser)

    def get_object(self, id):
        try:
            return Users.objects.get(pk=id)
        except Users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, id, format=None):
        usuario = self.get_object(id)
        #print("Id do usuario: %s" % id)
        #print(usuario.image_path)
        up_file = request.FILES.get('file', False)
        #print(up_file)
        if up_file and usuario:
            self.save_image_perfil(usuario, up_file)
            serializer = UsersSerializer(usuario)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


    def save_image_perfil(self, usuario, up_file):
        try:
            caminho_relativo = "imagens/imagem_perfil_usuario_movel/"
            url_arquivo = settings.MEDIA_ROOT + '/' + caminho_relativo
            #print(url_arquivo)
            if usuario.image_path:
                self.deletar_arquivo_anterior(str(settings.MEDIA_ROOT) + '/' + str(usuario.image_path))

            nome_arquivo = (str(usuario.name).replace(" ", "") + str(random.randint(0, 5000)) + str(usuario.id) + '.jpg')
            if not os.path.exists(url_arquivo):
                os.makedirs(url_arquivo, exist_ok=True)

            im = open(url_arquivo + nome_arquivo, 'wb+')
            for chunk in up_file.chunks():
                im.write(chunk)
            im.close()
            #im.save(url_arquivo + nome_arquivo, quality=75, optimize=True)
            try:
                size = 256, 256
                im = Image.open(url_arquivo + nome_arquivo)
                im.thumbnail(size)
                im.save(url_arquivo + nome_arquivo, "JPEG")
            except Exception as e:
                print("cannot create thumbnail for", caminho_relativo+nome_arquivo)
                print(e)
            usuario.image_path = (caminho_relativo+nome_arquivo)
            usuario.save()
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)

    def deletar_arquivo_anterior(self, arquivo):
        os.remove(arquivo)

class  GetProgramOfACoordinator(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, id, format=None):
        try:
            usuario = Users.objects.get(id=id)
            professor =Teachers.objects.get(user=usuario)
            cursos = Program.objects.filter(coordinator=professor)
            serializer = ProgramSerializer(cursos[0])
            return Response(serializer.data)
        except Program.DoesNotExist:
            raise Http404

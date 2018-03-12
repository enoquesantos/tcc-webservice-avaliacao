from django.contrib.auth.models import User
from .models import Users, Teachers, Students
class UserMobileBackend(object):

    def authenticate(self, request, username=None, password=None):
        try:
            usuario = Teachers.objects.get(siape=username)
        except Teachers.DoesNotExist:
            try:
                usuario = Students.objects.get(enrollment=username)
            except Students.DoesNotExist:
                #print("Não achou nada")
                return None
        if usuario:
            if usuario.user.password==password:
                try:
                    user = User.objects.get(username=username)
                    user.password = password
                    user.save()
                    #print("Logou com Sucesso")
                except User.DoesNotExist:
                    #print("Criando Usuario")
                    user = User(username=username)
                    user.password = password
                    user.is_staff = False
                    user.is_superuser = False
                    user.save()
                return user
            else:
                #print("Senha nao confere")
                return None
        else:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

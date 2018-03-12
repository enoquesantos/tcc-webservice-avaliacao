from django.db import models
from .choices import GENDER_CHOICES
from datetime import datetime
from django.utils import timezone

class Institution(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    name = models.CharField(max_length=50, blank=True, null=True)
    abbreviation = models.CharField(max_length=10, blank=True, null=True)
    cnpj = models.CharField(max_length=18, unique=True)
    address =  models.CharField(max_length=250, blank=True, null=True)
    current_program_section = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Instituição'
        verbose_name_plural = 'Instituições'

class Destinations(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    name = models.CharField(max_length=50, blank=False, null=False)
    url_service = models.CharField(max_length=250, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo de Envio'
        verbose_name_plural = 'Tipos de Envio'

class Permissions(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    description = models.CharField(max_length=20, blank=False, null=False)
    messagedestinations = models.ManyToManyField(Destinations, blank=True)
    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Permissão'
        verbose_name_plural = 'Permissões'

class Users(models.Model):
    id= models.AutoField(primary_key=True, blank=False, null=False)
    #username = models.CharField(max_length=20, blank=False, null=False)
    email = models.CharField(max_length=50, unique=True, blank=False,)
    password = models.TextField(blank=False, null=False)
    name = models.CharField(max_length=250, blank=True, null=True)
    birth_date = models.DateField(
            blank=True, null=True)
    gender=models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    address =  models.CharField(max_length=250, blank=True, null=True)
    push_notification_token = models.TextField(blank=True, null=True)
    image_path = models.ImageField(upload_to='imagem/usuario',blank=True, null=True, help_text="Profile Picture", verbose_name="Profile Picture")
    #thumbNail = models.ImageField(upload_to='imagem/usuario/thumbNail')
    permission = models.ForeignKey(Permissions)
    #course_sections =
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Usuário do App'
        verbose_name_plural = 'Usuários do App'
        ordering = ('name',)

class Teachers(models.Model):
     siape = models.CharField(max_length=20, blank=False, null=False)
     user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='dados_professor')

     def __str__(self):
         return self.user.name

     class Meta:
         verbose_name = 'Professor'
         verbose_name_plural = 'Professores'
         ordering = ('user__name',)

class Program(models.Model):
     id = models.CharField(max_length=6, primary_key=True)
     name = models.CharField(max_length=50, blank=True, null=True)
     abbreviation = models.CharField(max_length=10, blank=True, null=True)
     total_hours = models.IntegerField(blank=True, null=True)
     total_credits = models.IntegerField(blank=True, null=True)
     institution = models.ForeignKey(Institution, related_name='programs')
     coordinator =  models.ForeignKey(Teachers, blank=False, related_name='is_coordinator')

     def __str__(self):
         return self.name

     class Meta:
         verbose_name = 'Curso'
         verbose_name_plural = 'Cursos'
         ordering = ('name',)

class Students(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE,primary_key=True, related_name='dados_estudante')
    enrollment = models.CharField(max_length=20, blank=False, null=False)
    program = models.ForeignKey(Program, related_name='students')

    def __str__(self):
        return self.user.name
    class Meta:
        verbose_name = 'Estudante'
        verbose_name_plural = 'Estudantes'
        ordering = ('user__name',)

class CourseType(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    description = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Tipo de Disciplina'
        verbose_name_plural = 'Tipos de Disciplina'
        ordering = ('description',)

class Courses(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    code = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    credits = models.IntegerField(blank=True, null=True)
    hours = models.IntegerField(blank=True, null=True)
    program_section = models.IntegerField(blank=True, null=True)
    course_type = models.ForeignKey(CourseType)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='courses')
    #course_sections =

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'
        ordering = ('name',)


class CourseSectionStudentsStatus(models.Model):

    id = models.AutoField(primary_key=True, blank=False, null=False)
    description = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Course Section Student Status'
        verbose_name_plural = 'Courses Sections Students Status'
        ordering = ('description',)

class CourseSections(models.Model):

    id = models.AutoField(primary_key=True, blank=False, null=False)
    code = models.CharField(max_length=20, blank=False, null=False)
    name = models.CharField(max_length=80, blank=False, null=False)
    course = models.ForeignKey(Courses, blank=False, null=False, related_name='data_couses')
    teacher = models.ForeignKey(Teachers, blank=True, null=False, related_name='data_teachers')
    course_section_period = models.CharField(max_length=6, blank=False, null=False)
    #section_times = db.relationship("SectionTimes", backref='course_section', lazy='dynamic')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
        ordering = ('course__program__name','name',)

class CourseSectionStudents(models.Model):
    id =  models.AutoField(primary_key=True, blank=False, null=False)
    student = models.ForeignKey(Students, blank=False, null=False, related_name='data_students')
    course_section = models.ForeignKey(CourseSections, null=False)
    status = models.ForeignKey(CourseSectionStudentsStatus, null=False)
    #grade = models.IntegerField(null=True)
    #__table_args__ = (db.UniqueConstraint('course_section_id','user_id', name='course_section_user_uc'),)

    def __str__(self):
        return self.student.user.name

    class Meta:
        verbose_name = 'Aluno x Turma'
        verbose_name_plural = 'Alunos x Turmas'
        unique_together = ('student','course_section')
        ordering = ('student__user__name',)

class WallMessages(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    date = models.DateTimeField(null=True, default=timezone.now)
    sender = models.ForeignKey(Users, blank=False, null=False, related_name='data_sender_who')
    destination = models.ManyToManyField(Users,blank=False, related_name='message_destinations')
    title = models.CharField(max_length=50, blank=False, null=False)
    message = models.TextField()

    class Meta:
        verbose_name = 'Mensagen'
        verbose_name_plural = 'Mensagens'

    def __str__(self):
        return self.message

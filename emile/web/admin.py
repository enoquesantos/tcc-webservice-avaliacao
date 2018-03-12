# Register your models here.
from django.contrib import admin
from .models import WallMessages, CourseSections, CourseSectionStudents, Destinations, Permissions, Users, Program, Institution, Courses, CourseType, Students, Teachers, CourseSectionStudentsStatus
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(u' <a href="%s" target="_blank"><img src="%s" alt="%s" /></a> %s ' % \
                          (image_url, image_url, file_name, _('Change:')))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))

class ImageWidgetAdmin(admin.ModelAdmin):
    image_fields = []

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in self.image_fields:
            request = kwargs.pop("request", None)
            kwargs['widget'] = AdminImageWidget
            return db_field.formfield(**kwargs)
        return super(ImageWidgetAdmin, self).formfield_for_dbfield(db_field, **kwargs)

class ProgramAdminline(admin.TabularInline):
    model= Program
    extra=0

class InstitutionAdmin(admin.ModelAdmin):
    inlines = [ProgramAdminline]

class CourseAdminline(admin.TabularInline):
    model = Courses
    #search_fields = ('name','code','course_type__description','program__name')
    list_display = ('name','code','course_type','program',)
    extra = 0

class StudentAdminline(admin.TabularInline):
    model = Students
    extra = 0

class TeacherAdminline(admin.TabularInline):
    model = Teachers
    extra = 0

class ProgramAdmin(admin.ModelAdmin):
    #inlines = [CourseAdminline, StudentAdminline]
    inlines = [CourseAdminline]
    search_fields = ('name','abbreviation','coordinator__name',)
    list_display = ('name', 'abbreviation','coordinator',)

class UserAdmin(ImageWidgetAdmin):
    inlines =[TeacherAdminline, StudentAdminline]
    image_fields = ['image_path', 'detailImage']
    search_fields = ('name','permission__description')
    list_display = ('name', 'permission',)

class CourseSectionStudentsAdmin(admin.ModelAdmin):
    search_fields = ('student__user__name','course_section__name',)
    list_display = ('student', 'course_section',)

class CourseSectionsAdmin(admin.ModelAdmin):
    search_fields = ('code','name','course__name','course__program__name','teacher__user__name','course_section_period',)
    list_display = ('code','name','course','teacher','course_section_period',)

class CourseAdmin(admin.ModelAdmin):
    search_fields = ('code','name','credits','hours','course_type__description','program__name',)
    list_display = ('code','name','credits','hours','course_type','program',)


class WallMessagesAdmin(admin.ModelAdmin):
    search_fields = ('date','sender__name','title','message',)
    list_display = ('date','sender','title','message',)


admin.site.register(Destinations)
admin.site.register(Users,UserAdmin)
admin.site.register(CourseSectionStudentsStatus)
admin.site.register(Permissions)
admin.site.register(Courses,CourseAdmin)
admin.site.register(CourseType)
admin.site.register(CourseSections, CourseSectionsAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(CourseSectionStudents,CourseSectionStudentsAdmin)
admin.site.register(WallMessages,WallMessagesAdmin)

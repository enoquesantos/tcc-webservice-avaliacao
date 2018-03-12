from openpyxl import load_workbook
import sys
import os
import django

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
print(SITE_ROOT)

sys.path.append(SITE_ROOT)
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'emile.settings'
django.setup()

from web.models import WallMessages, CourseSectionStudents, CourseSections, CourseSectionStudentsStatus, Courses, Institution, Destinations, Permissions, Users, Teachers,Program, Students, CourseType
from django.db.models import Q

print("Incluindo CourseSectionsStudends ....")
wb = load_workbook('web/planilhas/CourseSectionsStudendsIntegrado.xlsx', data_only = True)
ws = wb.get_sheet_by_name('Sheet1')
mylist = []
for row in ws.get_squared_range(min_col=1, min_row=2, max_col=5, max_row=165):
    coursesectionstudent = CourseSectionStudents()
    for cell in row:
        mylist.append(cell.value)
    selectedstudent = Students.objects.get(enrollment=mylist[3])
    coursesectionstudent.student = selectedstudent
    names = '{}-{}-{}'.format(mylist[1].strip(),mylist[2],mylist[0].strip())
    print(names)
    selectedcoursesection = CourseSections.objects.get(name=names)
    coursesectionstudent.course_section = selectedcoursesection
    coursesectionstudent.status = CourseSectionStudentsStatus.objects.get(description="Cursando")
    coursesectionstudent.save()
    mylist.clear()

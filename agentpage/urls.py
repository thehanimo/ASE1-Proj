from django.urls import path,include
from . import views
from django.conf.urls import url

app_name='agentpage'

urlpatterns = [
    path('home/',views.agentpage,name="agentpage"),
    path('addemployee/',views.addemployee,name="addemployee"),
    path('employee/',views.employee,name="employee"),
    path('employee/logined/',views.employeework,name="employeework"),
    path('todo/',views.todo,name="todo"),
    path('delivering/',views.delivering,name="delivering"),
    path('delivered/',views.delivered,name="delivered"),
]

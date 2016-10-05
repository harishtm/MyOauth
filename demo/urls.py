from django.conf.urls import patterns, include, url
from demo.views import *

urlpatterns = patterns('',

    url(r'^register/$', RegistrationView.as_view()),
    # Todos endpoint 
    url(r'^todos/$', TodosView.as_view()),
    url(r'^todos/(?P<todo_id>[0-9]*)$', TodosView.as_view()),
    url(r'^sign-up/$', SignUp.as_view(), name="sign_up"),

)

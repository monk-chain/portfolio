from django.urls import path
from . import views 
from . import line_api

urlpatterns = [
    path("webhook/",line_api.webhook,name="webhook"),
    path("orgdebug/",line_api.orgdebug,name="orgdebug"),
]
"""srs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from app.utils import captcha
from srs import settings
from srs.controllers import home
from srs.controllers import login
from srs.controllers.activate_account import activate_account_cont
from srs.controllers.forgotten_password import forgotten_password_cont
from srs.controllers.login import sign_in_cont
from srs.controllers.reset_password import reset_password_cont
from srs.controllers.sign_up import sign_up_cont

urlpatterns = [
    url(r'^$', home.index, name='home'),
    url(r'^captcha/(?P<name>[a-zA-Z0-9_-]+)$', captcha.show_image, name='captcha'),
    url(r'^sign_up', sign_up_cont, name='sign_up'),
    url(r'^activate_account/(?P<hash>[a-zA-Z0-9]+)$', activate_account_cont, name='activate_account'),
    url(r'^forgotten_password', forgotten_password_cont, name='forgotten_password'),
    url(r'^reset_password/(?P<hash>[a-zA-Z0-9]+)$', reset_password_cont, name='reset_password'),
    url(r'^sign_in', sign_in_cont, name='sign_in'),
    url(r'^dashboard/', include('dashboard.urls')),
    # url(r'^admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

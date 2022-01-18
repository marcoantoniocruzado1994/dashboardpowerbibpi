from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, logout_then_login
from .views import home,upload,sesiones,sesiones_random,loginPage

urlpatterns = [
    #LOGIN
    path('', LoginView.as_view( template_name='upload/index.html'), name='login'),
    path('accounts/login/', LoginView.as_view( template_name='upload/index.html')),
    path('logout/', logout_then_login, name='logout'),
    path('login/', loginPage, name='login_page'),
    path('home/', login_required(home), name='home'),

    #CARGAR ARCHIVO SLA
    path('upload/',login_required(upload), name='upload'),

    #SESIONES RANDON
    path('sessiones/', login_required(sesiones), name='sessiones'),
    path('sessiones/random/', login_required(sesiones_random), name='sesiones_random'),   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

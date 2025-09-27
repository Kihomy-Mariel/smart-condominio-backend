# backend_condominio/urls.py
from django.contrib import admin
from django.urls import path, include
from administradores.auth_views import LoginView, RefreshView, LogoutView, MeView
from administradores.urls import urlpatterns as admin_urls
from copropietarios.urls import urlpatterns as cop_urls
from copropietarios.mobile_auth import LoginCopropietarioView, LogoutCopropietarioView
from visitantes.urls_mobile import urlpatterns as visit_mob_urls
from guardias.urls import urlpatterns as guardias_urls
from guardias.mobile_auth import LoginGuardiaView, LogoutGuardiaView

from casas.urls import urlpatterns as casas_urls         # <-- NUEVO
from casas.urls_mobile import urlpatterns as casas_mob_urls  # <-- NUEVO
from vehiculos.urls import urlpatterns as vehiculos_urls
from vehiculos.urls_mobile import urlpatterns as vehiculos_mob_urls
from mascotas.urls import urlpatterns as mascotas_urls
from mascotas.urls_mobile import urlpatterns as mascotas_mob_urls


urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/auth/login/",   LoginView.as_view(),   name="jwt_login"),
    path("api/auth/refresh/", RefreshView.as_view(), name="jwt_refresh"),
    path("api/auth/logout/",  LogoutView.as_view(),  name="jwt_logout"),
    path("api/auth/me/",      MeView.as_view(),      name="jwt_me"),

    # CRUDs protegidos por admin
    path("api/", include(admin_urls)),
    path("api/", include(cop_urls)),        # /api/copropietarios/ (solo admin)
    path("api/", include(guardias_urls)), 
    path("api/", include(casas_urls)), 
    path("api/", include(vehiculos_urls)),      # Admin protegido
     path("api/", include(mascotas_urls)),      # Admin protegido
    path("api/mobile/auth/logincopropietario/",  LoginCopropietarioView.as_view()),
    path("api/mobile/auth/logoutcopropietario/", LogoutCopropietarioView.as_view()),
    path("api/mobile/auth/loginguardia/",  LoginGuardiaView.as_view()),
    path("api/mobile/auth/logoutguardia/", LogoutGuardiaView.as_view()),

     # Móvil (público)
    path("api/", include(visit_mob_urls)), # /api/mobile/visitantes/...
    path("api/", include(casas_mob_urls)),
    path("api/", include(vehiculos_mob_urls)),  # Móvil público
    path("api/", include(mascotas_mob_urls)),  # Móvil público

]

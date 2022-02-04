import notifications.urls
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path
from src.accounts.views import GoogleLoginView, CustomRegisterAccountView
from .settings import DEBUG, MEDIA_ROOT, MEDIA_URL

urlpatterns = [

    # WEBSITE APPLICATION --------------------------------------------------------------------------------
    path('', include('src.website.urls', namespace='website')),

    # ADMIN/ROOT APPLICATION
    path('admin/', admin.site.urls),
    path('accounts/', include('src.accounts.urls', namespace='accounts')),
    path('accounts/', include('allauth.urls')),

    # PORTALS ---------------------------------------------------------- #
    path('a/', include('src.portals.admins.urls', namespace='admins')),
    path('c/', include('src.portals.customer.urls', namespace='customer')),

    # REST API -------------------------------------------------------------------------------------------
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', CustomRegisterAccountView.as_view(), name='account_create_new_user'),
    path('auth/google/', GoogleLoginView.as_view(), name='google-login-view'),

    path('api/', include('src.api.urls', namespace='api')),

    # NOTIFICATIONS APPLICATION ---------------------------------------------------------------------------------
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),

]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

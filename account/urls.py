"""""   2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views
from .views import CreateAccount

urlpatterns = [
    path('signin/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("register/", CreateAccount.as_view()),
    path("recover-account/", CreateAccount.as_view()),

]
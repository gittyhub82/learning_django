from django.urls import path, include

app_name = "authentication_app"

urlpatterns = [
    path('', include('django.contrib.auth.urls'))
]
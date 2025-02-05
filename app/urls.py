from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.http import JsonResponse

# def handle_404(request, exception):
#     return JsonResponse({"status": "page not found."})

# def handle_403(request, exception):
#     return JsonResponse({"status": "forbidden."})

# def handle_500(request):
#     return JsonResponse({"status": "server error."})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("user.urls")),     #ユーザーURL
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
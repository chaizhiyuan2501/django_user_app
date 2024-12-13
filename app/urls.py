from django.contrib import admin
from django.urls import path,include
from django.http import JsonResponse

# def handle_404(request, exception):
#     return JsonResponse({"status": "page not found."})

# def handle_403(request, exception):
#     return JsonResponse({"status": "forbidden."})

# def handle_500(request):
#     return JsonResponse({"status": "server error."})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("",include("user.urls")),
    # path("todo/",include("todo.urls")),
]

# handler403 = 'project.urls.handle_403'
# handler404 = 'project.urls.handle_404'
# handler500 = 'project.urls.handle_500'
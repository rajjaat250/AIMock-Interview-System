from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔥 All API routes
    path('api/', include('interview.urls')),
]
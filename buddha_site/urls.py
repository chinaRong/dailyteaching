from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def default_image_view(request):
    # 没有 id 的访问者返回一张默认图片
    html = """
    <html><body style="text-align:center;">
        <h2>🙏 欢迎访问每日教言 🙏</h2>
        <p>请使用绑定了ID的手环访问本页面。</p>
        <img src="/static/default.jpg" width="300">
    </body></html>
    """
    return HttpResponse(html)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', default_image_view),
]

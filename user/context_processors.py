from django.conf import settings

# 全体のテンプレートが使える変数
def constant_data(request):
    return {
        "APP_TITLE": settings.APP_TITLE,
    }
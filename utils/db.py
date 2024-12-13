from user.models import User

def get_user_model_data(request):
    if request.user.is_authenticated:
        # 用户已登录，获取模型数据
        data = User.objects.all().values()  # 根据需求修改查询逻辑
        return data
    else:
        # 用户未登录，返回空数据
        return "ゲスト"

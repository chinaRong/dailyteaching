from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserData
from datetime import date, datetime
import json
import os


def date_to_day_number(date_str):
    """将日期字符串转换为该年的第几天（1-365）"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.timetuple().tm_yday


@csrf_exempt
def visitor_view(request):
    user_id = request.GET.get("id")

    if not user_id:
        return JsonResponse({
            "status": "guest",
            "message": "游客访问，无ID。请使用带手环的链接访问。"
        })

    user_obj, created = UserData.objects.get_or_create(
        user_id=user_id,
        defaults={"data_map": {"visits": [], "last_visit": None}}
    )

    data_map = user_obj.data_map or {}
    visits = data_map.get("visits", [])
    today_str = date.today().isoformat()
    today_num = date_to_day_number(today_str)

    # ✅ 防止重复添加
    if today_num not in visits:
        visits.append(today_num)

    data_map["visits"] = visits
    data_map["last_visit"] = today_str
    user_obj.data_map = data_map
    user_obj.save()

    return JsonResponse({
        "status": "success",
        "new_user": created,
        "user_id": user_id,
        "data_map": data_map,
    })


'''
{
    "active": 1,
    "content": "每周一~周六 Zoom房间 2025茶话会 进行《入菩萨行论》共修，欢迎各位同学参加。点击此公告即能复制获得房间号及密码~",
    "extend": "房间号2026202601 密码123456",
    "dead time": "2025-12-31"
}
'''


def announcement():
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "announcement.json")

    if not os.path.exists(file_path):
        return JsonResponse({"active": 0})

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return JsonResponse(data)
    except Exception:
        return JsonResponse({"active": 0})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserData
from datetime import date, datetime


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


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Member
import json

# 原有视图：显示表格页面
def index(request):
    members = Member.objects.all()  # 获取全部，建议加上排序，例如 order_by('gaijin_id')
    return render(request, 'members_app/index.html', {'members': members})

# -------- API 接口（用于前端AJAX）--------

@require_http_methods(["GET"])
def api_members(request):
    """返回所有成员信息（JSON）"""
    members = list(Member.objects.values())
    return JsonResponse(members, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def api_add_member(request):
    """新增成员"""
    try:
        data = json.loads(request.body)
        gaijin_id = data.get('gaijin_id')
        if not gaijin_id:
            return JsonResponse({'error': 'gaijin_id 不能为空'}, status=400)
        if Member.objects.filter(gaijin_id=gaijin_id).exists():
            return JsonResponse({'error': '该 gaijin_id 已存在'}, status=400)

        Member.objects.create(
            gaijin_id=gaijin_id,
            name=data['name'],
            state=data['state'],
            join_date=data['join_date'],
            landforce=data['landforce'],
            airforce=data['airforce'],
            navy=data['navy'],
        )
        return JsonResponse({'status': 'ok', 'gaijin_id': gaijin_id})
    except KeyError as e:
        return JsonResponse({'error': f'缺少字段: {e}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def api_update_member(request, gaijin_id):
    """更新成员信息（gaijin_id 不可修改）"""
    try:
        member = get_object_or_404(Member, gaijin_id=gaijin_id)
        data = json.loads(request.body)
        # 更新允许的字段
        member.name = data.get('name', member.name)
        member.state = data.get('state', member.state)
        member.join_date = data.get('join_date', member.join_date)
        member.landforce = data.get('landforce', member.landforce)
        member.airforce = data.get('airforce', member.airforce)
        member.navy = data.get('navy', member.navy)
        member.save()
        return JsonResponse({'status': 'ok'})
    except Member.DoesNotExist:
        return JsonResponse({'error': '成员不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def api_delete_member(request, gaijin_id):
    """删除成员"""
    try:
        member = get_object_or_404(Member, gaijin_id=gaijin_id)
        member.delete()
        return JsonResponse({'status': 'ok'})
    except Member.DoesNotExist:
        return JsonResponse({'error': '成员不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
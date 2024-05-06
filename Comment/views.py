from django.http import JsonResponse,HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Comment
import json

@csrf_exempt  # CSRF 보안 예외
def comment_list(request):
    if request.method == "GET":  # 댓글 목록 조회
        comments = Comment.objects.all().order_by("-created_at")  # 최신순 정렬
        comment_list = [{"name": c.name, "content": c.content, "created_at": c.created_at} for c in comments]
        htmlfile = render(request,"comment_form.html" ,{"comments":comments})
      #  if len(comment_list) > 0: 
       #     return JsonResponse( comment_list, safe=False)  # 목록 반환
        return htmlfile
       # return render(request,"comment_form.html" ,{"댓글":comment_list})


    elif request.method == "POST":  # 새로운 댓글 작성
        try:
            data = json.loads(request.body)  # 요청 데이터 추출
            name = data.get("name")
            password = data.get("password")
            content = data.get("content")

            if not (name and password and content):
                return JsonResponse({"error": "필수 입력 사항을 모두 작성해주세요."}, status=400)
            
            Comment.objects.create(name=name, password=password, content=content)  # 댓글 저장
            return JsonResponse({"message": "댓글이 성공적으로 작성되었습니다."})
        except json.JSONDecodeError:
            name = request.POST.get("name")
            password = request.POST.get("password")
            content = request.POST.get("content")    
            Comment.objects.create(name=name, password=password, content=content)  # 댓글 저장


            return HttpResponseRedirect("/comments/")
           # return JsonResponse({"error": "유효하지 않은 JSON 데이터입니다."}, status=400)
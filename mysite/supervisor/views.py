from django.shortcuts import render, get_object_or_404
from django.utils import timezone  # 시간대가 적용된 현재 시각 획득

# Create your views here.
def testpage(request):
    # print(timezone.now()) # 터미널에 출력되는 시간은 정상인데
    return render(request, 
                  'supervisor/testpage.html', 
                  {'now': timezone.now().strftime('%Y-%m-%d %H:%M:%S')}  # 웹페이지 출력되는 시간이 35분 느린 오류는 뭐지???
                  )


from django.shortcuts import render, get_object_or_404
from django.utils import timezone  # 시간대가 적용된 현재 시각 획득

# Create your views here.

def testpage(request):
    return render(request, 
                  'subject/testpage.html', 
                  {'now': timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
                  )
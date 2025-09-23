from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from ..models import Question

def index(request):
    """
    pybo목록출력
    """
    # 1. 입력 파라미터
    page = request.GET.get('page', '1') # 페이지 번호
    kw = request.GET.get('kw','') #검색어
    so = request.GET.get('so', 'recnet')

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter','-create_date')
    elif so == 'populer':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer','-create_date')
    else: # recent
        question_list = Question.objects.order_by('-create_date')

    # 2. 데이터 조회
    # question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()

    # 3. 페이지네이션
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 표시
    page_obj = paginator.get_page(page) # 페이지네이터 객체에서 해당 페이지의 데이터만 가져옴

    # 4. 결과 출력 (템플릿에 전달)
    context = {'question_list': page_obj} # 템플릿에 page_obj를 전달
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
from django.shortcuts import render, get_object_or_404, redirect 
from django.http import HttpResponse # 2014.03.14 추가
from .models import Question # 2014.03.14 추가
from .forms import QuestionForm, AnswerForm # 2014.03.15 추가
from django.utils import timezone # 2014.03.14 현재시간 timezone.now() 사용하기 위해
from django.core.paginator import Paginator # 2024.03.18 페이징 기능 추가하기

# Create your views here.

# 2014.03.14 추가
def index(request) :
    """
    pybo 목록 출력
    """
    
    # 입력 인자
    page = request.GET.get('page', '1') # 2024.03.18 페이지
    
    # 조회
    question_list = Question.objects.order_by('-create_date')
    
    # 페이징 처리
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    
    # context = {'question_list': question_list}
    context = {'question_list': page_obj} # 2024.03.18 page_obj로 변경
    
    return render(request, 'pybo/question_list.html', context) # render 함수 적용
  # return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다. <br/> 오늘도 행복하세요~!")
  
  
# 2014.03.14 질문상세함수 detail() 추가 
def detail(request, question_id) :
    """
    pybo 내용 출력
    """
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id) # 404 에러 처리 추가
    context = {'question' : question}
    return render(request, 'pybo/question_detail.html', context) 

# 2014.03.14 답변등록 answer_create() 함수 추가
# 2014.03.15 답변등록 answer_create() 함수 수정 : POST, GET으로 분리
def answer_create(request, question_id):
    """
    pybo 답변 등록
    """

    question = get_object_or_404(Question, pk=question_id)

    # 2024.03.15 POST, GET으로 분리해서 추가
    if request.method == "POST" :
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else :
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

# 2014.03.15 질문등록 question_create() 함수 추가
def question_create(request):
    """
    pybo 질문 등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False) # create_date가 지정될 때까지 임시저장
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else :
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)
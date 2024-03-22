from django.contrib import messages # '수정권한이 없습니다' 오류 메세지 발생시키기 위해
from django.contrib.auth.decorators import login_required # @login_required 애더네이션 적용하기
from django.shortcuts import render, get_object_or_404, redirect 
from django.utils import timezone # 현재시간 timezone.now() 사용하기 위해

from ..forms import QuestionForm
from ..models import Question

# 2024.03.15 질문등록 question_create() 함수 추가
@login_required(login_url='common:login') # 2024.03.19 질문등록하려면 login 먼저하라고!
def question_create(request):
    """
    pybo 질문 등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False) # create_date가 지정될 때까지 임시저장
            question.author = request.user # 추가한 속성 author 적용. 2024.03.19 
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else :
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

# 2024.03.19 질문수정함수 추가
@login_required(login_url='common:login') 
def question_modify(request, question_id):
    """
    pybo 질문 수정
    """
    question = get_object_or_404(Question, pk=question_id)
    # 로그인한 사용자(request.user)와 글쓴이(question.author)가 다르면 수정권한없음
    if request.user != question.author: 
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False) # create_date가 지정될 때까지 임시저장
            question.author = request.user 
            question.modify_date = timezone.now() # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else :
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

# 2024.03.19 질문삭제함수 추가
@login_required(login_url='common:login') 
def question_delete(request, question_id):
    """
    pybo 질문 삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    # 로그인한 사용자(request.user)와 글쓴이(question.author)가 다르면 삭제권한없음
    if request.user != question.author: 
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    
    question.delete()
    return redirect('pybo:index')
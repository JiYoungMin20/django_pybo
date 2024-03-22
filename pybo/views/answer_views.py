from django.contrib import messages # '수정권한이 없습니다' 오류 메세지 발생시키기 위해
from django.contrib.auth.decorators import login_required # @login_required 애더네이션 적용하기
from django.shortcuts import render, get_object_or_404, redirect, resolve_url 
from django.utils import timezone # 현재시간 timezone.now() 사용하기 위해

from ..forms import AnswerForm
from ..models import Question, Answer


# 2014.03.14 답변등록 answer_create() 함수 추가
# 2014.03.15 답변등록 answer_create() 함수 수정 : POST, GET으로 분리
@login_required(login_url='common:login') # 2024.03.19 답변등록하려면 login 먼저하라고!
def answer_create(request, question_id):
    """
    pybo 답변 등록
    """

    question = get_object_or_404(Question, pk=question_id)

    # 2024.03.15 POST, GET으로 분리해서 추가
    if request.method == "POST" :
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False) # create_date가 지정될 때까지 임시저장
            answer.author = request.user # 추가한 속성 author 적용. 2024.03.19 
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            # return redirect('pybo:detail', question_id=question.id)
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=question.id), answer.id)) # 앵커 엘리먼트 위치로
    else :
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

# 2024.03.19 답변수정함수 추가
@login_required(login_url='common:login') 
def answer_modify(request, answer_id):
    """
    pybo 답변 수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    # 로그인한 사용자(request.user)와 답변자(answer.author)가 다르면 수정권한없음
    if request.user != answer.author: 
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)
    
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False) # create_date가 지정될 때까지 임시저장
            answer.author = request.user 
            answer.modify_date = timezone.now() # 수정일시 저장
            answer.save()
            # return redirect('pybo:detail', question_id=answer.question.id)
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=answer.question.id), answer.id)) # 앵커 엘리먼트 위치로
    else :
        form =AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)

# 2024.03.19 답변삭제함수 추가
@login_required(login_url='common:login') 
def answer_delete(request, answer_id):
    """
    pybo 답변 삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    # 로그인한 사용자(request.user)와 글쓴이(question.author)가 다르면 삭제권한없음
    if request.user != answer.author: 
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)

from django.shortcuts import render, get_object_or_404, redirect 
from django.http import HttpResponse # 2014.03.14 추가
# 2014.03.14 Question 추가 03.19 Answer 추가 03.20 Comment 추가
from .models import Question, Answer, Comment 
from .forms import QuestionForm, AnswerForm, CommentForm # 2024.03.20 CommentForm 추가
from django.utils import timezone # 2014.03.14 현재시간 timezone.now() 사용하기 위해
from django.core.paginator import Paginator # 2024.03.18 페이징 기능 추가하기
from django.contrib.auth.decorators import login_required # 2024.03.18 @login_required 애더네이션 적용하기
from django.contrib import messages # '수정권한이 없습니다' 오류 메세지 발생시키기 위해

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


# 2014.03.15 질문등록 question_create() 함수 추가
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
            return redirect('pybo:detail', question_id=question.id)
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
            return redirect('pybo:detail', question_id=answer.question.id)
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

# 2024.03.20 질문 댓글 등록 함수 추가
@login_required(login_url='common:login') # 2024.03.20 login 먼저하라고!
def comment_create_question(request, question_id):
    """
    pybo 질문 댓글 등록
    """
    question = get_object_or_404(Question, pk=question_id)

    if request.method == "POST" :
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) # create_date가 지정될 때까지 임시저장
            comment.author = request.user 
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            return redirect('pybo:detail', question_id=question.id)
    else :
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

# 2024.03.20 질문 댓글 수정 함수 추가
@login_required(login_url='common:login') 
def comment_modify_question(request, comment_id):
    """
    pybo 질문 댓글 수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    # 로그인한 사용자(request.user)와 댓글작성자(comment.author)와 다르면 수정권한없음
    if request.user != comment.author: 
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question.id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False) # create_date가 지정될 때까지 임시저장
            comment.author = request.user 
            comment.modify_date = timezone.now() 
            comment.save()
            return redirect('pybo:detail', question_id=comment.question.id)
    else :
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

# 2024.03.20 질문 댓글 삭제 함수 추가
@login_required(login_url='common:login') 
def comment_delete_question(request, comment_id):
    """
    pybo 질문 댓글 삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    # 로그인한 사용자(request.user)와 댓글작성자(comment.author)와 다르면 삭제권한없음
    if request.user != comment.author: 
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question.id)
    else :
        comment.delete()
    return redirect('pybo:detail', question_id=comment.question.id)

# 2024.03.20 답변 댓글 등록 함수 추가
@login_required(login_url='common:login') # 2024.03.20 login 먼저하라고!
def comment_create_answer(request, answer_id):
    """
    pybo 답변 댓글 등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)

    if request.method == "POST" :
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) # create_date가 지정될 때까지 임시저장
            comment.author = request.user 
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            return redirect('pybo:detail', question_id=comment.answer.question.id)
    else :
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

# 2024.03.20 답변 댓글 수정 함수 추가
@login_required(login_url='common:login') 
def comment_modify_answer(request, comment_id):
    """
    pybo 답변 댓글 수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    # 로그인한 사용자(request.user)와 댓글작성자(comment.author)와 다르면 수정권한없음
    if request.user != comment.author: 
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question.id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False) # create_date가 지정될 때까지 임시저장
            comment.author = request.user 
            comment.modify_date = timezone.now() 
            comment.save()
            return redirect('pybo:detail', question_id=comment.answer.question.id)
    else :
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

# 2024.03.20 답변 댓글 삭제 함수 추가
@login_required(login_url='common:login') 
def comment_delete_answer(request, comment_id):
    """
    pybo 답변 댓글 삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    # 로그인한 사용자(request.user)와 댓글작성자(comment.author)와 다르면 삭제권한없음
    if request.user != comment.author: 
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.answer.question.id)
    else :
        comment.delete()
    return redirect('pybo:detail', question_id=comment.answer.question.id)
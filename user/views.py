from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import UserModel
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.auth.decorators import login_required


# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated  # is_authenticated : 로그인 되어 있는지 검사
        if user:
            return redirect('/')  # 로그인 한 사용자라면 home.html 이동
        else:
            return render(request, 'user/signup.html')  # 로그인 하지 않은 사용자라면 회원가입 페이지로 이동

    elif request.method == 'POST':
        # POST 받은 username 저장 없다면 None
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')

        if password != password2:
            # 패스워드 확인이 틀릴 경우
            return render(request, 'user/signup.html', {'error': '패스워드가 일치하지 않습니다'})
        else:
            # 사용자 이름과 비밀번호가 비어있을 경우
            if username == '' or password == '':
                return render(request, 'user/signup.html', {'error': '사용자 이름과 비밀번호는 필수 값 입니다'})

            # get_user_model() : 사용자 데이터의 DB 내 존재유무 검사
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                # 중복 사용자 이름일 경우
                return render(request, 'user/signup.html', {'error': '이미 존재하는 사용자 이름입니다'})
            else:
                # django의 auth_user에 존재하는 create_user 사용
                UserModel.objects.create_user(username=username, password=password, bio=bio)
                return redirect('/sign-in')


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # 인증 기능 모듈을 먼저 불러온다
        # authenticate : 암호화된 비밀번호와 현재 입력된 비밀번호와 일치하는지 그게 사용자와 맞는지까지 확인
        me = auth.authenticate(request, username=username, password=password)
        if me is not None:
            auth.login(request, me)  # 세션과 같은 로그인과 관련된 처리들을 django가 해준다
            return redirect('/')  # tweet/views.py의 home 실행
        else:
            return render(request, 'user/signin.html', {'error': '잘못된 사용자 이름 또는 비밀번호입니다'})

    elif request.method == 'GET':
        user = request.user.is_authenticated  # is_authenticated : 로그인 되어 있는지 검사
        if user:
            return redirect('/')  # 로그인 한 사용자라면 home.html 이동
        else:
            return render(request, 'user/signin.html')  # 로그인 하지 않은 사용자라면 로그인 페이지로 이동


# @login_required : 사용자가 로그인이 되어 있어야만 접근 할 수 있는 함수라고 정의
@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자 불러오기, exclude로 로그인 한 사용자 제외
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user
    target_user = UserModel.objects.get(id=id)
    # target_user를 follow 하는 모든 user을 불러와서 me가 있는지 검사
    if me in target_user.followee.all():
        # 이미 follow가 되어 있다면 팔로우 취소
        target_user.followee.remove(request.user)
    else:
        # follow가 되어 있지 않다면 팔로우
        target_user.followee.add(request.user)
    return redirect('/user')

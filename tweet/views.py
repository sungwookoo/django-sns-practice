from django.views.generic import ListView, TemplateView
from django.shortcuts import render, redirect
from .models import TweetModel, TweetComment
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    user = request.user.is_authenticated  # is_authenticated : 로그인 되어 있는지 검사
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')


def tweet(request):
    if request.method == 'GET':
        user = request.user.is_authenticated  # is_authenticated : 로그인 되어 있는지 검사
        if user:
            all_tweet = TweetModel.objects.all().order_by('-created_at')  # -created_at : created_at 기준 역순 (최신 먼저)
            return render(request, 'tweet/home.html', {'tweet': all_tweet})  # 로그인 한 사용자라면 home.html 이동
        else:
            return redirect('/sign-in')  # 로그인 하지 않은 사용자라면 로그인 페이지로 이동

    elif request.method == 'POST':
        user = request.user  # 지금 로그인 되어있는 사용자의 정보 전체를 가져온다
        content = request.POST.get('my-content', '')
        tags = request.POST.get('tag', '').split(',')

        # 내용이 비어있을 경우
        if content == '':
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'error': '내용을 입력해주세요', 'tweet': all_tweet})
        else:
            my_tweet = TweetModel.objects.create(author=user, content=content)
            for tag in tags:
                tag = tag.strip() # strip() : 공백 제거
                if tag != '':
                    my_tweet.tags.add(tag)

            my_tweet.save()
            return redirect('/tweet')


# login_required : 로그인이 되어 있어야만 실행할 수 있음
@login_required
def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')


@login_required
def detail_tweet(request, id):
    if request.method == 'GET':
        user = request.user.is_authenticated  # is_authenticated : 로그인 되어 있는지 검사
        if user:
            target_tweet = TweetModel.objects.get(id=id)
            comment = TweetComment.objects.filter(tweet_id=id)
            return render(request, 'tweet/tweet_detail.html', {'tweet': target_tweet, 'comment': comment})
        else:
            return redirect('/sign-in')  # 로그인 하지 않은 사용자라면 로그인 페이지로 이동


@login_required
def write_comment(request, id):
    if request.method == 'POST':
        user = request.user
        target_tweet = TweetModel.objects.get(id=id)
        my_comment = TweetComment()
        my_comment.author = user
        my_comment.tweet = target_tweet
        my_comment.comment = request.POST.get('comment', '')
        my_comment.save()
        return redirect('/tweet/' + str(id))


@login_required
def delete_comment(request, id):
    my_comment = TweetComment.objects.get(id=id)
    my_comment.delete()
    return redirect('/tweet/' + str(my_comment.tweet_id))


class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context

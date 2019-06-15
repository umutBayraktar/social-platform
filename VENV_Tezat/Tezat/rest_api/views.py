from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from article.models import Article,Comment,Reply,RelatedLink
from user.models import UserNormal
from .serializers import (ArticleSerializer,ArticleListSerializer,CommentSerializer,
                        ReplySerializer,CommentUserSerializer,RelatedLinkSerializer,
                          DiscussCommentSerializer,DiscussionListSerializer,DiscussionDetailSerializer,
                          DiscussionReplySerializer,TimelineSerializer)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http import JsonResponse,Http404,response
from .pagination import CommentPageNumberPagination,ReplyPageNumberPagination
from django.db.models import Q
from discussion.models import Discussion,DiscussionComment,DiscussionReply
from tag.models import Tag
from notifications.signals import notify




class AllArticleList(ListAPIView):

    serializer_class = ArticleListSerializer
    pagination_class = ReplyPageNumberPagination
    def get_queryset(self,*args,**kwargs):

        query_set= Article.objects.filter(is_active=True)
        if(query_set):
            return query_set
        return JsonResponse(serializer.errors,status=400)


class PopularArticleList(ListAPIView):

    serializer_class = ArticleListSerializer
    pagination_class = ReplyPageNumberPagination

    def get_queryset(self,*args,**kwargs):

        query_set= Article.objects.filter(is_active=True).order_by("-pageview")
        if query_set:
            return query_set
        return JsonResponse(serializer.errors,status=400)

class NewAddedArticleList(ListAPIView):

    serializer_class = ArticleListSerializer
    pagination_class = ReplyPageNumberPagination
    def get_queryset(self,*args,**kwargs):

        query_set= Article.objects.filter(is_active=True).order_by("-created_date")
        if(query_set):
            return query_set
        return JsonResponse(serializer.errors,status=400)

class ArticleDetail(APIView):


    def get(self,request,id):
        article=Article.objects.get(id=id)
        serializer=ArticleSerializer(article,many=False)
        article.pageview+=1
        article.save()
        return Response(serializer.data)

    def post(self):
        pass

class ArticleLike(APIView):

    #authentication_classes = (authentication.SessionAuthentication)
    #permission_classes = (IsAuthenticated)

    def get(self, request, id):
        article=get_object_or_404(Article,id=id)
        user =UserNormal.objects.get(username=self.request.user)
        count=0
        if user in article.likes.all():
            article.likes.remove(user)
        elif user in article.dislikes.all():
            article.dislikes.remove(user)
            article.likes.add(user)
        else:
            article.likes.add(user)
        like_count = article.likes.count()
        dislike_count = article.dislikes.count()
        response = {
            'like': like_count,
            'dislike': dislike_count
        }
        return Response(response)

class ArticleDislike(APIView):

    #authentication_classes = (authentication.SessionAuthentication)
    #permission_classes = (IsAuthenticated)

    def get(self, request, id):
        article=get_object_or_404(Article,id=id)
        user =UserNormal.objects.get(username=self.request.user)
        if user in article.dislikes.all():
            article.dislikes.remove(user)
        elif user in article.likes.all():
            article.likes.remove(user)
            article.dislikes.add(user)
        else:
            article.dislikes.add(user)
        like_count = article.likes.count()
        dislike_count=article.dislikes.count()
        response={
            'like':like_count,
            'dislike':dislike_count
        }
        return Response(response)

class ArticlePositiveComments(ListAPIView):

    serializer_class = CommentSerializer
    pagination_class = CommentPageNumberPagination
    def get_queryset(self,*args,**kwargs):
        article_id = self.request.GET.get("article")
        if int(article_id):
            query_set=Comment.objects.filter(article=article_id,is_positive=True).order_by("-created_date")
            return  query_set
        else:
            return JsonResponse(serializer.errors, status=400)

class ArticleNegativeComments(ListAPIView):

    serializer_class = CommentSerializer
    pagination_class = CommentPageNumberPagination

    def get_queryset(self,*args,**kwargs):
        article_id = self.request.GET.get("article")
        if int(article_id):
            query_set=Comment.objects.filter(article=article_id,is_positive=False).order_by("-created_date")
            return  query_set
        else:
            return JsonResponse(serializer.errors, status=400)

class AddComment(APIView):

    # permissions = [IsAuthenticatedOrReadOnly]
    # lookup_field ='pk'

    def get(self):
        pass

    def post(self, request, id):
        author = get_object_or_404(UserNormal, username=request.user.username)
        article = get_object_or_404(Article, pk=id)
        notification_recipient=get_object_or_404(UserNormal,pk=article.author)
        if article:
            article = article.pk
            data = {
                'author': author.id,
                'image': author.photo,
                'username': author.username,
                'article': article,
                'content': self.request.POST.get('content'),
                'is_positive':self.request.POST.get('is_positive'),
                'like_count': 0,
                'dislike_count': 0,
            }
            serializer = CommentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                notification_text="<a href=\"http://127.0.0.1:8000/articles/article/"+str(article)+"\" target=\"_blank\">yazınıza olumlu bir yorum yaptı</a>"
                notify.send(author, recipient=notification_recipient,verb=notification_text)
                return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

class CommentLike(APIView):

    #authentication_classes = (authentication.SessionAuthentication)
    #permission_classes = (IsAuthenticated)

    def get(self, request, id):
        comment=get_object_or_404(Comment,id=id)
        user =UserNormal.objects.get(username=self.request.user)
        count=0
        if user in comment.likes.all():
            comment.likes.remove(user)
        elif user in comment.dislikes.all():
            comment.dislikes.remove(user)
            comment.likes.add(user)
        else:
            comment.likes.add(user)
        like_count = comment.likes.count()
        dislike_count = comment.dislikes.count()
        response = {
            'like': like_count,
            'dislike': dislike_count
        }
        return Response(response)

class CommentDislike(APIView):

    #authentication_classes = (authentication.SessionAuthentication)
    #permission_classes = (IsAuthenticated)

    def get(self, request, id):
        comment=get_object_or_404(Comment,id=id)
        user =UserNormal.objects.get(username=self.request.user)
        if user in comment.dislikes.all():
            comment.dislikes.remove(user)
        elif user in comment.likes.all():
            comment.likes.remove(user)
            comment.dislikes.add(user)
        else:
            comment.dislikes.add(user)
        like_count = comment.likes.count()
        dislike_count=comment.dislikes.count()
        response={
            'like':like_count,
            'dislike':dislike_count
        }
        return Response(response)

class AddReply(APIView):

    # permissions = [IsAuthenticatedOrReadOnly]
    # lookup_field ='pk'

    def get(self):
        pass

    def post(self, request, id):
        author = get_object_or_404(UserNormal, username=request.user.username)
        comment = get_object_or_404(Comment, pk=id)
        if comment:
            comment = comment.pk
            data = {
                'author': author.id,
                'image': author.photo,
                'username': author.username,
                'parent': comment,
                'content': self.request.POST.get('content'),
                'like_count': 0,
                'dislike_count': 0,
            }
            serializer = ReplySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

class GetReplies(ListAPIView):

    serializer_class = ReplySerializer
    pagination_class = ReplyPageNumberPagination
    def get_queryset(self,*args,**kwargs):
        comment_id = self.request.GET.get("comment")
        if int(comment_id):
            parent= get_object_or_404(Comment,id=comment_id)
            return parent.replies.order_by("-created_date")
        else:
            return JsonResponse(serializer.errors, status=400)

class ReplyLike(APIView):

    #authentication_classes = (authentication.SessionAuthentication)
    #permission_classes = (IsAuthenticated)

    def get(self, request, id):
        reply=get_object_or_404(Reply,id=id)
        user =UserNormal.objects.get(username=self.request.user)
        count=0
        if user in reply.likes.all():
            reply.likes.remove(user)
        elif user in reply.dislikes.all():
            reply.dislikes.remove(user)
            reply.likes.add(user)
        else:
            reply.likes.add(user)
        like_count = reply.likes.count()
        dislike_count = reply.dislikes.count()
        response = {
            'like': like_count,
            'dislike': dislike_count
        }
        return Response(response)

class ReplyDislike(APIView):

    #authentication_classes = (authentication.SessionAuthentication)
    #permission_classes = (IsAuthenticated)

    def get(self, request, id):
        reply=get_object_or_404(Reply,id=id)
        user =UserNormal.objects.get(username=self.request.user)
        if user in reply.dislikes.all():
            reply.dislikes.remove(user)
        elif user in reply.likes.all():
            reply.likes.remove(user)
            reply.dislikes.add(user)
        else:
            reply.dislikes.add(user)
        like_count = reply.likes.count()
        dislike_count=reply.dislikes.count()
        response={
            'like':like_count,
            'dislike':dislike_count
        }
        return Response(response)


class GetPositiveRelatedLinks(ListAPIView):

    serializer_class = RelatedLinkSerializer
    pagination_class = CommentPageNumberPagination

    def get_queryset(self):

        article_id =self.request.GET.get("article")
        article_id =int(article_id)
        if int(article_id):
            query_set = RelatedLink.objects.filter(article=article_id,is_positive=True)
            return query_set
        return JsonResponse(serializer.errors,status=400)


class GetNegativeRelatedLinks(ListAPIView):

    serializer_class = RelatedLinkSerializer
    pagination_class = CommentPageNumberPagination

    def get_queryset(self):

        article_id =self.request.GET.get("article")
        article_id =int(article_id)
        if int(article_id):
            query_set = RelatedLink.objects.filter(article=article_id,is_positive=False)
            return query_set
        return JsonResponse(serializer.errors,status=400)


class AddRelatedLink(APIView):

    def get(self):
        pass

    def post(self,request,id):
        author = get_object_or_404(UserNormal, username=request.user.username)
        article = get_object_or_404(Article, pk=id)
        if article:
            article = article.pk
            data = {
                'article': article,
                'title': self.request.POST.get('title'),
                'author': author.id,
                'username': author.username,
                'link': self.request.POST.get('link'),
                'is_positive': self.request.POST.get('is_positive'),
            }


            serializer = RelatedLinkSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class GetDiscussComments(ListAPIView):

    serializer_class = DiscussCommentSerializer
    pagination_class = CommentPageNumberPagination

    def get_queryset(self):
        discuss_id = self.request.GET.get("discussion")
        discuss_id = int(discuss_id)
        if discuss_id:
            queryset = DiscussionComment.objects.filter(discussion=discuss_id).order_by("-created_date")
            return queryset
        return JsonResponse(serializer.errors,status=400)

class AddDiscussionComment(APIView):

    # permissions = [IsAuthenticatedOrReadOnly]
    # lookup_field ='pk'

    def get(self):
        pass

    def post(self, request, id):
        author = get_object_or_404(UserNormal, username=request.user.username)
        discussion = get_object_or_404(Discussion, pk=id)
        if discussion:
            discussion = discussion.pk
            data = {
                'author': author.id,
                'image': author.photo,
                'username': author.username,
                'discussion': discussion,
                'content': self.request.POST.get('content'),
                'like_count': 0,
                'dislike_count': 0,
            }
            serializer = DiscussCommentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class DiscussionsList(ListAPIView):

    serializer_class =DiscussionListSerializer
    pagination_class = CommentPageNumberPagination

    def get_queryset(self):
        return Discussion.objects.all()


class PopularDiscussionList(ListAPIView):

    serializer_class = DiscussionListSerializer
    pagination_class = CommentPageNumberPagination
    def get_queryset(self,*args,**kwargs):

        query_set= Discussion.objects.order_by("-pageview")
        if(query_set):
            return query_set
        return JsonResponse(serializer.errors,status=400)

class NewAddedDiscussionList(ListAPIView):

    serializer_class = DiscussionListSerializer
    pagination_class = CommentPageNumberPagination
    def get_queryset(self,*args,**kwargs):

        query_set= Discussion.objects.order_by("-created_date")
        if(query_set):
            return query_set
        return JsonResponse(serializer.errors,status=400)



class DiscussionDetail(APIView):


    def get(self,request,id):
        id =int(id)
        if id:
            discussion = get_object_or_404(Discussion, id=id)
            serializer = DiscussionDetailSerializer(discussion, many=False)
            discussion.pageview += 1
            discussion.save()
            return Response(serializer.data)
        return  JsonResponse(serializer.errors,status=400)

    def post(self):
        pass

class DiscussionCommentLike(APIView):

    #authentication_classes = (authentication.SessionAuthentication)
    #permission_classes = (IsAuthenticated)

    def get(self, request, id):
        comment=get_object_or_404(DiscussionComment,id=id)
        user =UserNormal.objects.get(username=self.request.user)
        count=0
        if user in comment.likes.all():
            comment.likes.remove(user)
        elif user in comment.dislikes.all():
            comment.dislikes.remove(user)
            comment.likes.add(user)
        else:
            comment.likes.add(user)
        like_count = comment.likes.count()
        dislike_count = comment.dislikes.count()
        response = {
            'like': like_count,
            'dislike': dislike_count
        }
        return Response(response)

class DiscussionCommentDislike(APIView):

    #authentication_classes = (authentication.SessionAuthentication)
    #permission_classes = (IsAuthenticated)

    def get(self, request, id):
        comment=get_object_or_404(DiscussionComment,id=id)
        user =UserNormal.objects.get(username=self.request.user)
        if user in comment.dislikes.all():
            comment.dislikes.remove(user)
        elif user in comment.likes.all():
            comment.likes.remove(user)
            comment.dislikes.add(user)
        else:
            comment.dislikes.add(user)
        like_count = comment.likes.count()
        dislike_count=comment.dislikes.count()
        response={
            'like':like_count,
            'dislike':dislike_count
        }
        return Response(response)

class DiscussionLike(APIView):

    #authentication_classes = (authentication.SessionAuthentication)
    #permission_classes = (IsAuthenticated)

    def get(self, request, id):
        discussion=get_object_or_404(Discussion,id=id)
        user =UserNormal.objects.get(username=self.request.user)
        count=0
        if user in discussion.likes.all():
            discussion.likes.remove(user)
        elif user in discussion.dislikes.all():
            discussion.dislikes.remove(user)
            discussion.likes.add(user)
        else:
            discussion.likes.add(user)
        like_count = discussion.likes.count()
        dislike_count = discussion.dislikes.count()
        response = {
            'like': like_count,
            'dislike': dislike_count
        }
        return Response(response)

class DiscussionDislike(APIView):

    #authentication_classes = (authentication.SessionAuthentication)
    #permission_classes = (IsAuthenticated)

    def get(self, request, id):
        discussion=get_object_or_404(Discussion,id=id)
        user =UserNormal.objects.get(username=self.request.user)
        if user in discussion.dislikes.all():
            discussion.dislikes.remove(user)
        elif user in discussion.likes.all():
            discussion.likes.remove(user)
            discussion.dislikes.add(user)
        else:
            discussion.dislikes.add(user)
        like_count = discussion.likes.count()
        dislike_count=discussion.dislikes.count()
        response={
            'like':like_count,
            'dislike':dislike_count
        }
        return Response(response)


class AddDiscussionReply(APIView):

    # permissions = [IsAuthenticatedOrReadOnly]
    # lookup_field ='pk'

    def get(self):
        pass

    def post(self, request, id):
        author = get_object_or_404(UserNormal, username=request.user.username)
        comment = get_object_or_404(DiscussionComment, pk=id)
        if comment:
            comment = comment.pk
            data = {
                'author': author.id,
                'image': author.photo,
                'username': author.username,
                'parent': comment,
                'content': self.request.POST.get('content'),
                'like_count': 0,
                'dislike_count': 0,
            }
            serializer = DiscussionReplySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

class GetDiscussionReplies(ListAPIView):

    serializer_class = DiscussionReplySerializer
    pagination_class = ReplyPageNumberPagination
    def get_queryset(self,*args,**kwargs):
        comment_id = self.request.GET.get("comment")
        if int(comment_id):
            parent= get_object_or_404(DiscussionComment,id=comment_id)
            return parent.replies.order_by("-created_date")
        else:
            return JsonResponse(serializer.errors, status=400)


class DiscussionReplyLike(APIView):

    #authentication_classes = (authentication.SessionAuthentication)
    #permission_classes = (IsAuthenticated)

    def get(self, request, id):
        reply=get_object_or_404(DiscussionReply,id=id)
        user =UserNormal.objects.get(username=self.request.user)
        count=0
        if user in reply.likes.all():
            reply.likes.remove(user)
        elif user in reply.dislikes.all():
            reply.dislikes.remove(user)
            reply.likes.add(user)
        else:
            reply.likes.add(user)
        like_count = reply.likes.count()
        dislike_count = reply.dislikes.count()
        response = {
            'like': like_count,
            'dislike': dislike_count
        }
        return Response(response)

class DiscussionReplyDislike(APIView):

    #authentication_classes = (authentication.SessionAuthentication)
    #permission_classes = (IsAuthenticated)

    def get(self, request, id):
        reply=get_object_or_404(DiscussionReply,id=id)
        user =UserNormal.objects.get(username=self.request.user)
        if user in reply.dislikes.all():
            reply.dislikes.remove(user)
        elif user in reply.likes.all():
            reply.likes.remove(user)
            reply.dislikes.add(user)
        else:
            reply.dislikes.add(user)
        like_count = reply.likes.count()
        dislike_count=reply.dislikes.count()
        response={
            'like':like_count,
            'dislike':dislike_count
        }
        return Response(response)



class GetUserArticles(ListAPIView):

    serializer_class = ArticleListSerializer
    pagination_class = CommentPageNumberPagination

    def get_queryset(self,*args,**kwargs):
        username=self.request.GET.get("user")
        if username:
            user=get_object_or_404(UserNormal,username=username)
            query =user.articles.filter(is_active=True).order_by("-created_date")
            if query:
                return query
        return JsonResponse(serializer.errors, status=400)

class GetUserDiscussions(ListAPIView):

    serializer_class = DiscussionListSerializer
    pagination_class = CommentPageNumberPagination

    def get_queryset(self,*args,**kwargs):
        username=self.request.GET.get("user")
        if username:
            user=get_object_or_404(UserNormal,username=username)
            query =user.discussions.order_by("-created_date")
            if query:
                return query
        return JsonResponse(serializer.errors, status=400)

class GetTagArticles(ListAPIView):

    serializer_class = ArticleListSerializer
    pagination_class = CommentPageNumberPagination

    def get_queryset(self,*args,**kwargs):
        tag_name=self.request.GET.get("tag")
        if tag_name:
            tag=get_object_or_404(Tag,name=tag_name)
            query =tag.article.filter(is_active=True).order_by("-created_date")
            if query:
                return query
        return JsonResponse(serializer.errors, status=400)

class GetTagDiscussions(ListAPIView):

    serializer_class = DiscussionListSerializer
    pagination_class = CommentPageNumberPagination

    def get_queryset(self,*args,**kwargs):
        tag_name=self.request.GET.get("tag")
        if tag_name:
            tag=get_object_or_404(Tag,name=tag_name)
            query =tag.discussion.order_by("-created_date")
            if query:
                return query
        return JsonResponse(serializer.errors, status=400)


class FollowTag(APIView):

    #authentication_classes = (authentication.SessionAuthentication)
    #permission_classes = (IsAuthenticated)

    def get(self, request,tagname):
        tag=get_object_or_404(Tag,name=tagname)
        user =UserNormal.objects.get(username=self.request.user)
        count=0
        if tag in user.tags.all():
            user.tags.remove(tag)
            message="Takip Et"
        else:
            user.tags.add(tag)
            message = "Takipten Çık"
        response={
            'message':message
        }
        return Response(response)

class FollowUser(APIView):

    #authentication_classes = (authentication.SessionAuthentication)
    #permission_classes = (IsAuthenticated)

    def get(self, request,username):
        user=get_object_or_404(UserNormal,username=username)#takip edilen
        follower =UserNormal.objects.get(username=self.request.user) #takip eden
        count=0
        if follower in user.followers.all(): #takip ediyorsam
            user.followers.remove(follower) #onun takipçilerinden beni sil
            follower.following.remove(user) #benim takip ettiklerimden onu sil
            message="Takip Et"
        else:
            user.followers.add(follower) #onun takipçilerine beni ekle
            follower.following.add(user) #benim takip ettiklerime onu ekle
            message = "Takipten Çık"
        response={
            'message':message
        }
        return Response(response)


class GetTimeLineFollowingArticle(ListAPIView):
    serializer_class = ArticleListSerializer
    pagination_class = CommentPageNumberPagination

    def get_queryset(self,*args,**kwargs):
        user = get_object_or_404(UserNormal, username=self.request.user)
        if user:
            qs_following=user.following.all()
            following_articles= Article.objects.filter(author=qs_following).order_by("-created_date")
            return following_articles
        return JsonResponse(serializer.errors, status=400)


class GetTimeLineFollowingDiscussions(ListAPIView):
    serializer_class = DiscussionListSerializer
    pagination_class = CommentPageNumberPagination

    def get_queryset(self,*args,**kwargs):
        user = get_object_or_404(UserNormal, username=self.request.user)
        if user:
            qs_following=user.following.all()
            following_discussions = Discussion.objects.filter(author=qs_following).order_by("-created_date")
            return following_discussions
        return JsonResponse(serializer.errors, status=400)




class GetTimeLineTagArticle(ListAPIView):
    serializer_class = ArticleListSerializer
    pagination_class = CommentPageNumberPagination

    def get_queryset(self,*args,**kwargs):
        user = get_object_or_404(UserNormal, username=self.request.user)
        if user:
            qs_tag = user.tags.all()
            tag_articles = Article.objects.filter(tags=qs_tag).order_by("-created_date")
            return tag_articles
        return JsonResponse(serializer.errors, status=400)

class GetTimeLineTagDiscussion(ListAPIView):
    serializer_class = DiscussionListSerializer
    pagination_class = CommentPageNumberPagination

    def get_queryset(self,*args,**kwargs):
        user = get_object_or_404(UserNormal, username=self.request.user)
        if user:
            qs_tag = user.tags.all()
            tag_discussions = Discussion.objects.filter(tags=qs_tag).order_by("-created_date")
            return tag_discussions
        return JsonResponse(serializer.errors, status=400)










class NotificationRead(APIView):

    def get(self,request):

        user=get_object_or_404(UserNormal,username=request.user.username)
        message=""
        if(user):
            qs=user.notifications.all()
            qs.mark_all_as_read()
            message="bildirimler silindi"
            return JsonResponse({"message":message})
        return JsonResponse({"message":"silinmedi"})




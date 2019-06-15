from rest_framework import  serializers
from article.models import Article,Comment,Reply,RelatedLink
from user.models import UserNormal,UserStatistics
from tag.models import Tag
from discussion.models import DiscussionComment,Discussion,DiscussionReply
from datetime import datetime


class UsernameSerializer(serializers.ModelSerializer):

    class Meta:
        model =UserNormal
        fields = ["username"]


class ArticleTagSerializer(serializers.ModelSerializer):

    class Meta:
        model=Tag
        fields="__all__"


class ArticleSerializer(serializers.ModelSerializer):

    author =UsernameSerializer(many=False,read_only=True)
    tags =ArticleTagSerializer(many=True,read_only=True)

    class Meta:
        model =Article
        fields = ("id","title","author","image","created_date","author","content","tags","pageview")


class ArticleListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()#UsernameSerializer(many=False, read_only=True)

    class Meta:
        model = Article
        fields=["id","title","image","author","pageview","created_date"]

    def get_author(self,obj):
        return obj.author.username

class UserIstatisticSerializer(serializers.ModelSerializer):

    class Meta:
        model=UserStatistics
        fields = "__all__"

class CommentUserSerializer(serializers.ModelSerializer):

    #user =serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    class Meta:
        model =UserNormal
        fields =['id','username','image']

    #def get_user(self,obj):
    #    return obj.username

    def get_image(self,obj):
        if obj.photo:
            return  obj.photo.url
        return None

class CommentSerializer(serializers.ModelSerializer):

    like_count=serializers.SerializerMethodField()
    dislike_count =serializers.SerializerMethodField()
    #author = CommentUserSerializer(many=False)
    username=serializers.SerializerMethodField()
    image =serializers.SerializerMethodField()
    created_date=serializers.SerializerMethodField()
    class Meta:
        model  = Comment
        fields = ["id","created_date","content","author","username","image","is_positive","article","like_count","dislike_count"]


    def get_like_count(self,obj):
        return obj.likes.count()

    def get_dislike_count(self,obj):
        return obj.dislikes.count()

    def get_username(self,obj):
        return obj.author.username

    def get_image(self,obj):
        if obj.author.photo:
            return  obj.author.photo.url
        return None
    def get_created_date(self,obj):
        time=obj.created_date
        time=time.strftime('%m/%d/%Y %H:%M')
        return time


class ReplySerializer(serializers.ModelSerializer):

    like_count=serializers.SerializerMethodField()
    dislike_count =serializers.SerializerMethodField()
    username=serializers.SerializerMethodField()
    image =serializers.SerializerMethodField()
    created_date =serializers.SerializerMethodField()

    class Meta:
        model  = Reply
        fields = ["id","created_date","content","author","username","image","parent","like_count","dislike_count"]


    def get_like_count(self,obj):
        return obj.likes.count()

    def get_dislike_count(self,obj):
        return obj.dislikes.count()

    def get_username(self,obj):
        return obj.author.username

    def get_image(self,obj):
        if obj.author.photo:
            return  obj.author.photo.url
        return None

    def get_created_date(self,obj):
        time=obj.created_date
        time=time.strftime('%m/%d/%Y %H:%M')
        return time

    #def get_created_date(self,obj):
    #    time=obj.created_date
    #    time=time.strftime('%m/%d/%Y %H:%M')
    #    return time



class RelatedLinkSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    created_date =serializers.SerializerMethodField()

    class Meta:
        model = RelatedLink
        fields = ['id','article','title','author','link','is_positive','created_date','username']

    def get_username(self,obj):
        return obj.author.username

    def get_created_date(self,obj):
        time=obj.created_date
        time=time.strftime('%m/%d/%Y %H:%M')
        return time




class DiscussCommentSerializer(serializers.ModelSerializer):

    like_count=serializers.SerializerMethodField()
    dislike_count =serializers.SerializerMethodField()
    #author = CommentUserSerializer(many=False)
    username=serializers.SerializerMethodField()
    image =serializers.SerializerMethodField()
    created_date=serializers.SerializerMethodField()
    class Meta:
        model  = DiscussionComment
        fields = ["id","created_date","content","author","username","image","discussion","like_count","dislike_count"]


    def get_like_count(self,obj):
        return obj.likes.count()

    def get_dislike_count(self,obj):
        return obj.dislikes.count()

    def get_username(self,obj):
        return obj.author.username

    def get_image(self,obj):
        if obj.author.photo:
            return  obj.author.photo.url
        return None
    def get_created_date(self,obj):
        time=obj.created_date
        time=time.strftime('%m/%d/%Y %H:%M')
        return time



class DiscussionListSerializer(serializers.ModelSerializer):

    author =serializers.SerializerMethodField()
    created_date =serializers.SerializerMethodField()
    text =serializers.SerializerMethodField()

    class Meta:
        model= Discussion
        fields = ["id","image","created_date","text","pageview","video_url","author"]


    def get_author(self,obj):
        return obj.author.username

    def get_created_date(self, obj):
        time = obj.created_date
        time = time.strftime('%m/%d/%Y %H:%M')
        return time

    def get_text(self,obj):
        text =obj.text[:100]
        return text

class DiscussionDetailSerializer(serializers.ModelSerializer):
    author = UsernameSerializer(many=False, read_only=True)
    tags = ArticleTagSerializer(many=True, read_only=True)

    class Meta:
        model = Discussion
        fields = ("id", "text", "author", "image", "created_date", "video_url", "tags", "pageview")


class DiscussionReplySerializer(serializers.ModelSerializer):

    like_count=serializers.SerializerMethodField()
    dislike_count =serializers.SerializerMethodField()
    username=serializers.SerializerMethodField()
    image =serializers.SerializerMethodField()
    created_date =serializers.SerializerMethodField()

    class Meta:
        model  = DiscussionReply
        fields = ["id","created_date","content","author","username","image","parent","like_count","dislike_count"]


    def get_like_count(self,obj):
        return obj.likes.count()

    def get_dislike_count(self,obj):
        return obj.dislikes.count()

    def get_username(self,obj):
        return obj.author.username

    def get_image(self,obj):
        if obj.author.photo:
            return  obj.author.photo.url
        return None

    def get_created_date(self,obj):
        time=obj.created_date
        time=time.strftime('%m/%d/%Y %H:%M')
        return time

class TimelineSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()  # UsernameSerializer(many=False, read_only=True)
    image  = serializers.SerializerMethodField()
    text   =serializers.CharField()

    class Meta:
        model = Article,Discussion
        fields = ["id", "title","text","image", "author", "pageview", "created_date"]

    def get_author(self, obj):
        return obj.author.username

    def get_image(self,obj):
        if obj.author.photo:
            return  obj.author.photo.url
        return None



"""
def create_comment_serializer(model_type='post', slug=None, parent_id=None, user=None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                'id',
                'content',
                'timestamp',
            ]
        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.slug = slug
            self.parent_obj = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() ==1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise ValidationError("This is not a valid content type")
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=self.slug)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise ValidationError("This is not a slug for this content type")
            return data

        def create(self, validated_data):
            content = validated_data.get("content")
            if user:
                main_user = user
            else:
                main_user = User.objects.all().first()
            model_type = self.model_type
            slug = self.slug
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(
                    model_type, slug, content, main_user,
                    parent_obj=parent_obj,
                    )
            return comment

    return CommentCreateSerializer

"""
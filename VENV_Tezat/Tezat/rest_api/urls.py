from django.conf.urls import url
from .views import *
from .views import AllArticleList
from rest_framework.urlpatterns import format_suffix_patterns


app_name="rest_api"

urlpatterns=[

    url("articles/popular/",PopularArticleList.as_view(),name="popular_articles"),
    url("articles/new/",NewAddedArticleList.as_view(),name="new_articles"),
    url("article/(P?[0-9]+)/$",ArticleDetail.as_view(),name="article_datail"),
    url('article/like/(P?[0-9]+)/$', ArticleLike.as_view(), name="article_like"),
    url('article/dislike/(P?[0-9]+)/$', ArticleDislike.as_view(), name="article_dislike"),
    url('article/add-comment/(P?[0-9]+)/$',AddComment.as_view(),name="article_add_comment"),
    url('article/positive-comments/',ArticlePositiveComments.as_view(),name="positive_comments"),
    url('article/negative-comments/', ArticleNegativeComments.as_view(), name="negative_comments"),
    url('article/comment/like/(P?[0-9]+)/$', CommentLike.as_view(), name="comment_like"),
    url('article/comment/dislike/(P?[0-9]+)/$', CommentDislike.as_view(), name="comment_dislike"),
    url('article/add-reply/(P?[0-9]+)/$', AddReply.as_view(), name="comment_add_reply"),
    url('article/replies',GetReplies.as_view(),name="get_comment_replies"),
    url('article/reply/like/(P?[0-9]+)/$', ReplyLike.as_view(), name="reply_like"),
    url('article/reply/dislike/(P?[0-9]+)/$', ReplyDislike.as_view(), name="reply_dislike"),
    url('article/positive-related/$',GetPositiveRelatedLinks.as_view(),name="positive_related_articles"),
    url('article/negative-related/$',GetNegativeRelatedLinks.as_view(),name="negative_related_articles"),
    url('add-related-link/(P?[0-9]+)/$',AddRelatedLink.as_view(),name="add_related_link"),
    url('discussion/(P?[0-9]+)/$',DiscussionDetail.as_view(),name="discussion_detail"),
    url('discussion/add-comment/(P?[0-9]+)/$',AddDiscussionComment.as_view(),name="add_discussion_comment"),
    url('discussion/comments/',GetDiscussComments.as_view(),name="get_discussion_comments"),
    #url('discussions/',DiscussionsList.as_view(),name="all_discussions"),
    url('discussions/popular/$',PopularDiscussionList.as_view(),name="popular_discussions"),
    url('discussions/new/$',NewAddedDiscussionList.as_view(),name="new_discussions"),
    url('discussion/comment/like/(P?[0-9]+)/$', DiscussionCommentLike.as_view(), name="discussion_comment_like"),
    url('discussion/comment/dislike/(P?[0-9]+)/$', DiscussionCommentDislike.as_view(), name="discussion_comment_dislike"),
    url('discussion/like/(P?[0-9]+)/$', DiscussionLike.as_view(), name="discussion_like"),
    url('discussion/dislike/(P?[0-9]+)/$', DiscussionDislike.as_view(), name="discussion_dislike"),
    url('discussion/add-reply/(P?[0-9]+)/$',AddDiscussionReply.as_view(), name="disc_comment_add_reply"),
    url('discussion/replies',GetDiscussionReplies.as_view(),name="get_disc_comment_replies"),
    url('discussion/reply/like/(P?[0-9]+)/$', DiscussionReplyLike.as_view(), name="disc_reply_like"),
    url('discussion/reply/dislike/(P?[0-9]+)/$', DiscussionReplyDislike.as_view(), name="disc_reply_dislike"),
    url('user/articles/$',GetUserArticles.as_view(),name="get_user_articles"),
    url('user/discussions/$',GetUserDiscussions.as_view(),name="get_user_discussions"),
    url('tag/articles/$',GetTagArticles.as_view(),name="get_tag_articles"),
    url('tag/discussions/$',GetTagDiscussions.as_view(),name="get_tag_discussions"),
    url('tag/follow/(.+)/$',FollowTag.as_view(),name="follow_unfollow_tag"),
    url('user/follow/(.+)/$',FollowUser.as_view(),name="follow_unfollow_user"),
    url('bildirimoku/$',NotificationRead.as_view(),name="notification_read"),
    url('timeline/following-articles/$',GetTimeLineFollowingArticle.as_view(),name="timeline_following_article"),
    url('timeline/following-discussions/$',GetTimeLineFollowingDiscussions.as_view(),name="timeline_following_discussions"),
    url('timeline/tag-articles/$',GetTimeLineTagArticle.as_view(),name="timeline_tag_article"),
    url('timeline/tag-discussions/$',GetTimeLineTagDiscussion.as_view(),name="timeline_tag_article"),

]
urlpatterns =format_suffix_patterns(urlpatterns)
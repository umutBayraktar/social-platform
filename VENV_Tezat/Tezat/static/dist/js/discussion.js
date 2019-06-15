/* Get Discussion */
        function getDiscussion(DiscussionId) {
            $.get(API_URL + "discussion/" + DiscussionId, function (data) {

                var $el = $("#discussion");

                var template = `
                    <p id="discussion_text">${data.text}</p>`
                    if(data.image != null){
                    template += `<img id="discussion_image" src="${data.image}" alt="" width="560" height="315" class="card-img-top">`
                    }
                    else if (data.video_url != null){
                    template += `<a href="${data.video_url}" target="_blank">
<img src="https://cdn.webtekno.com/media/cache/content_detail_v2/article/48713/youtube-un-diger-uygulamalari-kullanirken-acik-kalan-resim-icinde-resim-modu-ucretsiz-oluyor-1530178593.jpg" alt="" width="560" height="320">
</a>`
                    }
                    template +=`
                    <div class="card-header">
                        
                        <h4 id="discussion_created_date" class="card-subtitle mb-2 text-muted">${data.created_date}</h4>
                        <h3 id="discussion_pageview" class="card-subtitle mb-2 text-muted"> <i class="fas fa-eye"></i>${data.pageview}</h3>
                        <a id="discussion_author" href="{% url 'user:user_page'%}?user=${data.author.username}"  class="card-title">${data.author.username}</a>
                    </div>
                    
                    <div class="navbar-light bg-light" style="padding: 5px;margin:5px 5px; text-align: center">
                        
                        <button type="button" id="btn_discussion_comments" class="btn btn-success col-md-1">
                            <img style="width: 20px" src="{% static 'dist/img/icons/positive-comment.png' %}">
                        </button>
                        <button type="button" id="btn_discussion_like" class="btn btn-success col-md-1">
                            <i class="fa fa-thumbs-up" aria-hidden="true"></i>
                            <span id="like_count"></span>
                        </button>
                        <button type="button" id="btn_discussion_dislike" class="btn btn-danger col-md-1">
                            <i class="fa fa-thumbs-down" aria-hidden="true"></i>
                            <span id="dislike_count"></span>
                        </button>                       
                       
                    </div>
                `;
                $el.html(template);

            })
        }

        /* Get Discussion */

         /* Like Discussion */
        function discussionLike(discussionId) {
            $.get(API_URL + "discussion/like/" + discussionId, function (data) {
                $("#like_count").text(data.like);
                $("#dislike_count").text(data.dislike);
            })
        }

        /* Like Discussion */

        /* Dislike Article */
        function discussionDisLike(discussionId) {
            $.get(API_URL + "discussion/dislike/" + discussionId, function (data) {
                $("#like_count").text(data.like);
                $("#dislike_count").text(data.dislike);
            })
        }

        /* Dislike Article */


         /* Get Discussion Comments */
        function getDiscussionComments(discussionId) {
            $.get(API_URL + "discussion/comments/?discussion=" + discussionId, function (data) {

                var comments = data.results;
                var template = ``;
                var comment_form = `<div class="add-comment-form">
                    <div class="row">
                        <div class="col-md-10">
                            <input type="text" class="form-control comment-input">
                        </div>
                        <div class="col-sm-2">
                            <button class="btn btn-primary btn_add_comment" id="comment">Yorum Ekle</button>
                        </div>
                    </div>
                </div>`;

                comments.forEach(function (item) {
                    template += `
                        <div class="card" data-comment-id="${item.id}">
                            <div class="card-body">
                                <div class="row">
                                    <div class="col-md-2">
                                        <img src="${item.image}" class="img img-rounded img-fluid"/>
                                        <p class="text-secondary text-center"> ${item.created_date}</p>
                                    </div>
                                    <div class="col-md-10">
                                        <p>
                                            <a class="float-left" href="{% url 'user:user_page'%}?user=${item.username}"><strong> ${item.username} </strong></a>
                                         </p>
                                       <div class="clearfix"></div>
                                        <p> ${item.content}</p>
                                        <p class="clearfix">
                                            <button class="float-right btn btn-outline-primary ml-2 btn_replies"><i class="fa fa-reply"></i> Replies</button>
                                            <button class="float-right btn text-white btn-danger ml-2 btn_dislike_comment"> <i class="fa fa-thumbs-down"></i> <span class="comment_dislike_count"></span></button>
                                            <button class="float-right btn text-white btn-success ml-2 btn_like_comment"> <i class="fa fa-thumbs-up"></i> <span class="comment_like_count"></span></button>
                                      </p>
                                      <div class="reply-container"></div>
                                   </div>
                                </div>
                            </div>
                        </div>
                    `;
                })


                $("#discussion-footer").html(template);
                $("#discussion-footer").append(comment_form);

            })
        }


        /* Get Discussion Comments */

        /* Comment Like */
        function commentLike(commentId, callback) {
            $.get(API_URL + "discussion/comment/like/" + commentId, function (data) {
                console.log(data);
                callback(data);
            })
        }


        /* Comment Like */

        /* Comment DisLike */
        function commentDisLike(commentId, callback) {
            $.get(API_URL + "discussion/comment/dislike/" + commentId, function (data) {
                callback(data);
            })
        }


        /* Comment DisLike */

        /* Get Replies */
        function getReplies(commentId, callback) {
            $.get(API_URL + "discussion/replies/?comment=" + commentId, function (data) {

                callback(data);

            })
        }

        /* Get Replies */

        /* Reply Like */
        function replyLike(replyId, callback) {
            $.get(API_URL + "discussion/reply/like/" + replyId, function (data) {
                console.log(data);
                callback(data);
            })
        }

        /* Reply Like */

         /* Reply DisLike */
        function replyDisLike(commentId, callback) {
            $.get(API_URL + "discussion/reply/dislike/" + commentId, function (data) {
                callback(data);
            })
        }


        /* Reply DisLike */


         /* Add Reply */
        function addReply(commentId, data, callback) {
            $.post(API_URL + "discussion/add-reply/" + commentId+"/", {

                content: data.content,
                csrfmiddlewaretoken:data.csrfmiddlewaretoken

            }).done(function (data) {
                callback(commentId);
            })
        }


        /* Add Reply */

        /* Add Comment */

        function addComment(discussionId, data, callback) {
            $.post(API_URL + "discussion/add-comment/" + discussionId + "/", {
                content: data.content,
                csrfmiddlewaretoken: data.csrfmiddlewaretoken
            }).done(function (data) {
                callback(data);
            })

        }


        /* Add Comment */
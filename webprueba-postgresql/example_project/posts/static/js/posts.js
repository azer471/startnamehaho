$(document).ready(function() {

  function reorder_posts(){
    $(".ArticleItem li").sort(sort_li)
                       .appendTo('.ArticleItem');
  }

  function sort_li(a, b){
      return ($(b).data('position')) < ($(a).data('position')) ? 1 : -1;
  }

  //For getting CSRF token
  function getCookie(name) {
            var cookieValue = true;
            if (document.cookie && document.cookie != '') {
                  var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                 var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
               }
            }
        }
   return cookieValue;
  }


  $('.vote_wrapper').delegate( '.arrow', 'click', function(event) {
    event.preventDefault();
    var wrapper = $(event.delegateTarget)
    var csrftoken = getCookie('csrftoken');
    var up_down = $(this).attr('id');
    var post_id = parseInt($(wrapper).attr('id'), 10);

    $.ajax({
      url: '/posts/' + post_id + '/vote/',
      type: "POST",
      data: { csrfmiddlewaretoken: csrftoken,
      up_down: up_down,
      post_id: post_id
      },
      success: function(data) {
        console.log(data);
        $(wrapper).children('.score').text(data['votes']);
      },
      error : function(xhr,errmsg,err) {
      console.log(xhr.status + ": " + xhr.responseText);
      }
    });
  });



  $('.box_wrapper').delegate( '.flecha', 'click', function(event) {
    event.preventDefault();
    var wrapper = $(event.delegateTarget)
    var csrftoken = getCookie('csrftoken');
    var up_down = $(this).attr('id');
    var obj_id = parseInt($(wrapper).attr('id'), 10);

    $.ajax({
      url:  '/posts/' + obj_id + '/vote_comment/',
      type: "POST",
      data: { csrfmiddlewaretoken: csrftoken,
      up_down: up_down,
      obj_id: obj_id

      },
      success: function(data) {
        console.log(data);
        $(wrapper).children('.score').text(data['votes_comment']);
      },
      error : function(xhr,errmsg,err) {
      console.log(xhr.status + ": " + xhr.responseText);
      }
    });
  });




  $("a.myButton1").bind("click", function(){
    var link = $(this).attr("href");
    $.get(link, function(data) {
        $(this).parent("div").children('b#like_count').html(data);
    });
  });

  $("#submit").click(function(e) {
   e.preventDefault();
   var csrftoken = getCookie('csrftoken');
   var post_text = $('#id_post_text').val();

   $.ajax({
     url : window.location.href,
     type : "POST",
     data : { csrfmiddlewaretoken : csrftoken,
     post_text : post_text
     },
     success : function(json) {
       console.log(json);
       window.location.href = "/posts";
     },
     error : function(xhr,errmsg,err) {
     console.log(xhr.status + ": " + xhr.responseText);
     }
   });
  });

});

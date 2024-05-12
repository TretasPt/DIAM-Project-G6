$(document).ready(function(event){

    $('form#message_form').submit(function (event) {
        event.preventDefault();
        $.ajax({
            type:'POST',
            url:'/sendmessage',
            data:{
                group_id:$('#group_id').val(),
                message:$('#message_input').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (response) {
                func();
            }
        });
        $('#message_input').val('');
    });

    function func () {
        let shown_messages_id_list = []
        $('.message').each(function () {
            let message_id_text = $(this).attr('id');
            let message_id = parseInt(message_id_text.replace('message_',''));
            shown_messages_id_list.push(message_id)
        });
        $.ajax({
            type: 'POST',
            url: '../receivemessage',
            data:{
                group_id:$('#group_id').val(),
                shown_messages_id_list:shown_messages_id_list,
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (response) {
                for (let key in response.messages_list) {
                    //alert(response.messages_list[key].id + response.messages_list[key].texto);
                    let message_id = response.messages_list[key].id;
                    let message_text = response.messages_list[key].texto;
                    let message = $('#message_template').clone();
                    message.removeAttr('id')
                    message.addClass('message')
                    message.attr('id', 'message_' + message_id)
                    message.removeClass('hiddensection')
                    message.children('.messagetext').append(message_text)
                    $('#group_messages_body').append(message);
                }
            }
        });
    }

    setInterval(func, 5000);
});
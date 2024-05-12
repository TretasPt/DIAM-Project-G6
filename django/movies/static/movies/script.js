let global = false

$(document).ready(function(event){

    $('.film.radio_option').click(function () {
        $('.film.radio_option.click').removeClass('click');
        let film_id_text = $(this).attr('id');
        let film_id = parseInt(film_id_text.replace('film_',''));
        $(this).next('input.radio').click();
    });

    $('.radio_option').click(function () {
       $(this).toggleClass('click');
    });

    $('.group.radio_option').click(function () {
        $('#global').removeClass('click');
        global = false;
    });

    $('.cinema.radio_option').click(function () {
        $('#global').removeClass('click');
        global = false;
    });

    $('#global').click(function () {
        if (global) {
            $('.group').each(function () {
                $(this).removeClass('click');
            });
            $('.cinema').each(function () {
                $(this).removeClass('click');
            });
        } else {
            $('.group').each(function () {
                $(this).addClass('click');
            });
            $('.cinema').each(function () {
                $(this).addClass('click');
            });
        }
        global = !global;
    })

    $('form#postform').submit(function(event) {
        $('.click.group').each(function () {
            let group_id_text = $(this).attr('id');
            let group_id = parseInt(group_id_text.replace('group_',''));
            let input = document.createElement('input');
            input.setAttribute('name', 'groups[]');
            input.setAttribute('value', group_id.toString());
            input.setAttribute('type', 'number');
            input.setAttribute('hidden', 'hidden');
            $('form').append(input);
        });
        $('.click.cinema').each(function () {
            let cinema_id_text = $(this).attr('id');
            let cinema_id = parseInt(cinema_id_text.replace('cinema_',''));
            let input = document.createElement('input');
            input.setAttribute('name', 'cinemas[]');
            input.setAttribute('value', cinema_id.toString());
            input.setAttribute('type', 'number');
            input.setAttribute('hidden', 'hidden');
            $('form').append(input);
        });
    });

    $('form#messageform').submit(function (event) {
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
                    let message_id = response.messages_list[key].id;
                    let message_text = response.messages_list[key].texto;
                    let message_imagem = "/static/"+response.messages_list[key].sender__imagem;
                    let message = $('#message_template').clone();
                    message.removeAttr('id')
                    message.addClass('message')
                    message.attr('id', 'message_' + message_id)
                    message.removeClass('hiddensection')
                    message.children('.messagetext').append(message_text)
                    message.children('.messageprofileimgcropper').children("img").attr("src",message_imagem)
                    $('#group_messages_body').append(message);
                }
            }
        });
    }

    setInterval(func, 1000);
});
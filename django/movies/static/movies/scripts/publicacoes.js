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

    $('form#post_form').submit(function(event) {
        let groups_cinemas = 0
        let film = 0
        $('.click.group').each(function () {
            let group_id_text = $(this).attr('id');
            let group_id = parseInt(group_id_text.replace('group_',''));
            let input_g = document.createElement('input');
            input_g.setAttribute('name', 'groups[]');
            input_g.setAttribute('value', group_id.toString());
            input_g.setAttribute('type', 'number');
            input_g.setAttribute('hidden', 'hidden');
            $('form').append(input_g);
            groups_cinemas++;
        });
        $('.click.cinema').each(function () {
            let cinema_id_text = $(this).attr('id');
            let cinema_id = parseInt(cinema_id_text.replace('cinema_',''));
            let input_c = document.createElement('input');
            input_c.setAttribute('name', 'cinemas[]');
            input_c.setAttribute('value', cinema_id.toString());
            input_c.setAttribute('type', 'number');
            input_c.setAttribute('hidden', 'hidden');
            $('form').append(input_c);
            groups_cinemas++
        });
        $('.click.film').each(function () {
            let film_id_text = $(this).attr('id');
            let film_id = parseInt(film_id_text.replace('film_',''));
            let input_f = document.createElement('input');
            input_f.setAttribute('name', 'film_id');
            input_f.setAttribute('value', film_id.toString());
            input_f.setAttribute('type', 'number');
            input_f.setAttribute('hidden', 'hidden');
            $('form').append(input_f);
            film++;
        });
        if (groups_cinemas === 0) {
            event.preventDefault();
            alert('Sem selecionar grupos ou cinemas a sua publicação não será visível')
        }
        else if (film === 0) {
            event.preventDefault();
            alert('Escolha um filme para a sua publicação')
        }
        let input_g = document.createElement('input');
        input_g.setAttribute('name', 'is_global');
        input_g.setAttribute('type', 'text');
        input_g.setAttribute('hidden', 'hidden');
        if (global) {
            input_g.setAttribute('value', 'true');
        } else {
            input_g.setAttribute('value', 'false');
        }
        $('form').append(input_g);
    });
});
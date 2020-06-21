$(document).ready(function() {
    $('.ui.dropdown').dropdown();

    $('.config.item').click(function() {
        var name = $(this).html();
        load_config(name);
    });

    $('#domains').click(function() { load_domains() });

    load_domains();

});

function load_domains() {
    $.when(fetch_html('api/domains')).then(function() {
        $('#domain').hide();
        $('#domain_cards').fadeIn();
    });
}

function add_domain() {
    var name = $('#add_domain').val();
    $('#add_domain').val('');

    $.ajax({
        type: 'POST',
        url: '/api/domain/' + name,
        statusCode: {
            201: function() { fetch_domain(name) }
        }
    });

}

function enable_domain(name, enable) {

    $.ajax({
        type: 'POST',
        url: '/api/domain/' + name + '/enable',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        data: JSON.stringify({
            enable: enable
        }),
        statusCode: {
            200: function() { fetch_domain(name); }
        }
    });

}

function update_domain(name) {
    var _file = $('#file-content').val();
    $('#dimmer').addClass('active');

    $.ajax({
        type: 'PUT',
        url: '/api/domain/' + name,
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        data: JSON.stringify({
            file: _file
        }),
        statusCode: {
            200: function() { setTimeout(function(){ fetch_domain(name) }, 400) }
        }
    });

}

function fetch_domain(name) {

    fetch('api/domain/' + name)
    .then(function(response) {
        response.text().then(function(text) {
            $('#domain').html(text).fadeIn();
            $('#domain_cards').hide();
        });
    })
    .catch(function(error) {
        console.error(error);
    });

}

function remove_domain(name) {

    $.ajax({
        type: 'DELETE',
        url: '/api/domain/' + name,
        statusCode: {
            200: function() {
                load_domains();
            },
            400: function() {
                alert('Deleting not possible');
            }
        }
    });

}

function fetch_html(url) {

    fetch(url)
    .then(function(response) {
        response.text().then(function(text) {
            $('#content').html(text);
        });
    })
    .catch(function(error) {
        console.error(error);
    });

}

function update_config(name) {
    var _file = $('#file-content').val();
    $('#dimmer').addClass('active');

    $.ajax({
        type: 'POST',
        url: '/api/config/' + name,
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        data: JSON.stringify({
            file: _file
        }),
        statusCode: {
            200: function() {

                setTimeout(function() {
                    $('#dimmer').removeClass('active');
                }, 450);

            }
        }
    });

}

function load_config(name) {

    fetch('api/config/' + name)
    .then(function(response) {
        response.text().then(function(text) {
            $('#content').html(text);
        });
    })
    .catch(function(error) {
        console.error(error);
    });

}

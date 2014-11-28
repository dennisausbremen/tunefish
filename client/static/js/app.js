(function ( $, window, document, undefined ) {
    'use strict';

    var form = $('form');

    form.on('submit', function(e){
        e.preventDefault();
        console.log('et le click, svp! ',$('[data-user]',this).val(),' ',$('[data-pass]',this).val());

        $.post(this.action, {login:$('[data-user]',this).val(),password:$('[data-pass]',this).val()}, function(data){
            console.log(data);
        });
    });


})( jQuery, window, document );
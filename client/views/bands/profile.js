$('#band_form').submit(function (e) {
    e.preventDefault();

    submit(this,
        function (result) { console.log("ok"); },
        function (errors) { console.log("errors", errors); }
    );

});
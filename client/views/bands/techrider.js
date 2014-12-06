$('#techrider_form').submit(function (e) {
    e.preventDefault();

    upload(this,
        function (result) {
            console.log("result", result);
            $("#techrider").html(result['techrider']);
        },
        function (errors) {
            console.log("errors", errors);
        }
    );

});
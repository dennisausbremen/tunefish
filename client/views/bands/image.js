$('#image_form').submit(function (e) {
    e.preventDefault();

    upload(this,
        function (result) {
            console.log("result", result);
            $("#image").html(result['image']);
        },
        function (errors) {
            console.log("errors", errors);
        }
    );

});
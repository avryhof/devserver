function add_to_playlist() {
    var pl_form = $(this);
    var playlist = pl_form.find("input[name=playlist]").val();
    var song = pl_form.find("input[name=song]").val();
    console.log(playlist);
    console.log(song);
    // $.ajax({
    //     type: "POST",
    //     url: pl_form.attr("action"),
    //     data: {"song": song, "playlist": playlist},
    //     success: success,
    //     dataType: dataType
    // });
}

$(document).ready(function () {
    $('.grid').masonry({
        // options
        itemSelector: '.grid-item',
        columnWidth: 200
    });
});
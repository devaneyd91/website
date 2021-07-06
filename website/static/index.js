function deleteNote(noteId) {
    fetch('delete-note', {
        method: "POST",
        body: JSON.stringify({ noteId: noteId})
    }).then((_res) => {
        window.location.href = "members_area";
    });
}

function deletePubnote(noteId) {
    fetch('delete-pubnote', {
        method: "POST",
        body: JSON.stringify({ noteId: noteId})
    }).then((_res) => {
        window.location.href = "public_notes";
    });
}

 function commentPubnote(noteId) {
     var comment = document.getElementById("pubcom"+noteId).value;
     fetch('comment-pubnote',{
         method: "POST",
         body: JSON.stringify({ noteId: noteId, comment: comment})
     }).then((_res) => {
        window.location.href = "public_notes";
    });
}

 $(document).ready(function(){
    // Check Radio-box
    $(".rating input:radio").attr("checked", false);

    $('.rating input').click(function () {
        $(".rating span").removeClass('checked');
        $(this).parent().addClass('checked');
    });

    $('input:radio').change(
      function(){
        var userRating = this.value;
        var noteId = $("input:radio").parent().attr('id');
        fetch('rate-pubnote',{
            method: "POST",
            body: JSON.stringify({ noteId: noteId, rating: userRating})
        }).then((_res) => {
            window.location.href = "public_notes";
            alert(noteId);
        });
    });
});

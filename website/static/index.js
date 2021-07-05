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
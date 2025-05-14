var editModal = document.getElementById('editModal');
editModal.addEventListener('show.bs.modal', function(event) {
    var button = event.relatedTarget;
    var id = button.getAttribute('data-id');
    var lname = button.getAttribute('data-lname');
    var fname = button.getAttribute('data-fname');
    var mname = button.getAttribute('data-mname');
    var course = button.getAttribute('data-course');
    var year = button.getAttribute('data-year');
    var addedBy = button.getAttribute('data-added_by');

    document.getElementById('id').value = id;
    document.getElementById('lname').value = lname;
    document.getElementById('fname').value = fname;
    document.getElementById('mname').value = mname;
    document.getElementById('course').value = course;
    document.getElementById('year').value = year;
    document.getElementById('addedBy').value = addedBy;
});

document.getElementById('saveChangesBtn').addEventListener('click', function() {
    var id = document.getElementById('id').value;
    var lname = document.getElementById('lname').value;
    var fname = document.getElementById('fname').value;
    var mname = document.getElementById('mname').value;
    var course = document.getElementById('course').value;
    var year = document.getElementById('year').value;
    var addedBy = document.getElementById('addedBy').value;

    var data = {
        id: id,
        lname: lname,
        fname: fname,
        mname: mname,
        course: course,
        year: year,
        added_by: addedBy,
    };

    fetch('/update_student', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Student updated successfully!');
            window.location.reload();
        } else {
            alert('Error updating student.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

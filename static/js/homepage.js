// When modal is about to show
var editModal = document.getElementById('editModal');
editModal.addEventListener('show.bs.modal', function (event) {
    var button = event.relatedTarget;

    var id = button.getAttribute('data-id');
    var lname = button.getAttribute('data-lname');
    var fname = button.getAttribute('data-fname');
    var mname = button.getAttribute('data-mname');
    var course = button.getAttribute('data-course');
    var year = button.getAttribute('data-year');
    var addedby = button.getAttribute('data-addedby');

    document.getElementById('id').value = id;
    document.getElementById('lname').value = lname;
    document.getElementById('fname').value = fname;
    document.getElementById('mname').value = mname;
    document.getElementById('course').value = course;
    document.getElementById('year').value = year;
    document.getElementById('addedby').value = addedby;
});

// When clicking save button
document.getElementById('saveChangesBtn').addEventListener('click', function () {
    var id = document.getElementById('id').value;
    var lname = document.getElementById('lname').value;
    var fname = document.getElementById('fname').value;
    var mname = document.getElementById('mname').value;
    var course = document.getElementById('course').value;
    var year = document.getElementById('year').value;
    var addedby = document.getElementById('addedby').value;

    var data = {
        id: id,
        lname: lname,
        fname: fname,
        mname: mname,
        course: course,
        year: year,
        addedby: addedby
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

  // Search functionality
  document.getElementById('searchInput').addEventListener('keyup', function () {
    var searchValue = this.value.toLowerCase();
    var rows = document.querySelectorAll('#studentList tr');

    rows.forEach(function (row) {
      var rowText = row.innerText.toLowerCase();
      row.style.display = rowText.includes(searchValue) ? '' : 'none';
    });
  });

  // Populate modal
  var editModal = document.getElementById('editModal');
  editModal.addEventListener('show.bs.modal', function (event) {
    var button = event.relatedTarget;
    document.getElementById('id').value = button.getAttribute('data-id');
    document.getElementById('lname').value = button.getAttribute('data-lname');
    document.getElementById('fname').value = button.getAttribute('data-fname');
    document.getElementById('mname').value = button.getAttribute('data-mname');
    document.getElementById('course').value = button.getAttribute('data-course');
    document.getElementById('year').value = button.getAttribute('data-year');
  });

  // Handle form submission
  document.getElementById('editStudentForm').addEventListener('submit', function (e) {
    e.preventDefault();
    var formData = new FormData(this);

    fetch('/update_student', {
      method: 'POST',
      body: formData,
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


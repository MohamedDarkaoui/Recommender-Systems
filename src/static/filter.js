function filter() {
    var input = document.getElementById("input")
    var table = document.getElementById("table_user");
    if (input.value.size == 0) {
      for (var i = 1, row; row = table.rows[i]; i++) {
        row.style.display = "";
      }
    }
    else {
      for (var i = 1, row; row = table.rows[i]; i++) {
        var size = input.value.length;
        console.log(row.cells[1].innerText.substring(0, size));
        if (input.value != row.cells[1].innerText.substring(0, size)) {
          row.style.display = "none";
        }
        else{
          row.style.display = "";
        }
      }
    }
  }
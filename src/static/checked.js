function readonly(){
    if (!document.getElementById("isRandomItems").checked) {
        document.getElementById("isRandomItems_readonly").setAttribute("readonly", true)
    }
}

function checker() {
    if (document.getElementById("isRandomItems").checked) {
        readonly()
        document.getElementById("isRandomItems_readonly").removeAttribute("readonly");
    }
    if (document.getElementById("isRandomClient").checked) {
        readonly()
    }
    if (document.getElementById("isEmptyClient").checked) {
        readonly()
    }
    if (document.getElementById("isAllClients").checked) {
        readonly()
    }
    if (document.getElementById("isCopyFromExperiment").checked) {
        readonly()
    }
    if (document.getElementById("isCopyFromList").checked) {
        readonly()
    }
 }

 function checker2(){
    if (document.getElementById("checkbox").checked){
        document.getElementById("upload_files").style.display = "block";
        document.getElementById("add").style.display = "block";
        document.getElementById("delete_but").style.display = "block";
    }
    else{
        document.getElementById("upload_files").style.display = "none";
        document.getElementById("add").style.display = "none";
        document.getElementById("delete_but").style.display = "none";
    }
 }

//  var counter = 0
// function add_upload(){
//     counter = counter + 1
//     var tmp = document.getElementById("csvmetadata")
//     var tabel = document.getElementById("filetabel")
//     if(tmp.value.length > 0){
//         var rij = document.createElement("tr")
//         rij.innerHTML = "<th>" + counter + "</th>" + "<th>" + tmp.value.split("\\").pop() + "</th>"
//         tabel.appendChild(rij)
//     }
    
// }

// function delete_upload(){
//     var tabel = document.getElementById("filetabel")
//     if(tabel.rows.length > 0){
//         counter = counter - 1  
//         tabel.deleteRow(-1)
//     }  
// }
var counter = -1;
function add_upload(){
    counter = counter + 1;
    var itm = document.getElementById("meta-data_upload");
    var html = document.createElement("div");
    html.className = "custom-file mb-3";
    html.id = "meta-data_upload"  + counter;
    html.innerHTML = '<input multiple type="file" class="custom-file-input" id="csvmetadata' + counter + '" name="csvmetadata"><label class="custom-file-label" for="csvmetadata' + counter + '">Choose file</label>';
    document.getElementById("upload_files").appendChild(html);
    $(".custom-file-input").on("change", function () {
        var fileName = $(this).val().split("\\").pop();
        $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
    });
}

function delete_upload(){
    var list = document.getElementById("upload_files")
    if(list.childNodes.length > 3){
        list.removeChild(list.lastChild)
    }
}
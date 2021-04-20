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
var counter = 0
var id = "copy_id"
function add_upload(){
    counter = counter + 1
    var itm = document.getElementById("meta-data_upload");
    var itm2 = document.getElementById("copy_id0")
    var cln = itm.cloneNode(true);
    var cln2 = itm2.cloneNode(true)
    cln.id = id + counter
    document.getElementById("upload_files").appendChild(cln);
    alert(counter)
}

function delete_upload(){
    var list = document.getElementById("upload_files")
    if(list.childNodes.length > 3){
        var itm = document.getElementById("meta-data_upload")
        itm.remove()
    }
    
    
}
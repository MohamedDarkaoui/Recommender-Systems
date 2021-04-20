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

function add_upload(){
    var itm = document.getElementById("meta-data_upload");
    var cln = itm.cloneNode(true);
    document.getElementById("upload_files").appendChild(cln);
}

function delete_upload(){
    var list = document.getElementById("upload_files")
    if(list.childNodes.length > 3){
        var itm = document.getElementById("meta-data_upload")
        itm.remove()
    }
    
    
}
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
var counter = 0;
function add_upload(){
    counter = counter + 1;
    //find
    var itm = document.getElementById("meta-data_upload");
    var csv = document.getElementById("csvmetadata");
    var lab = document.getElementById("label10");

    // clone
    var clnItm = itm.cloneNode(true);
    var clnCsv = csv.cloneNode(true);
    var clnLab = lab.cloneNode(true);

    // change id value
    clnCsv.id = "csvmetadata" + counter;
    clnLab.id = "label10" + counter;
    clnItm.id = "meta-data_upload" + counter;
    clnLab.for =  clnCsv.id

    // append
    document.getElementById("upload_files").appendChild(clnItm);
    document.getElementById("csvmetadata").id =  "csvmetadata0"
    document.getElementById("label10").id = "label100"
    document.getElementById(clnItm.id).removeChild(document.getElementById("csvmetadata"));
    document.getElementById(clnItm.id).removeChild(document.getElementById("label10"));

    alert(clnCsv.id)
    document.getElementById(clnItm.id).appendChild(clnCsv);
    document.getElementById(clnItm.id).appendChild(clnLab);

    document.getElementById("csvmetadata0").id =  "csvmetadata"
    document.getElementById("label100").id = "label10"

}

function delete_upload(){
    var list = document.getElementById("upload_files")
    if(list.childNodes.length > 3){
        var itm = document.getElementById("meta-data_upload")
        itm.remove()
        alert("lololo")
    }
    
    
}
function readonly(){
    if (!document.getElementById("amount").checked) {
        document.getElementById("amount_readonly").setAttribute("readonly", true)
    }
    if (!document.getElementById("item").checked) {
        document.getElementById("item_readonly").setAttribute("readonly", true)
    }
}

function checker() {
    if (document.getElementById("amount").checked) {
        readonly()
        document.getElementById("amount_readonly").removeAttribute("readonly");
    }
    if (document.getElementById("item").checked) {
        readonly()
        document.getElementById("item_readonly").removeAttribute("readonly");
    }
    if (document.getElementById("empty").checked) {
        readonly()
    }
    if (document.getElementById("random").checked) {
        readonly()
    }
 }
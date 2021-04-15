function closeall() {
    document.getElementById("ease").style.display = "none";
    document.getElementById("pop").style.display = "none";
    document.getElementById("wmf").style.display = "none";
    document.getElementById("iknn").style.display = "none";

}
function getform() {
    var a = document.getElementById("selected").value;
    if (a == "ease") {
        closeall();
        document.getElementById("ease").style.display = "block";
    };
    if (a == "default") {
        closeall();
    };
    if (a == "pop"){
        closeall();
        document.getElementById("pop").style.display = "block";
    };
    if (a == "wmf"){
        closeall();
        document.getElementById("wmf").style.display = "block";
    };
    if (a == "iknn"){
        closeall()
        document.getElementById("iknn").style.display = "block";
    }
    

};
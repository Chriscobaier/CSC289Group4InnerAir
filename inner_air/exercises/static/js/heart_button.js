//Test
var btn = document.getElementById('btnh1');

function Toggle1(){
        if (btn.style.color =="red") {
            console.log("Unfavorited");
            btn.style.color = "grey"
        }
        else{
            console.log("Favorited");
            btn.style.color = "red"
        }
}

$(document).ready(function() {
    var backgroundFade = document.getElementById("backgroundFade");
    var backgroundImg = document.getElementById("bgImage");
    
    var alpha = 1;
    var interval = -0.01;
    var currImg = 1;
    var newImg = new Image();
    newImg.src = bgFolder + "bg0.jpg";
    document.getElementById("bgImage").style.backgroundImage = "url('" + newImg.src + "')";
    console.log(newImg.src);
    var loaded = false;
    var waiting = false;
    
    var countTime = 0;
    
    var id = setInterval(frames, 10);
    function frames() {
        if (waiting == true) {
            countTime++;
            if (countTime == 500) {
                waiting = false;
                countTime = 0;
            }
        }
        else {
            alpha += interval;
            backgroundFade.style.backgroundColor = "RGBA(128,128,128," + alpha + ")";
            if(alpha <= 0.2 && interval < 0) {
                interval = 0.01;
                console.log("asdasd");
                currImg++;
                if (currImg == 6) {
                    currImg = 0;
                }
                newImg.src = bgFolder + "bg" + currImg + ".jpg";
                waiting = true;
            }
            else if (alpha >= 1.0 && interval > 0) {
                document.getElementById("bgImage").style.backgroundImage = "url('" + newImg.src + "')";
                interval = -0.01;
            }
        }
    }
})
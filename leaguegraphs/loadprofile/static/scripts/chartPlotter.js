var profileUrl = window.location.href;
var urlArray = profileUrl.split("profile");
var dataUrl = urlArray[0] + "profileData" + urlArray[1];
var chart, points, polyline, dataSet, option;
var textArray = [4];
for(i=0; i<4; i++){
    textArray[i] = document.createElementNS("http://www.w3.org/2000/svg", 'text');
    textArray[i].setAttribute("x", 60);
    textArray[i].setAttribute("y", (i+1)*100 + 5);
    textArray[i].setAttribute("text-anchor", "end");
}
var options = ["cs_average10", "gpm_average10", "xpm_average10"];

$(document).ready(function() {
    points = document.getElementsByTagName("circle");
    polyline = document.getElementById("chartLine");
    chart = document.getElementById("svgChart");
    for(i=0; i<4; i++){
        chart.appendChild(textArray[i]);
    }
    $.getJSON( dataUrl, function(data) {
        dataSet = data;
        console.log(dataSet);
        setWinCircles();
        setDateAxis();
        updateChart();
    })
})

function setWinCircles() {
    for(game = 0; game < 5; game++) {
        if (dataSet[game]['win_loss'] == true) {
            points[4 - game].style.fill = "green";
        }
    }
}

function setDateAxis() {
    for(game = 0; game<5; game++){
        var dateText = document.createElementNS("http://www.w3.org/2000/svg", 'text');
        var g = document.createElementNS("http://www.w3.org/2000/svg", 'g');
        var date = document.createElementNS("http://www.w3.org/2000/svg", 'tspan');
        var time = document.createElementNS("http://www.w3.org/2000/svg", 'tspan');
        var epochsTime = dataSet[4-game]['game_date'];
        var datetime = new Date(epochsTime);
        var datetext = datetime.getDate() + "/" + (datetime.getMonth()+1) + "/" + datetime.getFullYear();
        var timetext = datetime.toTimeString().substring(0,5);
        g.setAttribute("transform","translate("+(65 + 150 * game)+" "+435+")");
        date.setAttribute("x","0");
        date.setAttribute("dy","1.2em");
        time.setAttribute("x","15");
        time.setAttribute("dy","1.2em");
        date.textContent=datetext;
        time.textContent=timetext;
        dateText.appendChild(date);
        dateText.appendChild(time);
        g.appendChild(dateText);
        chart.appendChild(g);
    }
}

function updateChart() {
    var select = document.getElementById("chartSelect");
    
    if (select.value == 'cs') option = options[0];
    else if (select.value == 'gold') option = options[1];
    else option = options[2];
    
    var highest = dataSet[0][option];
    var lowest = dataSet[0][option];    
    for(game = 1; game <5; game++) {
        if (dataSet[game][option] > highest) highest = dataSet[game][option];
        if (dataSet[game][option] < lowest) lowest = dataSet[game][option];
    }
    
    textArray[0].textContent = highest.toFixed(1);
    textArray[3].textContent = lowest.toFixed(1);
    textArray[1].textContent = (highest-(highest-lowest)/3).toFixed(1);
    textArray[2].textContent = (lowest+(highest-lowest)/3).toFixed(1);
    var polyPointsy = [5];
    var currPolyPointsy = [5];
    for(game = 0; game < 5; game++) {
        polyPointsy[4-game] = scaleMap(dataSet[game][option], highest, lowest);
        currPolyPointsy[game] = parseInt(points[game].getAttribute("cy"));
        animatePoint(points[4 - game], scaleMap(dataSet[game][option], highest, lowest));
    }
    animateLines(polyPointsy,currPolyPointsy);
}

function scaleMap(data, highest, lowest) {
    var difference = highest - lowest;
    
    var scale = (data - lowest) / difference;
    return parseInt(400 - (scale * 300));
}

function circleHover(circle) {
    var hoverText = document.getElementById("hoverText");
    var x = "" + (parseInt(circle.getAttribute("cx")) - 25);
    var y = "" + (parseInt(circle.getAttribute("cy")) - 25);
    hoverText.setAttribute("x", x);
    hoverText.setAttribute("y", y);
    
    var datasetIndex = (parseInt(circle.getAttribute("cx")) - 100) / 150;
    hoverText.textContent = dataSet[4 - datasetIndex][option].toFixed(1);
    
    var r = 6;
    var id = setInterval(frame, 10);
    function frame() {
        if (r == 20) {
            clearInterval(id);
        } else {
            r++;
            circle.setAttribute("r", r);
        }
    }
    //circle.setAttribute("r", 20);
}

function circleUnhover(circle) {
    var hoverText = document.getElementById("hoverText");
    hoverText.textContent = "";
    
    var r = 20;
    var id = setInterval(frame, 10);
    function frame() {
        if (r == 6) {
            clearInterval(id);
        } else {
            r--;
            circle.setAttribute("r", r);
        }
    }
}

function animatePoint(circle, newY) {
    var currY = parseInt(circle.getAttribute("cy"));
    var interval = 1;
    if (newY < currY) interval = -1;
    var id = setInterval(frame, 3);
    function frame() {
        if (currY == newY) {
            clearInterval(id);
        } else {
            currY += interval;
            circle.setAttribute("cy", currY);
        }
    }
}

function animateLines(polyPointsy, currPolyPointsy){
    var interval = 1;
    var intervals = [5];
    var currYs = currPolyPointsy;
    for(i=0; i<5; i++){
        if(currYs[i] > polyPointsy[i]) intervals[i] = -interval;
        else intervals[i] = interval;
    }
    var id = setInterval(frames, 2);
    function frames() {
        var cnt = 0;
        var polyPoints = "";
        for(i=0; i<5; i++){
            if( currYs[i] != polyPointsy[i] ){
                currYs[i] += intervals[i];
            } 
            else cnt++;
            polyPoints+= (100 + 150 * i)+","+currYs[i]+" ";
        }
        if(cnt==5) clearInterval(id);
        else{
            polyline.setAttribute('points', polyPoints);
        }
    }
}
            
/*function getMatch(circle){
    var datasetIndex = (parseInt(circle.getAttribute("cx")) - 100) / 150;
    var matchId = dataSet[4 - datasetIndex]['match_id'];
 */   
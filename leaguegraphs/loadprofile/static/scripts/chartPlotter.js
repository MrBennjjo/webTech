var profileUrl = window.location.href;
var urlArray = profileUrl.split("profile");
var dataUrl = urlArray[0] + "profileData" + urlArray[1];
var chart, points, polyline, dataSet, option;
var textArray = [4];
var spells = {1 : "SummonerBoost", 3 : "SummonerExhaust", 4 : "SummonerFlash", 6 : "SummonerHaste", 7 : "SummonerHeal", 11 : "SummonerSmite", 12 : "SummonerTeleport", 14 : "SummonerDot", 21 : "SummonerBarrier"}; 
var selectedCircle;

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
    initialradio = document.getElementById("graphCS");
    for(i=0; i<4; i++){
        chart.appendChild(textArray[i]);
    }
    $.getJSON( dataUrl, function(data) {
        dataSet = data;
        setWinCircles();
        setDateAxis();
        updateChart(initialradio);
        getMatch(points[4]);
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

function updateChart(radiobutton) {
    
    if (radiobutton.value == 'cs') option = options[0];
    else if (radiobutton.value == 'gold') option = options[1];
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
    if (circle == selectedCircle) r = 15;
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
    var minR = 6;
    if (circle == selectedCircle) minR = 15;
    
    var r = 20;
    var id = setInterval(frame, 10);
    function frame() {
        if (r == minR) {
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
            
function getMatch(circle) {
    if (selectedCircle != null) {
        selectedCircle.setAttribute("r", "6");
        selectedCircle.setAttribute("stroke-width", "0");
    }
    selectedCircle = circle;
    selectedCircle.setAttribute("r", "15");
    circle.setAttribute("stroke", "#000000");
    circle.setAttribute("stroke-width", "3");
    
    var index = 4 - ((parseInt(circle.getAttribute("cx")) - 100) / 150);
    var champ = document.getElementById("champImg");
    var spell1Img = document.getElementById("spell1Img");
    var spell2Img = document.getElementById("spell2Img");
    var spell1 = spells[dataSet[index]['spell1']];
    var spell2 = spells[dataSet[index]['spell2']];
    var items = dataSet[index]['items'].split(",");
    
    //console.log()
    var champKey = dataSet[6][dataSet[index]['champion']]['key'];
    champ.setAttribute("src", "http://ddragon.leagueoflegends.com/cdn/" + dataSet[5] + "/img/champion/" + champKey + ".png");
    spell1Img.setAttribute("src", "http://ddragon.leagueoflegends.com/cdn/" + dataSet[5] + "/img/spell/" + spell1 +".png");
    spell2Img.setAttribute("src", "http://ddragon.leagueoflegends.com/cdn/" + dataSet[5] + "/img/spell/" + spell2 +".png");
    document.getElementById("role").textContent = "Role: " + dataSet[index]['role'];
    document.getElementById("kda").textContent = "KDA: " + dataSet[index]['kills'] + "/" + dataSet[index]['deaths'] + "/"+ dataSet[index]['assists'];
    var deaths = dataSet[index]['deaths'];
    if (deaths == 0) deaths = 1;
    document.getElementById("kdaRatio").textContent = "KDA ratio: " + ((dataSet[index]['kills'] + dataSet[index]['assists']) / deaths).toFixed(1);
    document.getElementById("lvl").textContent = "lvl " + dataSet[index]['lvl'];
    document.getElementById("endCS").textContent = dataSet[index]['endCS'] + "CS";
    document.getElementById("endGold").textContent = numFormat(dataSet[index]['endGold']) + "g";
    
    for (i = 0; i < 7; i++) {
        if (items[i] != 0) {
            document.getElementById("item" + i).setAttribute("src", "http://ddragon.leagueoflegends.com/cdn/" + dataSet[5] + "/img/item/" + items[i] +".png");
        }
        else document.getElementById("item" + i).setAttribute("src", noItemImg);
    }
    
    var alpha = 0.2;
    var interval = 0.01;
    var backgroundFade = document.getElementById("backgroundFade");
    var id = setInterval(frames, 5);
    var loaded = false;
    var newImg = new Image();
    newImg.onload = function() { loaded = true; }
    newImg.src = "http://ddragon.leagueoflegends.com/cdn/img/champion//splash/" + champKey + "_0.jpg";
    function frames() {
        alpha += interval;
        backgroundFade.style.backgroundColor = "RGBA(128,128,128," + alpha + ")";
        if(alpha <= 0.2) clearInterval(id);
        else if (alpha >= 1.0){
            interval = 0;
            
            if (loaded == true) {
                document.getElementById("profileBackground").style.backgroundImage = "url('" + newImg.src + "')";
                interval = -0.005;
            }
        }
    }
}

function numFormat(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
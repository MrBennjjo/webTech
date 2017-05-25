var profileUrl = window.location.href;
var urlArray = profileUrl.split("profile");
var dataUrl = urlArray[0] + "profileData" + urlArray[1];
var chart;

var points;
var polyline;
var dataSet;
var option;
var options = ["cs_average10", "gpm_average10", "xpm_average10"];

$(document).ready(function() {
    points = document.getElementsByTagName("circle");
    polyline = document.getElementById("chartLine");
    chart = document.getElementById("svgChart");
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
        var datetime = dataSet[4-game]['game_date'].split('\n');
        g.setAttribute("transform","translate("+(65 + 150 * game)+" "+430+")");
        date.setAttribute("x","0");
        date.setAttribute("dy","1.2em");
        time.setAttribute("x","15");
        time.setAttribute("dy","1.2em");
        date.textContent=datetime[0];
        time.textContent=datetime[1];
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
    
    
    var polyPoints = "";
    for(game = 0; game < 5; game++) {
        
        polyPoints += "" + (100 + 150 * game) + "," + scaleMap(dataSet[4 - game][option], highest, lowest) + " ";
        points[4 - game].setAttribute("cy", scaleMap(dataSet[game][option], highest, lowest));
    }
    polyline.setAttribute("points", polyPoints);
}

function scaleMap(data, highest, lowest) {
    var difference = highest - lowest;
    
    var scale = (data - lowest) / difference;
    return 400 - (scale * 300);
}

function circleHover(circle) {
    var hoverText = document.getElementById("hoverText");
    var x = "" + (parseInt(circle.getAttribute("cx")) - 25);
    var y = "" + (parseInt(circle.getAttribute("cy")) - 25);
    hoverText.setAttribute("x", x);
    hoverText.setAttribute("y", y);
    
    var datasetIndex = (parseInt(circle.getAttribute("cx")) - 100) / 150;
    hoverText.textContent = dataSet[4 - datasetIndex][option].toFixed(1);
    circle.setAttribute("r", 20);
}

function circleUnhover(circle) {
    var hoverText = document.getElementById("hoverText");
    hoverText.textContent = "";
    circle.setAttribute("r", 6);
}
var started = 0;
var startTime = 0;
var ended = 0;
var timePassed = 0;
var demoText = document.getElementById("demotext").innerHTML;
var finalText = Array(0);
var numWords = 0;
var wpm = 0;
var numRight = 0;
var accuracy = 0;
var line = 0;
var maxNum = 80;
var startline = 0;
//var content = "";

function init() {
  //console.log(demoText);
  for (var i=0; i<demoText.length; i++){
    if (demoText[i] == " "){
      numWords++;
    }
  }
  console.log("Numwords: "+numWords);

  var lastCut = 0;
  for (var i=0; i<demoText.length; i++){
    if (i==80*(line+1)){
      finalText.push(demoText.substring(lastCut, i));
      lastCut = i;
      line++;
    }
  }
  line = 0;
  if (finalText.length<3){
    document.getElementById("canvi").innerHTML += '<canvas id="myCanvas" width="1200" height="' + 30 * finalText.length + '"></canvas>';
  }
  else{
    document.getElementById("canvi").innerHTML += '<canvas id="myCanvas" width="1200" height="' + 90 + '"></canvas>';
  }
  for(var i=0; i<finalText.length && i<3; i++){
    console.log(finalText[i]);
    var ctx = document.getElementById("myCanvas").getContext("2d");
    ctx.font = "20px Courier New";
    ctx.fillStyle = "gray";
    ctx.fillText(finalText[i],5,24*(i+1));
  }

  /*var ctx = document.getElementById("myCanvas").getContext("2d");
  ctx.font = "20px Courier New";
  ctx.fillStyle = "gray";
  ctx.fillText(demoText + "WWwwiiiII",1,24);*/
}



function myFunction() {
  var x = document.getElementById("myInput").value;
  //console.log("x.length: " + x.length);
  //console.log("started: " + started);
  if (x.length == 0){
    started = 0;
  }
  if (!started && x.length == 1){
    ended = 0;
    wpm = 0;
    numRight = 0;
    accuracy = 0;
    startTime = new Date().getTime() / 1000;
    console.log(startTime);
    started = 1;
  }
  x = x.substring(0,demoText.length);
  startline = -Math.floor(x.length/80);
  console.log("x.length: " + x.length);
  console.log("Startline: " + startline);

  /*var result = "";
  for(var i=0; i<x.length; i++){
    //console.log("i: " + i);
    if (x[i] == demoText[i]){
      result += x[i].fontcolor("green");
      //console.log(result);
    }
    else{
      result += x[i].fontcolor("red");
      //console.log(result);
    }
  }
  document.getElementById("demo").innerHTML = "You wrote:<br>" + result;*/

  //content = x + demoText.substring(x.length,demoText.length);

  var ctx = document.getElementById("myCanvas").getContext("2d");
  ctx.font = "20px Courier New";
  ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
  var width = 5;
  line = 0;
  for (var i=0; i<x.length; i++){
    if(i==80*(line+1)){
      line++;
      width=5;
    }
    if (x[i] == demoText[i]){
      ctx.fillStyle = "green";
      ctx.fillText(x[i],width,24*(startline+line+1));
    }
    else{
      ctx.fillStyle = "red";
      if (x[i]==" "){
        ctx.fillText("_",width,24*(startline+line+1));
      }
      else{
        ctx.fillText(x[i],width,24*(startline+line+1));
      }
    }
    width+=12;
  }
  ctx.fillStyle = "gray";
  console.log("Line: " + line);
  var start = x.length-80*(line)-1;
  if (line==0){
    start++;
  }
  for (var i=0; i<finalText.length; i++){
    //console.log("Startline + i: " + startline + i);
    if (startline + i != 0){
      ctx.fillText(finalText[i],5,24*(startline+i+1));
      //console.log("s");
    }
  }
  ctx.fillText(finalText[line].substring(start,demoText.length),width,24*(startline+line+1));

  if (x.length==demoText.length && !ended){
    timePassed = Math.floor((new Date().getTime() / 1000 - startTime) * 100) / 100;
    console.log(timePassed);
    console.log(numWords);
    wpm = Math.floor(numWords / (timePassed / 60));
    console.log("wpm: " + wpm);
    for (var i=0; i<demoText.length; i++){
      if (x[i] == demoText[i]){
        numRight++;
      }
    }
    accuracy = Math.floor((numRight / demoText.length) * 100);
    ended = 1;
  }
  document.getElementById("time").innerHTML = "Time: " + timePassed + " s";
  document.getElementById("wpm").innerHTML = "Wpm: " + wpm;
  document.getElementById("accuracy").innerHTML = "Accuracy: " + accuracy + "%";
}

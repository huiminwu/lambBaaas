var List = require("collections/list");
var started = 0;
var startTime = 0;
var ended = 0;
var timePassed = 0;
var demoText = document.getElementById("demotext").innerHTML;
var demoTextSplit = new List();
var finalText;
var numWords = 0;
var wpm = 0;
var numRight = 0;
var accuracy = 0;
//var content = "";

function init() {
  console.log(demoText);
  for (var i=0; i<demoText.length; i++){
    if (demoText[i] == " "){
      numWords++;
    }
  }
  console.log("Numwords: "+numWords);

  var lastCut = 0;
  for (var i=0; i<demoText.length; i++){
    if (demoText[i] == "\n"){
      demoTextSplit.add(demoText.substring(lastCut, i));
      lastCut = i+1;
    }
  }
  finalText = demoTextSplit.toArray();
  for(var i=0; i<finalText.length; i++){
    console.log(finalText[i]);
  }

  var ctx = document.getElementById("myCanvas").getContext("2d");
  ctx.font = "20px Courier New";
  ctx.fillStyle = "gray";
  ctx.fillText(demoText + "WWwwiiiII",1,24);
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
  ctx.clearRect(0, 0, 1000, 30);
  var width = 1;
  for (var i=0; i<x.length; i++){
    if (x[i] == demoText[i]){
      ctx.fillStyle = "green";
      ctx.fillText(x[i],width,24);
    }
    else{
      ctx.fillStyle = "red";
      if (x[i]==" "){
        ctx.fillText("_",width,24);
      }
      else{
        ctx.fillText(x[i],width,24);
      }
    }
    width+=12;
  }
  ctx.fillStyle = "gray";
  ctx.fillText(demoText.substring(x.length,demoText.length),width,24);

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

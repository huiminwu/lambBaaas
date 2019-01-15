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
var startline = 0;
var dif = '';
//var content = "";

function selectDif(difficulty){
  dif = difficulty;
  document.getElementById("selectDifficulty").innerHTML = '<div style="display: none;">' + document.getElementById("selectDifficulty").innerHTML + '</div>';
  init(difficulty);
}

function init(difficulty) {
  //console.log(demoText);
  //demoText = demoText.substring(0, demoText.length-1);
  if (difficulty == 'Easy'){
    demoText = demoText.toLowerCase();
    demoText = demoText.replace(/[^a-z ]/g, '');
  }
  console.log(demoText);
  if (difficulty == 'Easy' || difficulty == 'Medium'){
    demoText = demoText.replace(/[^a-zA-Z0-9 ]/g, '');
  }
  for (var i=0; i<demoText.length; i++){
    if (demoText[i] == " "){
      numWords++;
    }
  }
  console.log(demoText);
  console.log("Numwords: "+numWords);
  console.log("Text length: "+demoText.length);

  var lastCut = 0;
  for (var i=0; i<demoText.length; i++){
    if (demoText[i] == "\n"){
      demoText[i] = " ";
    }
    if (i==80*line){
      finalText.push(demoText.substring(lastCut, i+80));
      console.log("FinalText["+line+"]: "+finalText[line]);
      lastCut = i+80;
      line++;
    }
  }
  line = 0;
  for(var i=0; i<finalText.length; i++){
    console.log(finalText[i]);
    var ctx = document.getElementById("myCanvas").getContext("2d");
    ctx.font = "20px Courier New";
    ctx.fillStyle = "gray";
    ctx.fillText(finalText[i],5,24*(i+1)-5);
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
  startline = -Math.floor((x.length-1)/80);
  if(x.length==0){
    startline=0;
  }
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
    if (x[i] == demoText[i]){
      ctx.fillStyle = "green";
      ctx.fillText(x[i],width,24*(startline+line+1)-5);
    }
    else{
      ctx.fillStyle = "red";
      if (x[i]==" "){
        ctx.fillText("_",width,24*(startline+line+1)-5);
      }
      else{
        ctx.fillText(x[i],width,24*(startline+line+1)-5);
      }
    }
    width+=12;
    if(i==80*(line+1)-1){
      line++;
      width=5;
    }
  }
  ctx.fillStyle = "gray";
  console.log("Line: " + line);
  var start = x.length-80*(line);
  /*if (line==0){
    start++;
  }*/
  for (var i=0; i<finalText.length; i++){
    //console.log("Startline + i: " + startline + i);
    if (startline + i != 0){
      ctx.fillText(finalText[i],5,24*(startline+i+1)-5);
      //console.log("s");
    }
  }
  ctx.fillText(finalText[line].substring(start,finalText[line].length),width,24*(startline+line+1)-5);



  if (x.length==demoText.length && !ended){
    //console.log("x.length: " + x.length);
    //console.log("demoText.length: " + demoText.length);
    var endTime = new Date().getTime();
    var date = new Date(endTime);
    timePassed = Math.floor((endTime / 1000 - startTime) * 100) / 100;
    //console.log(timePassed);
    //console.log(numWords);
    wpm = Math.floor(numWords / (timePassed / 60));
    //console.log("wpm: " + wpm);
    for (var i=0; i<demoText.length; i++){
      if (x[i] == demoText[i]){
        numRight++;
      }
    }
    accuracy = Math.floor((numRight / demoText.length) * 100);
    ended = 1;
    //document.getElementById("finishbox").innerHTML = '<div id="exampleoverlay">'+ document.getElementById("finishbox").innerHTML.substring(0,34) + document.getElementById("finishbox").innerHTML.substring(49,document.getElementById("finishbox").innerHTML.length) + '</div>';
    //console.log("Time to log results.");
    document.getElementById("dif").value = dif;
    document.getElementById("time").value = endTime;
    document.getElementById("wpm").value = wpm;
    document.getElementById("accuracy").value = accuracy;
    document.forms["resultsForm"].submit();
  }
}

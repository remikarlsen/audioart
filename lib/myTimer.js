var active = false;

function startTimer(){
  if(active){
    var timer = document.getElementById("myTimer").innerHTML;
    var arr = timer.split(":");
    var min = arr[0];
    var sec = arr[1];

    if(sec==59){
      if(min==59){
        min=0;
      }
      else{
        min++;
      }
      if(min<10){
        min="0"+min;
      }
      sec="00";
    }
    else{
      sec++;
      if(sec<10){
        sec="0"+sec;
      }
    }
    document.getElementById("myTimer").innerHTML = min + ":" + sec;
    setTimeout(startTimer, 1000);//1 sec
  }
}

function activateTimer(){
  active=true;
  startTimer();
}

function stopTimer(){
  active=false;
}

function changeState(){
  if(active===false){
    active=true;
    startTimer();
    console.log("Timer started...");
    document.getElementById("control").innerHTML="PAUSE";
  }
  else{
    active=false;
    console.log("Timer paused...");
    document.getElementById("control").innerHTML="START";
  }
}

function reset(){
  document.getElementById("myTimer").innerHTML = "00:00";
  console.log("Timer reset...");
}

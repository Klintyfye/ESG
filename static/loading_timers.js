//Displays four timers during the loading screen.
//Timers are displayed one after another, when one process begins and ends.
//The timers should end when the process is finished.
//This program knows when respective tasks are done by reading from the stage.txt file.

//It is currently hard-coded to instead end after X seconds.

var task1timer = 0; 
var task2timer = 0;
var task3timer = 0;
var task4timer = 0;
var stage = 1; //What task we're currently on is stored here. 
const start = new Date().getTime();
var x = setInterval(function(task){
    var now = new Date().getTime();
    var distance = Math.floor((now-start)/1000);
    distance = distance - task1timer - task2timer - task3timer - task4timer;
    var vt = 0

    // const fs = require('fs')
    // fs.readFile('stage.txt', (err, data) => {
    //     if (err) throw err;
    //     console.log(data.toString());
    //     if (data.toString() == "1"){
    //         console.log("VT done")
    //         vt = 1;
    //     }
    // })

    document.getElementById("stage").innerHTML = stage;
    if (stage == 1){ //VT is working...
        document.getElementById("timer1").innerHTML = distance;
    }
    if (stage == 1 && distance > 4){ //TODO: Replace this with VT completion.
        stage = 2;
        if (task1timer == 0){
            task1timer = distance;
        }
        document.getElementById("timer1").innerHTML = "Done in " + task1timer.toString();

    }
    if (stage == 2){ //RetireJS is working...
        document.getElementById("timer2").innerHTML = distance;
    }
    if (stage == 2 && distance > 5){ //TODO: Replace this with RetireJS completion.
        stage = 3;
        if (task2timer == 0){
            task2timer = distance;
        }
        document.getElementById("timer2").innerHTML = "Done in " + task2timer.toString();
    }
    if (stage == 3){ //Data is being analyzed...
        document.getElementById("timer3").innerHTML = distance;
    }
    if (stage == 3 && distance > 7){ //TODO: Replace this with analyze completion.
        stage = 4;
        if (task3timer == 0){
            task3timer = distance;
        }
        document.getElementById("timer3").innerHTML = "Done in " + task3timer.toString();
    }
    if (stage == 4){ //Data is being uploaded to the database...
        document.getElementById("timer4").innerHTML = distance;
    }
    if (stage == 4 && distance > 10){ //TODO: Replace this with DB completion
        stage = 5;
        if (task4timer == 0){
            task4timer = distance;
        }
        document.getElementById("timer4").innerHTML = "Done in " + task4timer.toString();
    }
    // document.getElementById("timer1").innerHTML = distance;
}, 1000);




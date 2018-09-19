const sensorAbs = new AbsoluteOrientationSensor();
const sensorRel = new RelativeOrientationSensor();
const sensorGyro = new Gyroscope();
const sensorAcc = new Accelerometer();

$(document).ready(function(){
    $("#ball").css("position", "absolute");
    $("#ball").css("margin", "0");
    $("#ball").css("height", "100");
    $("#ball").css("width", "100");
    $("#ball").css("top", $(window).height() / 2 - 50);
    $("#ball").css("left", $(window).width() / 2 - 50);
    setInterval(move_ball, 300);
    setInterval(send_position, 10000);
});

function move_ball(){
    var new_x = parseInt($("#ball").css("left")) + 0.1 * sensorGyro.x;
    var new_y = parseInt($("#ball").css("top")) + 0.1 * sensorGyro.y;
    if(new_x > $(window).height() || new_x < 0 || new_y > $(window).width() || new_y < 0){
        return
    }
    else{
        $("#ball").css("left", new_x+"px");
        $("#ball").css("top", new_y+"px");
    }
};

function send_position(){
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/sensors/gyro/', true);
    xhr.setRequestHeader('Content-type', 'application/json');
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
            console.log('done!');
        }
    };
    xhr.send($("#ball").css("top") + ',' + $("#ball").css("left"));
}

sensorAbs.start();
sensorRel.start();
sensorGyro.start();
sensorAcc.start();
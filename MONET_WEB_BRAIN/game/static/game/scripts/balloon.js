/* 
    Yumin's Task
    load text_array from DB
*/

const game_height = $(window).height() * 0.8;
var start_time_list = [];
var end_time_list = [];
var response_time = [];
var responses = [];
var terminate = false;
var on_press = false;
var pressed = 0;


function falling_balloon(size, current_index, left, main_balloon = true) {
    if (terminate) {
        return;
    }

    /* generate a balloon */
    const margin = (size / 2) * (1 - 1.414 / 2);
    var current_balloon = $("<div/>", {
        class: "balloon",
        //style:"position:absolute; width:"+size+"px; height:"+size+"px; left:50%; background-color: #ff9966; top:0px"
        style: "position:absolute; width:" + size + "px; height:" + size + "px; left:" + left + "px; top:0px; padding:" + margin + "px"
    });

    /* show the balloon on screen */
    current_balloon.css({ "background": "url('http://icons.iconarchive.com/icons/custom-icon-design/flatastic-6/128/Circle-icon.png')" });
    current_balloon.css("background-size", "cover");
    $(".game").append(current_balloon);

    /* drop the balloon */
    let total_duration = 5000; // 5s
    if (!main_balloon)
        total_duration = Math.floor(Math.random() * 4000 + 6000);
    let total_distance = game_height - size;
    let text_assigned = false;
    let clicked = false;
    var start_time;
    if (main_balloon) {
        total_distance -= size;
        h = size * 2;
        w = size * 2;
        l = left - size / 2;
    }
    else {
        h = size;
        w = size;
        l = left
    }
    current_balloon.animate({ top: total_distance + "px", height: h, width: w, left:l}, {
        duration: total_duration,
        easing: "linear",
        step: function (now, fx) {
            if ($(this).position().top > total_distance * 0.3 && !text_assigned) {
                text_assigned = true;
                start_time = new Date();
                //console.log("start time" + start_time);
                /* if arrived at half, add text */
                if (main_balloon) {
                    $(this).css('text-align', 'center');
                    $(this).css('vertical-align', 'middle');
                    $(this).css('line-height', size + 'px');
                    $(this).css('color', 'white');
                    $(this).text(text_array[current_index]);
                    $(this).boxfit({ multiline: true });
                    on_press = true;
                }
            }
            /* ADD EVENT: if a button pressed, it must be removed */
            //$(this).click(function(){
            if (pressed != 0 && main_balloon && text_assigned && $(this).position().top > total_distance * 0.3) {
                on_press = false;
                responses.push(pressed);
                pressed = 0;
                //console.log(pressed);
                clicked = true;
                var end_time = new Date();
                end_time_list.push(end_time);
                start_time_list.push(start_time);
                var time_elapsed_ms = end_time - start_time;
                console.log(time_elapsed_ms)
                response_time.push(time_elapsed_ms);
                $(this).remove();
                if (main_balloon) {
                    if (current_index + 1 < text_array.length) {
                        falling_balloon(size, current_index + 1, left, main_balloon);
                    }
                    else if (current_index + 1 == text_array.length) {
                        terminate = true;
                        /* 
                            Yumin's Task
                            save response_time to DB
                            link to the result page
                        */

                           start_time_list.toString();
                           response_time.toString();
                           end_time_list.toString();
                           responses.toString();



                           // send the score using POST
                           var xhr = new XMLHttpRequest();
                           xhr.open("POST", '/game/balloon/', true);
       
                           //Send the proper header information along with the request
                           xhr.setRequestHeader("Content-type", "application/json");
       
                           xhr.onreadystatechange = function () {//Call a function when the state changes.
                               if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
                                   // Request finished. Do processing here.
                               }
                           }
       
                           //xhr.send(JSON.stringify(String(accuracy) + ' ' + String(avg_rt)));
                           xhr.send(response_time + '!' + start_time_list + '!' + end_time_list + '!' + responses);
       
                           setTimeout(function () { window.location.replace("/game/balloon/game-result"); }, 1000);
 



                        console.log("start" + start_time_list);
                        console.log("end"+end_time_list);
                        console.log("responses"+responses);
                        console.log("rt" + response_time);
                    }

                }
                else {
                    falling_balloon(size, current_index, left, main_balloon);
                }

            }
        },
        complete: function () {
            if (!clicked) {
                $(this).remove();
                falling_balloon(size, current_index, left, main_balloon);
                /* 
                if (main_balloon) {
                    //response_time.push(0.0);
                    
                    if (current_index + 1 < text_array.length) {
                        falling_balloon(size, current_index + 1, left, main_balloon);
                    }
                    else if (current_index + 1 == text_array.length) {
                        terminate = true;
                        

                        console.log(response_time);
                    }
                    

                }
                else {
                    falling_balloon(size, current_index, left, main_balloon);
                }
                */
            }
        }
    });
    return;
}

$(".start").click(function () {
    /* remove the layout of the main page */
    $(".main_control").remove();
    /* add the layout for the game */
    $(".game").css({ "height": game_height, "background-color": "#ffffff" });
    /* start the game */
    $(".bottom").css({ "height": game_height * 0.25, "background-color":"#dddddd", "padding":game_height * 0.25 * 0.3 + "px" });
    var row = $("<div/>", { class: "row" });
    var col1 = $("<col/>", {class:"col-1 d-flex justify-content-center"});
    var col2 = $("<col/>", {class:"col-2 d-flex justify-content-center"});
    var col3 = $("<col/>", {class:"col-2 d-flex justify-content-center"});
    var col4 = $("<col/>", {class:"col-2 d-flex justify-content-center"});
    var col5 = $("<col/>", {class:"col-2 d-flex justify-content-center"});
    var col6 = $("<col/>", {class:"col-2 d-flex justify-content-center"});
    var col7 = $("<col/>", {class:"col-1 d-flex justify-content-center"});

    var btn1 = $("<button/>", {
        type: "button",
        class: "btn btn-primary btn-lg start",
        text: "1(매우 아니다)",
    });
    btn1.click(function () {
        if(on_press){
            pressed = 1;
        }
    });
    var btn2 = $("<button/>", {
        type: "button",
        class: "btn btn-primary btn-lg start",
        text: "2",
    });
    btn2.click(function () {
        if(on_press){
            pressed = 2;
        }
    });
    var btn3 = $("<button/>", {
        type: "button",
        class: "btn btn-primary btn-lg start",
        text: "3",
    });
    btn3.click(function () {
        if(on_press){
            pressed = 3;
        }
    });
    var btn4 = $("<button/>", {
        type: "button",
        class: "btn btn-primary btn-lg start",
        text: "4",
    });
    btn4.click(function () {
        if(on_press){
            pressed = 4;
        }
    });
    var btn5 = $("<button/>", {
        type: "button",
        class: "btn btn-primary btn-lg start",
        text: "5(매우 그렇다)",
    });
    btn5.click(function () {
        if(on_press){
            pressed = 5;
        }
    });

    col2.append(btn1);
    col3.append(btn2);
    col4.append(btn3);
    col5.append(btn4);
    col6.append(btn5);
    
    row.append(col1);
    row.append(col2);
    row.append(col3);
    row.append(col4);
    row.append(col5);
    row.append(col6);
    row.append(col7);

    $(".bottom").append(row);


    balloon_size = 200;
    small_balloon_size = 100;
    for (i = 0; small_balloon_size * (i + 1) < $(".game").width() / 2 - balloon_size / 2; i++) {
        falling_balloon(small_balloon_size * 0.8, 0, i * small_balloon_size + 0.1 * small_balloon_size, false);
    }
    for (i = Math.floor($(".game").width() / small_balloon_size) - 1; small_balloon_size * i > $(".game").width() / 2 + balloon_size / 2; i--) {
        falling_balloon(small_balloon_size * 0.8, 0, i * small_balloon_size + 0.1 * small_balloon_size, false);
    }
    falling_balloon(balloon_size, 0, $(".game").width() / 2 - balloon_size / 2, true);

});

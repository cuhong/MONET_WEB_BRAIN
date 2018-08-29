/* 
    Yumin's Task
    load text_array from DB
*/

const game_height = $(window).height() * 0.8;
var start_time_list = [];
var end_time_list = [];
var response_time = [];
var responses = [];
var balloon_completed = false;
var terminate = false;
const balloon_size = 100;
const small_balloon_size = 100;
var main_balloon_index = 0;
const stop_displacement = (game_height -balloon_size) / 3;



function falling_balloon(size, current_index, left, main_balloon = true) {
    if (terminate) {
        return;
    }

    /* generate a balloon */
    const margin = (size) * (1 - 1.414 / 2);
    if(main_balloon){
        var current_balloon = $("<div/>", {
            class: "balloon",
            id: "balloon_main",
            //style:"position:absolute; width:"+size+"px; height:"+size+"px; left:50%; background-color: #ff9966; top:0px"
            style: "position:absolute; width:" + size + "px; height:" + size + "px; left:" + left + "px; top:0px; padding:" + margin + "px"
        });    
    }
    else{
        var current_balloon = $("<div/>", {
            class: "balloon",
            //style:"position:absolute; width:"+size+"px; height:"+size+"px; left:50%; background-color: #ff9966; top:0px"
            style: "position:absolute; width:" + size + "px; height:" + size + "px; left:" + left + "px; top:0px; padding:" + margin + "px"
        });    
    }
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
    current_balloon.animate({top:stop_displacement + "px"}, {
        duration: total_duration  / 3,
        easing: "linear"
    });    
    if(main_balloon){
        total_distance = 2 * total_distance / 3;   
    }
    if(main_balloon){
        current_balloon.animate({height: h, width: w, left:l}, {
            duration: total_duration * 2 / 3,
            easing: "linear",
            complete: function () {
                $(this).css('text-align', 'center');
                $(this).css('vertical-align', 'middle');
                $(this).css('line-height', size + 'px');
                $(this).css('color', 'black');
                $(this).text(text_array[current_index]);
                $(this).boxfit({ multiline: true });
                var start_time = new Date();
                start_time_list.push(start_time);
                main_balloon_index += 1;
                balloon_completed = true;
            }
            
        });
    }
    else{
        current_balloon.animate({ top: total_distance + "px", height: h, width: w, left:l}, {
            duration: total_duration * 2 / 3,
            easing: "linear",
            complete: function () {
                $(this).remove();
                falling_balloon(size, current_index, left, main_balloon);
            }
            
        });
    
    }
    return;
}
function remove_main_balloon(pressed){
    //console.log("start time" + start_time);
    /* if arrived, add text */
    balloon_completed = false;
    var current_main_balloon = $('#balloon_main');
    responses.push(pressed);
    console.log(pressed);
    var end_time = new Date();
    end_time_list.push(end_time);
    var time_elapsed_ms = end_time - start_time_list[start_time_list.length - 1];
    console.log(time_elapsed_ms);
    response_time.push(time_elapsed_ms);
    current_main_balloon.remove();
    if (main_balloon_index >= text_array.length) {
        terminate = true;
        /* 
            Yumin's Task
            save response_time to DB
            link to the result page
        */

        start_time_list.toString();
        end_time_list.toString();
        response_time.toString();
        responses.toString();

        var xhr = new XMLHttpRequest();
        xhr.open("POST", '/game/balloon/', true);
        xhr.setRequestHeader("Content-type", "application/json");
        xhr.onreadystatechange = function () {
            if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
            }
        };

        xhr.send(response_time + '!' + start_time_list + '!' + end_time_list + '!' + responses);

        setTimeout(function () { window.location.replace("/game/balloon/game-result"); }, 1000);
    }


}

$(".start").click(function () {
    /* remove the layout of the main page */
    $(".main_control").remove();
    /* add the layout for the game */
    $(".game").css({ "height": game_height, "background-color": "#ffffff" });
    /* start the game */
    $(".bottom").css({ "height": game_height * 0.25, "background-color":"#dddddd"});
    var row0 = $("<div/>", { class: "row", style:"padding-bottom: 10px "});
    var col01 = $("<col/>", {class:"col-4 d-flex justify-content-center"});
    var col02 = $("<col/>", {class:"col-4 d-flex justify-content-center"});
    var col03 = $("<col/>", {class:"col-4 d-flex justify-content-center"});
    var text01 = $("<div/>", {text: "전혀 그렇지 않다"});
    var text03 = $("<div/>", {text:"매우 그렇다"});
    col01.append(text01);
    col03.append(text03);
    row0.append(col01);
    row0.append(col02);
    row0.append(col03);
    $(".bottom").append(row0);

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
        text: "1",
    });
    btn1.click(function () {
        if (balloon_completed){
            next_idx = remove_main_balloon(1);    
            if(!terminate){
                falling_balloon(balloon_size, main_balloon_index, $(".game").width() / 2 - balloon_size / 2, true);
            }    
        }
    });
    var btn2 = $("<button/>", {
        type: "button",
        class: "btn btn-primary btn-lg start",
        text: "2",
    });
    btn2.click(function () {
        if (balloon_completed){
            next_idx = remove_main_balloon(2);    
            if(!terminate){
                falling_balloon(balloon_size, main_balloon_index, $(".game").width() / 2 - balloon_size / 2, true);
            }    
        }
    });
    var btn3 = $("<button/>", {
        type: "button",
        class: "btn btn-primary btn-lg start",
        text: "3",
    });
    btn3.click(function () {
        if (balloon_completed){
            next_idx = remove_main_balloon(3);    
            if(!terminate){
                falling_balloon(balloon_size, main_balloon_index, $(".game").width() / 2 - balloon_size / 2, true);
            }    
        }
    });
    var btn4 = $("<button/>", {
        type: "button",
        class: "btn btn-primary btn-lg start",
        text: "4",
    });
    btn4.click(function () {
        if (balloon_completed){
            next_idx = remove_main_balloon(4);    
            if(!terminate){
                falling_balloon(balloon_size, main_balloon_index, $(".game").width() / 2 - balloon_size / 2, true);
            }    
        }


    });
    var btn5 = $("<button/>", {
        type: "button",
        class: "btn btn-primary btn-lg start",
        text: "5",
    });
    btn5.click(function () {
        if (balloon_completed){
            next_idx = remove_main_balloon(5);    
            if(!terminate){
                falling_balloon(balloon_size, main_balloon_index, $(".game").width() / 2 - balloon_size / 2, true);
            }    
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


    for (i = 0; small_balloon_size * (i + 1) < $(".game").width() / 2 - balloon_size / 2; i++) {
        falling_balloon(small_balloon_size * 0.8, 0, i * small_balloon_size + 0.1 * small_balloon_size, false);
    }
    for (i = Math.floor($(".game").width() / small_balloon_size) - 1; small_balloon_size * i > $(".game").width() / 2 + balloon_size / 2; i--) {
        falling_balloon(small_balloon_size * 0.8, 0, i * small_balloon_size + 0.1 * small_balloon_size, false);
    }
    var target = $("<div/>",{style:"position:absolute; top:"+stop_displacement+"px; height:"+balloon_size+"px; width:"+balloon_size+"px; left:"+($(".game").width() / 2 - balloon_size / 2)+'px; padding:'+(balloon_size / 2) * (1 - 1.414 / 2) +'px; background:url("http://icons.iconarchive.com/icons/iconsmind/outline/128/Target-icon.png") 0% 0% / cover; overflow: hidden;'});
    $(".game").append(target);    

    falling_balloon(balloon_size, 0, $(".game").width() / 2 - balloon_size / 2, true);

});

/* 
    Yumin's Task
    load text_array from DB
*/

let game_height = $(window).height() * 0.9;
var start_time_list = [];
var end_time_list = [];
var response_time = [];
var responses = [];
var balloon_completed = false;
var terminate = false;
const balloon_size = 100;
const small_balloon_size = 100;
var main_balloon_index = 0;
var current_progress = 0;
const stop_displacement = (game_height -balloon_size) / 3;
var balloon_colors = ["#ffabab", "#a79aff", "#afcbff", "#ffa07a", "#fbf298", "#9af8d8"]



function falling_balloon(size, current_index, left, main_balloon = true) {
    if (terminate) {
        return;
    }
    current_color = balloon_colors[Math.floor((Math.random() * 6))];

    /* generate a balloon */
    const margin = (size) * (1 - 1.414 / 2);
    if(main_balloon){
        var current_balloon = $("<div/>", {
            class: "balloon",
            id: "balloon_main",
            //style:"position:absolute; width:"+size+"px; height:"+size+"px; left:50%; background-color: #ff9966; top:0px"
            style: "position:absolute; width:" + size + "px; z-index:2; height:" + size + "px; left:" + left + "px; top:0px; padding:" + margin + "px"
        });    

    }
    else{
        var current_balloon = $("<div/>", {
            class: "balloon",
            //style:"position:absolute; width:"+size+"px; height:"+size+"px; left:50%; background-color: #ff9966; top:0px"
            style: "position:absolute; width:" + size + "px; z-index:1; height:" + size + "px; left:" + left + "px; top:0px; padding:" + margin + "px"
        });    
    }
    /* show the balloon on screen */
    //current_balloon.css({ "background": "url('http://icons.iconarchive.com/icons/custom-icon-design/flatastic-6/128/Circle-icon.png')" });
    //current_balloon.css("background-size", "cover");
    current_balloon.css("background-color", current_color);
    current_balloon.css("border-radius", "50%");
    current_balloon.css("display", "inline-block");
    $(".game").append(current_balloon);

    /* drop the balloon */
    if (main_balloon)
        var total_duration = 1500; // 5s
    else
        var total_duration = 5000; // 5s
    if (!main_balloon)
        total_duration = Math.floor(Math.random() * 4000 + 6000);
    let total_distance = game_height - size;
    let text_assigned = false;
    let clicked = false;
    var start_time;
    if (main_balloon) {
        total_distance -= size;
        h = size * 3;
        w = size * 3;
        l = left - size;
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
                $(this).css("border-radius", "5%");
                $(this).css("left",0);
                $(this).css("width",$(window).width());
                $(this).text(text_array[current_index]);
                //$(this).boxfit({ multiline: true });
                $(this).wordBreakKeepAll();
                $(this).css("font-size","20px");
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
    //console.log(pressed);
    var end_time = new Date();
    end_time_list.push(end_time);
    var time_elapsed_ms = end_time - start_time_list[start_time_list.length - 1];
    //console.log(time_elapsed_ms);
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


function button_pressed(btn_number){
    if (balloon_completed){
        next_idx = remove_main_balloon(btn_number);    
        if(!terminate){
            falling_balloon(balloon_size, main_balloon_index, $(".game").width() / 2 - balloon_size / 2, true);
        }    
    /* update the progress bar */
    current_progress += 1 / text_array.length * 100;
    progress_bar = $("<div/>", {
        "class": "progress",
        "id" : "progress_bar"
    }).append($("<div/>", {
        "class": "progress-bar bg-success",
        "role": "progress-bar",
        "aria-valuenow": ""+current_progress,
        "aria-valuemin": "0",
        "aria-valuemax": "100",
        "style": "width:"+current_progress+"%",
        "text":Math.round(current_progress) + "%"
    }));
    $("#progress_bar").remove();
    $(".game").append(progress_bar);
    }    
}



$(".start").click(function () {
    /* remove the layout of the main page */
    $(".main_control").remove();
    /* change to full-screen mode */
    if (screenfull.enabled) {
        screenfull.request();
        $(document.body).css("width", $(window).width());
        $(document.body).css("height", $(window).height());
    }
    var main2 = $("<div/>", {
        "id": "main2"
    }).append($("<div/>",{
        "class": "game"
    }));
    main2.css("width", $(window).width());
    main2.css("height", $(window).height());
    main2.append($("<div/>",{
        "class": "bottom"
    }));
    $(document.body).append(main2);
    //$("#main2").addClass("fixed");
    game_height = $(window).height() * 0.8;
    /* add the layout for the game */
    $(".game").css({ "height": game_height, "background-color": "#ffffff" });
    var progress_bar = $("<div/>", {
        "class": "progress",
        "id" : "progress_bar"
    }).append($("<div/>", {
        "class": "progress-bar progress-bar-success progress-bar-striped",
        "role": "progress-bar",
        "aria-valuenow": "0",
        "aria-valuemin": "0",
        "aria-valuemax": "100",
        "style": "width:0%"
    }));
    $(".game").append(progress_bar);
    /* start the game */
    //$(".bottom").css({ "height": game_height * 0.25, "background-color":"#dddddd"});
    //var residual_height = $(document).height - $(".game").height
    $(".bottom").css({ "position":"fixed", "top":game_height, "height": $("#main2").height(), "width":$("#main2").width(), "overflow":"hidden", "background-color":"#dddddd"});

    var row0 = $("<div/>", { class: "row", style:"margin: 20px; padding-bottom: 10px "});
    var col01 = $("<col/>", {class:"col-5"});
    var col02 = $("<col/>", {class:"col-2"});
    var col03 = $("<col/>", {class:"col-5"});
    var text01 = $("<p/>", {class:"text-left", text: "전혀 그렇지 않다", style:"text-align: left; font-weight:bold;"});
    var text03 = $("<p/>", {class:"text-right", text:"매우 그렇다", style:"text-align: right; font-weight:bold;"});
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
        class: "button-round",
        text: "1"
    });
    btn1.click(()=>button_pressed(1));
    var btn2 = $("<button/>", {
        
        class: "button-round",
        text: "2",
    });
    btn2.click(()=>button_pressed(2));
    var btn3 = $("<button/>", {
        
        class: "button-round",
        text: "3",
    });
    btn3.click(()=>button_pressed(3));
    var btn4 = $("<button/>", {
        
        class: "button-round",
        text: "4",
    });
    btn4.click(()=>button_pressed(4));
    var btn5 = $("<button/>", {
        
        class: "button-round",
        text: "5",
    });
    btn5.click(()=>button_pressed(5));

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
    var target = $("<div/>",{style:"position:absolute; top:"+stop_displacement+"px; height:"+balloon_size+"px; width:"+balloon_size+"px; left:"+($(".game").width() / 2 - balloon_size / 2)+'px; padding:'+(balloon_size / 2) * (1 - 1.414 / 2) +'px; background:url("/static/game/images/Target-icon.png") 0% 0% / cover; overflow: hidden;'});
    
    $(".game").append(target);    

    falling_balloon(balloon_size, 0, $(".game").width() / 2 - balloon_size / 2, true);

});

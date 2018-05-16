/* 
    Yumin's Task
    load text_array from DB
*/
//var text_array = ["hello world 1", "hello world 2", "hello world 3"];
const game_height = 600;
var response_time = [];


function falling_balloon(size, current_index){
    /* generate a balloon */
    const margin = (size / 2) * (1- 1.414 / 2); 
    const left = $(".game").width() / 2 - size / 2;
    var current_balloon = $("<div/>", {
        class:"balloon",
        //style:"position:absolute; width:"+size+"px; height:"+size+"px; left:50%; background-color: #ff9966; top:0px"
        style:"position:absolute; width:"+size+"px; height:"+size+"px; left:"+left+"px; top:0px; padding:"+margin+"px"
    });

    /* show the balloon on screen */
    current_balloon.css({"background": "url('http://icons.iconarchive.com/icons/custom-icon-design/flatastic-6/128/Circle-icon.png')"});
    current_balloon.css("background-size","cover");
    $(".game").append(current_balloon);

    /* drop the balloon */
    const total_duration = 5000; // 5s
    const total_distance = game_height - size;
    let text_assigned = false;
    let clicked = false;
    current_balloon.animate({top: total_distance +"px"}, {
        duration: total_duration,
        easing: "linear",
        step: function(now, fx) {
            if(now > fx.end / 3 && !text_assigned){
                text_assigned = true;
                var start_time = new Date();
                /* if arrived at half, add text */
                $(this).css('text-align', 'center');
                $(this).css('vertical-align', 'middle');
                $(this).css('line-height', size+'px');
                $(this).css('color','black');
                $(this).text(text_array[current_index]);
                $(this).boxfit({multiline: true});
                /* ADD EVENT: if the balloon clicked, it must be removed */ 
                $(this).click(function(){
                    clicked = true;
                    var end_time = new Date();
                    var time_elapsed_ms = end_time - start_time;
                    response_time.push(time_elapsed_ms);
                    $(this).remove();
                    if(current_index + 1 < text_array.length){
                        falling_balloon(size, current_index + 1);
                    }                    
                    else if(current_index + 1 == text_array.length){
                        /* 
                            Yumin's Task
                            save response_time to DB
                            link to the result page
                        */

                        response_time.toString();
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
                        xhr.send(response_time);

                        setTimeout(function () { window.location.replace("/game/balloon/game-result"); }, 1000);

                        console.log(response_time);
                    }

                });
            }
        },
        complete: function(){
            if(!clicked){
                $(this).remove();
                response_time.push(0.0);
                if(current_index + 1 < text_array.length){
                    falling_balloon(size, current_index + 1);
                }
                else if(current_index + 1 == text_array.length){
                    /* 
                        Yumin's Task
                        save response_time to DB
                        link to the result page
                    */
                    ressponse_time.toString();
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
                    xhr.send(response_time);

                    setTimeout(function () { window.location.replace("/game/balloon/game-result"); }, 1000);
                    console.log(response_time);
                }
    
            }
        }
    });
    return;
}

$(".start").click(function(){
    /* remove the layout of the main page */
    $(".main_control").remove();
    /* add the layout for the game */
    $(".game").css({"height": game_height, "background-color":"#ffffff"});
    /* add the buttom */
    $(".bottom").css({"position":"absolute", "width":"100%", "height":"100%", "background-color": "#e6e6e6"});
    /* start the game */
    falling_balloon(250, 0);
});
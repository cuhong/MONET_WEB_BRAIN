/* 
    Yumin's Task
    load text_array from DB
*/

const game_height = $(window).height();
var response_time = [];


function falling_balloon(size, current_index, left, main_balloon=true){
    /* generate a balloon */
    const margin = (size / 2) * (1- 1.414 / 2); 
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
    let total_duration = 5000; // 5s
    if (!main_balloon)
        total_duration = Math.floor(Math.random() * 4000 + 6000);
    let total_distance = game_height - size;
    let text_assigned = false;
    let clicked = false;
    if(main_balloon){
        total_distance -= size;
        h = size * 2;
        w = size * 2;
    }
    else{
        h = size;
        w = size;
    }
    current_balloon.animate({top: total_distance +"px", height: h, width: w}, {
        duration: total_duration,
        easing: "linear",
        step: function(now, fx) {
            if(now > fx.end / 3 && !text_assigned){
                text_assigned = true;
                var start_time = new Date();
                /* if arrived at half, add text */
                if(main_balloon){
                    $(this).css('text-align', 'center');
                    $(this).css('vertical-align', 'middle');
                    $(this).css('line-height', size+'px');
                    $(this).css('color','black');
                    $(this).text(text_array[current_index]);
                    $(this).boxfit({multiline: true});    
                }
                /* ADD EVENT: if the balloon clicked, it must be removed */ 
                $(this).click(function(){
                    clicked = true;
                    var end_time = new Date();
                    var time_elapsed_ms = end_time - start_time;
                    response_time.push(time_elapsed_ms);
                    $(this).remove();
                    if (main_balloon){
                        if(current_index + 1 < text_array.length){
                            falling_balloon(size, current_index + 1, left, main_balloon);
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
                        }
    
                    }
                    else{
                        falling_balloon(size, current_index, left, main_balloon);
                    }
        
                });
            }
        },
        complete: function(){
            if(!clicked){
                $(this).remove();
                if (main_balloon){
                    response_time.push(0.0);
                    if(current_index + 1 < text_array.length){
                        falling_balloon(size, current_index + 1, left, main_balloon);
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
                    }
    
                }
                else{
                    falling_balloon(size, current_index, left, main_balloon);
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
    /* start the game */
    balloon_size = 200;
    small_balloon_size = 100;
    for(i=0;small_balloon_size*(i+1)<$(".game").width()/2-balloon_size/2;i++){
        falling_balloon(small_balloon_size * 0.8, 0, i*small_balloon_size + 0.1*small_balloon_size, false);
    }
    falling_balloon(balloon_size, 0, $(".game").width()/2 - balloon_size / 2, true);
    for(i=Math.floor($(".game").width() / small_balloon_size) - 1;small_balloon_size*i>$(".game").width()/2+balloon_size/2;i--){
        falling_balloon(small_balloon_size * 0.8, 0, i*small_balloon_size + 0.1*small_balloon_size, false);
    }
});
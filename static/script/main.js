

$(document).ready(function() {
    
    let arr=[{choice: '', from: '', to: ''}];
    let filterArr= [{parameter: '', code: ''}];
    var count= 0;

    
    
    $("#add").click(function() {
        //var filterDiv= $("<div></div>").addClass("filterDiv");
        
        var filter_div= $("<div></div>").attr("id","filterDiv");
        var inp= $('<input type="text"/>'); 
        
        var selectOne= $("<select></select>").attr("id", count);
        //one sec wait here....    count++;
        console.log(selectOne);
        selectOne.append('<option value="select">Select from below</option>','<option value="MACD">MACD Indicator</option>','<option value="RSI">RSI Indicator</option>','<option value="Arron">Arron Indicator</option>','<option value="Engulfing_pattern">Engulfing Pattern</option>','<option value="ADX">ADX Indicator</option>');
        
        
    
        var delIcon= $("<p></p>").text("X").attr("id", "001").css({"cursor": "pointer", "color": "gray"});
        var message= $("<p></p>").css({"padding-left": "40px"});

        
        //console.log(delIcon);
        $(selectOne).addClass("firstSelect");
        //$(selectTwo).addClass("firstSelect");
        $(delIcon).addClass("delIcon");
        $(inp).addClass("inpOne");
        
        $(filter_div).append(selectOne);
        $(filter_div).append(inp);
        //$(filter_div).append(selectTwo);
        $(filter_div).append(delIcon);
        //console.log(`select#${count}`);

        $(selectOne).change(function() {
            var selectedVal= $(this).children("option:selected").val();
            console.log(selectedVal);
            $(filter_div).append(message);
            if(selectedVal === "MACD"){
                message.text("Please enter three parameters (Number of Days) for MACD like 12,26,9(Default)");
                inp.attr("maxlength", "8");
            }else if(selectedVal === "RSI"){
                message.text("Please set one parameter(Number of days) for RSI like 14(Default)");
                inp.attr("maxlength", "2");
            }else if(selectedVal === "Aroon"){
                message.text("Please set one parameter(Number of days) for Aroon like 25(Default)");
                inp.attr("maxlength", "2");
            }else if(selectedVal === "Engulfing_pattern"){
                message.text("No need to enter any Parameter");
                inp.attr("maxlength", "2");
            }else if(selectedVal === "ADX"){
                message.text("Please set one parameter(Number of days) for ADX like 16(Default)");
                inp.attr("maxlength", "2");
            }
        });

        $(inp).blur(function() {
            filterArr.push({code: $(selectOne).children("option:selected").val(), parameter: $(inp).val()});
        });
        
        
        
        count++;

        $("#dynaSec").fadeIn(1000, function() {
            $(this).append(filter_div);
        });
        
        $(delIcon).click(function() {
            console.log("running");
            $(filter_div).slideUp(150,function() {
                $(this).remove();
            });
        })
  
    }) 
    
    $("#signup").click(function() {
        arr.push({choice: $("#searchBar").val()});
    })

    
    let isDuplicate= false;
    $(".log").click(function() {
        //arr.push({choice: $("#searchBar").val()});
        console.log(arr);
        //console.log(filterArr);
        //console.log(uniqueArr);
    })

    

    $("#run").click(function() {
        //alert(inpVal);
        //alert(inpVal);
        //alert($(inp).val());
        /*$(inp).change(function() {
            arr.push();
        })*/
        console.log("running");
        arr.push({from: $("#startDate").val()});
        arr.push({to: $("#endDate").val()});
        arr.push({choice: $("#searchBar").val()});
        console.log(arr);
          
        

        const uniqueArr= filterArr.filter((item,index)=> index !== filterArr.indexOf(item.code));
        console.log(uniqueArr);

        $.ajax(
            {
                type: 'POST',
                url: '/test',
                data:JSON.stringify(arr),
                contentType: 'application/json',
                dataType: 'json',
                success: function(result) {
                    console.log("Result:");
                    console.log(result);

                },
                error: function(error){
                    console.log(error);
                }
                

            }
        )

        $.ajax(
            {
                type: 'POST',
                url: '/test1',
                data:JSON.stringify(filterArr),
                contentType: 'application/json',
                dataType: 'json',
                success: function(result) {
                    console.log("Result:");
                    console.log(result);

                },
                error: function(error){
                    console.log(error);
                }
                

            }
        )

        //var checkSameVal= (`select#${count}`).children("option:selected").val();
         

        // if(sameVal) {
        //     alert("Please set different filter");
        // }


        //arr.push({filter.push({code: $(selectOne).children("option:selected").val(), parameter: $(inp).val()}}));
        // arr.map(item=> {
        //     item.filter.map(item=> {
        //         item.code= $(selectOne).children("option:selected").val();
        //         item.parameter= $(inp).val();
        //     })
        // })
        //arr.push($(inp).val());
        //arr.push($("select#s2 option:checked").val());
        //console.log(arr);
        
    })

})

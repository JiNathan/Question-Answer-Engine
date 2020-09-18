var index = 0;
var answers;
var inputtext = '';
var numOfQuestion = 3;
let hasAnswer = false;

$('#previous, #next').hide();

function giveresult(){
  hasAnswer = false;
  index = 0;
  inputtext = $("#Text").val()
  var inputquestion = $("#Question").val();

  $.post(
    "http://localhost:5000/result?Text=" + inputtext + "&Question=" + inputquestion,
    {'Text': inputtext, 'Question': inputquestion}
  ).done(function(data){
    //alert("Date Loaded: " + data)
//    $("#Result").val(inputtext);
//    console.log( $("#Result").val())
//	highlightText(data[0])
    console.log(data)
//    $("#Result").val(data[0]+"\n"+data[1]);
    answers = data;
    search(0)
  });
}

function search(position) {
    index += position ;
    if (index >= 0 && index < numOfQuestion){
        if (answers[0] == 'there was no match'){
            document.getElementById("Result").innerHTML = answers[0].toUpperCase();
        }
        else{
            hasAnswer = true;
            showHideNextButton()
            showHidePreviousButton()
            $('p#Result').text(inputtext)
            let result = document.getElementById("Result").innerHTML;
            let re = new RegExp(answers[index],"g"); // search for all instances
            let newText = result.replace(re, `<mark class= 'highlight'>${answers[index]}</mark>`);
            document.getElementById("Result").innerHTML = newText;

        }
	}
}

function showHidePreviousButton(){
    if(index >0){
        $('#previous').show();
    }else
        $('#previous').hide();
}

function showHideNextButton(){
    if(index < numOfQuestion -1){
        $('#next').show();
    }else
        $('#next').hide();
}



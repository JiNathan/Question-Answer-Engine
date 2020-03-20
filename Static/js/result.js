function giveresult(){
  var inputtext = $("#Text").val();
  var inputquestion = $("#Question").val();
  $.post(
    "http://localhost:5000/result?Text=" + inputtext + "&Question=" + inputquestion,
    {'Text': inputtext, 'Question': inputquestion}
  ).done(function(data){
    //alert("Date Loaded: " + data)
	$("#Result").val(data);
  });
}

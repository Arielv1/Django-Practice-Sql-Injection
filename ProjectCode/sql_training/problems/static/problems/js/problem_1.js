

//var check = $("#check");
//check.empty();
App = {

//  check_confirm_answer: function()
//  {
//      var txt;
//      var confirmed = confirm("you sure you want to see the answer?");
//      if (confirmed == true) {
//          txt = "You pressed OK!";
//      }
//      else {
//          txt = "You pressed Cancel!";
//      }
//  }
  change: function() {
  //      var confirmed = confirm("you sure you want to see the answer?");
   var confirmed = confirm("Hey sss");
         if (confirmed == true) {
          txt = "You pressed OK!";
      }
      else {
          txt = "You pressed Cancel!";
      }
      alert(txt);
  $("#check").html(txt);
  }

};

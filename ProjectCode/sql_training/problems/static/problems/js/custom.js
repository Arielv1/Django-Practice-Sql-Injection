   // Define the Dialog and its properties.
//    $("#dialog-confirm").dialog({
//        resizable: false,
//        modal: true,
//        title: "Modal",
//        height: 250,
//        width: 400,
//        buttons: [{
//            "Yes": function () {
//                $(this).dialog('close');
//                callback(true);
//            },
//                "No": function () {
//                $(this).dialog('close');
//                callback(false);
//            }
//        }]
//    });
//}

$('#btnOpenDialog').click(function() {
        // get form associated with the button
        console.log("we get here ????????");
        $("#dialog-confirm").dialog({
            resizable: false,
            height:140,
            width: 200,
            modal: true,
            buttons:[
            {
               text: "Yes",
               click: function() {
                   $( this ).dialog( "close" );
                   console.log("pressed yes?");
               }}

            ]
        });
        console.log("we get here ???????? end of function");

});

//               ,{
//                text: "No",
//                click: function() {
//                    console.log("pressed no?");
//                    $( this ).dialog( "close" );
//                }
//            }
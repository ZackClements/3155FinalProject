$(document).ready(function (){
    $(".add").click(function() {
        $("form > p:first-child").clone(true).insertBefore("form > p:last-child");

        return false;
    });

    $(".remove").click(function() {
        $(this).parent().remove();
    });
});



// GRAPH TODO:
/*
When form is submitted, search calories.csv and locate each food item
Create a circle graph of the calories of each food item
 */
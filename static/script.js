function sync() {
  str = "";
  one = 0;
  $(".clickable").each(function() {
    str += $(this).attr('id');
    if ($(this).hasClass('no')) {
      str += " 0\n";
    } else {
      str += " 1\n";
      one += 1;
    }
  });
  $("#status").text("Syncing...");
  //alert($("#folder").text());
  $.post("update", {folder: $("#folder").text(), data: str, overwrite: 1}, function(data) {
    if (data.charAt(0) == "1") {
      $("#status").text("Synced " + one);
    } else {
      $("#status").text("Failed");
    }
  });
}
var z, x, hiding = 0;
function hide() {
  if (hiding) {
    $("#hide").html("Hide unselected");
    $(".no").show();
  } else {
    $("#hide").html("Show unselected");
    $(".no").hide();
  }
  hiding ^= 1;
}
$(document).ready(function() {
  $(".clickable").click(function() {
    $(this).toggleClass('no');
    sync();
  }).mousemove(function() {
    if (z) {
      $(this).addClass('no');
    } else if (x) {
      $(this).removeClass('no');
    }
  });

  $("#clear").click(function() {
    $(".clickable").removeClass("no");
    sync();
  });

  $("#hide").click(function() {
    hide();
  });
  sync();
  hide();
});
$(document).keydown(function(e) {
  if (e.which == 90) z = 1; 
  if (e.which == 88) x = 1;
});
$(document).keyup(function(e) {
  if (e.which == 90) z = 0;
  if (e.which == 88) x = 0;
  sync();
});

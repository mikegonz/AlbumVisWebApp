function updateimage(username) {
  $.get("/api/playing/" + username, function(data, status) {
    console.log("Data: " + data + "\nStatus: " + status);
  });
  document.getElementById("vis").src = "/static/uhoh.jpg";
}

function reqloop() {
  return "it works";
}

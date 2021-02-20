function startPolling(username) {
  $.get("/api/playing/" + username, function(data, status) {
    document.getElementById("vis").src = data.path;
    poll(username);
  });
}

function poll(username) {
  $.get("/api/playingnext/" + username, function(data, status) {
    document.getElementById("vis").src = data.path;
    poll(username);
  });
}
window.onload = startPolling;

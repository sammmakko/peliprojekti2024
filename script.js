// pelaajan nicknamen asettaminen
function setNickname(nickname) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      console.log("nickname asetettu: " + nickname);
    }
  };
  xhttp.open("PUT", "/player/" + nickname, true);
  xhttp.send();
}

// pelin aloittaminen
function startGame() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      console.log("peli aloitettu!");
    }
  };
  xhttp.open("POST", "/game/start", true);
  xhttp.send();
}

// pelitilanteen tarkistaminen
function checkGameStatus() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var response = JSON.parse(this.responseText);
      console.log("Pelin tilanne: ", response);
    }
  };
  xhttp.open("GET", "/game/status", true);
  xhttp.send();
}


setNickname("me");

startGame();

checkGameStatus();
function hamburgerMenu(){
  document.getElementById("hamburger").classList.toggle("show");
}


window.onclick = function(e) {
  if (!e.target.matches('.button')) {
  var hamburger = document.getElementById("hamburger");
    if (hamburger.classList.contains('show')) {
        hamburger.classList.remove('show');
    }
  }
}

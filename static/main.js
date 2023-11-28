
// dark mode
var darkmode = document.getElementById("darkmode");

darkmode.onclick=function(){
    document.body.classList.toggle("darktheme");
}
// scroll
const sr= ScrollReveal({
    distance: '65px',
    duration: 2600,
    delay: 450,
    reset: true
});
sr.reveal('.home-text',{delay:100, origin:'bottom'});
sr.reveal('.home-img',{delay:100, origin:'top'});

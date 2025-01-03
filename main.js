let tabs = document.querySelectorAll(".tabs h3");
let tabContents = document.querySelectorAll(".tab-content div");

tabs.forEach((tab, index) => {
  tab.addEventListener("click", () => {
    tabContents.forEach((content) => {
      content.classList.remove("active");
    });
    tabs.forEach((tab) => {
      tab.classList.remove("active");
    });
    tabContents[index].classList.add("active");
    tabs[index].classList.add("active");
  });
});

var link = document.querySelector('.link');
// video download button function 
function video() {
  if (link.value != "") {
    if (link.value.indexOf("https://youtu.be/") != -1)
    {

      var YTurl = link.value.replace("https://youtu.be/", "https://www.000tube.com/watch?v=");

      window.open(YTurl, '_bhank');
    }
    else {

      var YTurl = link.value.replace("you", "000");

      window.open(YTurl, '_bhank');
    }
  }
}
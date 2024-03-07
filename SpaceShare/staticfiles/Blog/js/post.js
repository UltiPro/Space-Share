if (window.location.href.indexOf("#comments") > -1) {
    const scrollTo = document.getElementById("scroll-auto-target");
    window.scrollBy(0, scrollTo.offsetTop - 115);
}
const modal_click = document.getElementById("modal-image-click");
const modal_id = document.getElementById("modal-image-id");
const modal_img = document.getElementById("modal-image-img");

document.addEventListener("DOMContentLoaded", e => {
    modal_click.onclick = function () {
        modal_id.style.display = "block";
        modal_img.src = modal_click.src;
    }
    modal_id.onclick = function () {
        modal_id.style.display = "none";
    }
});
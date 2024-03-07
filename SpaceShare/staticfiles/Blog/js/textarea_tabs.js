addEventListener("DOMContentLoaded", (event) => {
    const textarea = document.querySelector("textarea");
    textarea.textContent = textarea.textContent.replaceAll("&emsp;", "    ");
    textarea.addEventListener("keydown", function (e) {
        if (e.key == "Tab") {
            e.preventDefault();
            const start = this.selectionStart;
            const end = this.selectionEnd;
            this.value = this.value.substring(0, start) + "    " + this.value.substring(end);
            this.selectionStart = this.selectionEnd = start + 4;
        }
    });
});
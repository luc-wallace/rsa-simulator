// @ts-nocheck

const els = document.getElementsByClassName("copy");
for (let el of els) {
  el.addEventListener("click", (e) => {
    const target = e.target.dataset.input;
    const input = document.getElementById(target);
    input.select();
    input.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(input.value);
    alert("Copied to clipboard.");
  });
}

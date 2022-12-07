function vis_toggle() {
	let x = document.getElementById("vis_toggle");
	const style = getComputedStyle(x);
	if (style.display === "none") {
	  x.style.display = "block";
	} else {
	  x.style.display = "none";
	}
 }
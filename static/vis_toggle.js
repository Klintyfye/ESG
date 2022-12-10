
function vis_toggle() {
	let x = document.getElementById("vis_toggle");
	const style = getComputedStyle(x);
	if (style.display === "none") {
		x.style.display = "block";
		document.getElementById("adv_view").innerHTML = "Basic View"
	} else {
		x.style.display = "none";
		document.getElementById("adv_view").innerHTML = "Advanced View"
	}
 }
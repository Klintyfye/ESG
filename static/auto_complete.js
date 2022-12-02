// Getting the required elements
const searchWrapper = document.querySelector(".search-bar-form");
const inputBox = searchWrapper.querySelector("input");
const suggBox = document.getElementById("list_box")

// If the user presses any key
inputBox.onkeyup = (e)=>{
	const s = JSON.stringify(e.target.value);
	$.ajax({
		url: "/auto_complete",
		type: "POST",
		contentType: "application/json",
		data: JSON.stringify(s)
	})
	.then(function (response){
		rm_auto_com();
		if (response.length){ // To remove any empty responses
			for (let i = 0; i < 4; i++){
				document.getElementById("list_box").innerHTML += "<li onclick='select(this)'>" + response[i] + "</li>";
			}
		}
	})
}

function rm_auto_com(){
	while (suggBox.lastElementChild) {
		suggBox.removeChild(suggBox.lastElementChild);
	}
}

function select(element){
	let sel = element.textContent;
	inputBox.value = sel;
	rm_auto_com();
}
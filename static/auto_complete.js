// Getting the required elements
const searchWrapper = document.querySelector(".search-bar-form");
const inputBox = searchWrapper.querySelector("input");
const suggBox = searchWrapper.querySelector(".autocom-box");

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
		if (response.length){ // To remove any empty responses
			for (let i = 0; i < 4; i++){
				document.getElementById("test").innerHTML += "<li>" + response[i] + "</li>";
				console.log(response[i])
	// https://www.youtube.com/watch?v=QxMBHi_ZiT8 Make the suggestions clickable.
	// Remove the old suggestions
			}
		}
	})
}

function get_rating(rating) {
	console.log(rating);

	// Get percentage
	const starPercentage = (rating / 5) * 100;

	console.log(starPercentage);

	// Round to nearest 10
	const starPercentageRounded = `${Math.round(starPercentage / 10) * 10}%`;

	console.log(starPercentageRounded);

	// Set width of stars-inner to percentage
	document.querySelector(`.stars-inner`).style.width = starPercentageRounded;

	// Add number rating
	document.querySelector(`.number-rating`).innerHTML = rating;
}

const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
	getLocation()
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});

function getLocation(){
	$.get("https://api.ipdata.co?api-key=a826677e341edcf50998fa5373bc70af115e2ee66cd35645f455280d", function(response) {
		const lat = response.latitude;
		const lng = response.longitude;
		document.getElementById("location_coordinates").value = `${lat} ${lng}`
	}, "jsonp");
}
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
	if ("geolocation" in navigator) {
		navigator.geolocation.getCurrentPosition(
		(position) => {
			const lat = position.coords.latitude;
			const lng = position.coords.longitude;
			document.getElementById("location_coordinates").value = `${lat} ${lng}`
		},
		(error) => {
			console.error("Error getting user location:", error);
		}
		);
	} else {
		console.error("Geolocation is not supported by this browser.");
	}
}
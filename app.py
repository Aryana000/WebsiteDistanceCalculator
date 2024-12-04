from flask import Flask, render_template, request, jsonify
import folium
from haversine import haversine, Unit
import os

app = Flask(__name__)

# Route untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk perhitungan jarak dan bearing
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        lat1 = float(request.form['lat1'])
        lon1 = float(request.form['lon1'])
        lat2 = float(request.form['lat2'])
        lon2 = float(request.form['lon2'])

        # Menghitung jarak menggunakan rumus haversine
        coords_1 = (lat1, lon1)
        coords_2 = (lat2, lon2)
        distance = haversine(coords_1, coords_2, unit=Unit.KILOMETERS)

        # Menghitung sudut bearing
        bearing = calculate_bearing(lat1, lon1, lat2, lon2)

        return jsonify(distance=distance, bearing=bearing)
    except Exception as e:
        return jsonify(error=str(e))

# Fungsi untuk menghitung bearing
def calculate_bearing(lat1, lon1, lat2, lon2):
    from math import radians, degrees, sin, cos, atan2

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    d_lon = lon2 - lon1
    x = cos(lat2) * sin(d_lon)
    y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(d_lon)
    
    initial_bearing = atan2(x, y)
    
    # Mengkonversi dari radian ke derajat
    initial_bearing = degrees(initial_bearing)
    
    # Menjadikan bearing positif
    compass_bearing = (initial_bearing + 360) % 360
    return compass_bearing

if __name__ == '__main__':
    app.run(debug=True)

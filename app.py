from flask import Flask, jsonify, render_template
from skyfield.api import load

app = Flask(__name__)

# Tải dữ liệu NASA
print("Đang tải dữ liệu thiên văn...")
eph = load('de421.bsp')
ts = load.timescale()

sun = eph['sun']
# Đã xóa moon = eph['moon']

# Cơ sở dữ liệu thông tin
celestial_bodies = {
    'mercury': {'obj': eph['mercury'], 'vi': 'Sao Thủy', 'desc': 'Hành tinh nhỏ nhất, bề mặt đầy hố thiên thạch.',
                'stats': {'temp': '430°C / -180°C', 'radius': '2,439 km', 'period': '88 days', 'day': '59 days'},
                'rotation_speed': 0.017, 'period_val': 88, 'atmos_color': None},
    
    'venus':   {'obj': eph['venus'],   'vi': 'Sao Kim',  'desc': 'Hành tinh nóng nhất do hiệu ứng nhà kính.',
                'stats': {'temp': '462°C', 'radius': '6,051 km', 'period': '225 days', 'day': '243 days'},
                'rotation_speed': -0.004, 'period_val': 225, 'atmos_color': [0.8, 0.6, 0.2]},
    
    'earth':   {'obj': eph['earth'],   'vi': 'Trái Đất', 'desc': 'Hành tinh duy nhất được biết đến có sự sống.',
                'stats': {'temp': '15°C', 'radius': '6,371 km', 'period': '365 days', 'day': '24 hours'},
                'rotation_speed': 1.0, 'period_val': 365, 'atmos_color': [0.2, 0.5, 1.0]},
    
    'mars':    {'obj': eph['mars'],    'vi': 'Sao Hỏa',  'desc': 'Hành tinh Đỏ, mục tiêu thám hiểm của loài người.',
                'stats': {'temp': '-60°C', 'radius': '3,389 km', 'period': '687 days', 'day': '24.6 hours'},
                'rotation_speed': 0.97, 'period_val': 687, 'atmos_color': [0.8, 0.3, 0.1]},
    
    'jupiter': {'obj': eph['jupiter barycenter'], 'vi': 'Sao Mộc', 'desc': 'Hành tinh khí khổng lồ lớn nhất hệ mặt trời.',
                'stats': {'temp': '-145°C', 'radius': '69,911 km', 'period': '12 years', 'day': '9.9 hours'},
                'rotation_speed': 2.4, 'period_val': 4333, 'atmos_color': [0.7, 0.6, 0.5]},
    
    'saturn':  {'obj': eph['saturn barycenter'],  'vi': 'Sao Thổ', 'desc': 'Nổi tiếng với hệ thống vành đai tuyệt đẹp.',
                'stats': {'temp': '-178°C', 'radius': '58,232 km', 'period': '29 years', 'day': '10.7 hours'},
                'rotation_speed': 2.18, 'period_val': 10759, 'atmos_color': [0.8, 0.7, 0.4]},
    
    'uranus':  {'obj': eph['uranus barycenter'],  'vi': 'Sao Thiên Vương', 'desc': 'Hành tinh băng khổng lồ, trục quay nằm ngang.',
                'stats': {'temp': '-224°C', 'radius': '25,362 km', 'period': '84 years', 'day': '17 hours'},
                'rotation_speed': -1.41, 'period_val': 30687, 'atmos_color': [0.4, 0.8, 0.9]},
    
    'neptune': {'obj': eph['neptune barycenter'], 'vi': 'Sao Hải Vương', 'desc': 'Hành tinh xa nhất, nơi có những cơn bão cực mạnh.',
                'stats': {'temp': '-214°C', 'radius': '24,622 km', 'period': '165 years', 'day': '16 hours'},
                'rotation_speed': 1.5, 'period_val': 60190, 'atmos_color': [0.2, 0.4, 0.8]},
}

SCALE_FACTOR = 1e6

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/planets')
def get_positions():
    t = ts.now()
    data = []

    for name, info in celestial_bodies.items():
        astrometric = sun.at(t).observe(info['obj'])
        x, y, z = astrometric.position.km
        data.append({
            'name_en': name.capitalize(),
            'name_vi': info['vi'],
            'type': 'planet',
            'desc': info['desc'],
            'stats': info['stats'],
            'rotation_speed': info['rotation_speed'],
            'period_val': info['period_val'],
            'atmos_color': info['atmos_color'],
            'position': {'x': x / SCALE_FACTOR, 'y': z / SCALE_FACTOR, 'z': y / SCALE_FACTOR}
        })

    # Đã xóa phần xử lý Mặt Trăng

    return jsonify({'planets': data})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

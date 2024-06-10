# cartridge.py

from flask import Blueprint, jsonify, request, render_template
from db_config import DATABASE_CONFIG
from datetime import datetime
import mysql.connector

cartridge_bp = Blueprint('cartridge', __name__)
db = mysql.connector.connect(**DATABASE_CONFIG)

@cartridge_bp.route('/cartridge', methods=['POST'])
def add_cartridge():
    data = request.get_json()
    cursor = db.cursor()
    sql = "INSERT INTO cartridges (cartridge_no, refill_date, used_date, user_allotted, user_department, location) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (
        data['cartridge_no'],
        datetime.strptime(data['refill_date'], '%Y-%m-%d').date(),
        datetime.strptime(data['used_date'], '%Y-%m-%d').date(),
        data['user_allotted'],
        data['user_department'],
        data['location']
    )
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    return jsonify({'message': 'Cartridge added successfully!'})

@cartridge_bp.route('/cartridges', methods=['GET'])
def get_cartridges():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cartridges")
    cartridges = cursor.fetchall()
    cursor.close()
    for cartridge in cartridges:
        cartridge['refill_date'] = cartridge['refill_date'].strftime('%Y-%m-%d')
        cartridge['used_date'] = cartridge['used_date'].strftime('%Y-%m-%d')
    return render_template('cartridges.html', cartridges=cartridges)

@cartridge_bp.route('/cartridge/<id>', methods=['PUT'])
def update_cartridge(id):
    data = request.get_json()
    cursor = db.cursor()
    sql = "UPDATE cartridges SET cartridge_no = %s, refill_date = %s, used_date = %s, user_allotted = %s, user_department = %s, location = %s WHERE id = %s"
    values = (
        data['cartridge_no'],
        datetime.strptime(data['refill_date'], '%Y-%m-%d').date(),
        datetime.strptime(data['used_date'], '%Y-%m-%d').date(),
        data['user_allotted'],
        data['user_department'],
        data['location'],
        id
    )
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    return jsonify({'message': 'Cartridge updated successfully!'})

@cartridge_bp.route('/cartridge/<id>', methods=['DELETE'])
def delete_cartridge(id):
    cursor = db.cursor()
    sql = "DELETE FROM cartridges WHERE id = %s"
    values = (id,)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    return jsonify({'message': 'Cartridge deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)

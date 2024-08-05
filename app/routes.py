from flask import Blueprint, request, jsonify
from app.models import Timer, db
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/timer', methods=['POST'])
def add_timer():
    data = request.json
    title = data.get("title")
    end_time_str = data.get("end_time")
    completion_status = data.get("completion_status")
    
    if not title or not end_time_str or completion_status is None:
        print("Missing data")
        return jsonify({"error": "Missing data"}), 400
    
    end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
    
    new_timer = Timer(title=title, end_time=end_time, expired=completion_status)
    db.session.add(new_timer)
    db.session.commit()
    
    print("Timer added successfully")
    return jsonify({"message": "Timer added successfully"}), 201

@bp.route('/timer', methods=['DELETE'])
def delete_timer():
    data = request.json
    title = data.get("title")
    
    if not title:
        print("Missing data")
        return jsonify({"error": "Missing data"}), 400
    
    timer = Timer.query.filter_by(title=title).first()
    if not timer:
        print("Timer not found")
        return jsonify({"error": "Timer not found"}), 404
    
    db.session.delete(timer)
    db.session.commit()
    
    print("Timer deleted successfully")
    return jsonify({"message": "Timer deleted successfully"}), 200

@bp.route('/timer', methods=['PUT'])
def complete_timer():
    data = request.json
    title = data.get("title")
    end_time_str = data.get("duration")
    completion_status = data.get("completion_status")
    
    if not title or not end_time_str or completion_status is None:
        print("Missing data")
        return jsonify({"error": "Missing data"}), 400
    
    timer = Timer.query.filter_by(title=title).first()
    if not timer:
        print("Timer not found")
        return jsonify({"error": "Timer not found"}), 404
    
    timer.expired = completion_status
    db.session.commit()
    
    print("Timer completed successfully") #TODO: Alarm sound
    return jsonify({"message": "Timer status updated successfully"}), 200

@bp.route('/timers', methods=['GET'])
def get_timers():
    timers = Timer.query.filter_by(expired=False).all()
    return jsonify([{
        "title": timer.title,
        "end_time": timer.end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "completion_status": timer.expired
    } for timer in timers])

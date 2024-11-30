from flask import Flask, render_template, jsonify
from models import (get_user_count,
                    get_group_count, 
                    get_message_count_today,
                    get_total_users_by_date,
                    get_daily_new_users,
                    get_total_groups_by_date,
                    get_daily_new_groups,
                    get_total_messages_by_date,
                    get_daily_new_messages,
                    calculate_weekly_growth
                    )

app = Flask(__name__)

@app.route('/')
def index():
    """Render the main HTML page."""
    return render_template('index.html')

@app.route('/stats', methods=['GET'])
def get_stats():
    """API endpoint to fetch statistics."""
    try:
        user_count = get_user_count()
        group_count = get_group_count()
        message_count_today = get_message_count_today()

        return jsonify({
            'user_count': user_count,
            'group_count': group_count,
            'message_count_today': message_count_today
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/total_users_by_date', methods=['GET'])
def total_users_by_date():
    return jsonify(get_total_users_by_date())

@app.route('/api/daily_new_users', methods=['GET'])
def daily_new_users():
    return jsonify(get_daily_new_users())

@app.route('/api/total_groups_by_date', methods=['GET'])
def total_groups_by_date():
    return jsonify(get_total_groups_by_date())

@app.route('/api/daily_new_groups', methods=['GET'])
def daily_new_groups():
    return jsonify(get_daily_new_groups())

@app.route('/api/total_messages_by_date', methods=['GET'])
def total_messages_by_date():
    return jsonify(get_total_messages_by_date())

@app.route('/api/daily_new_messages', methods=['GET'])
def daily_new_messages():
    return jsonify(get_daily_new_messages())

@app.route('/api/weekly_user_growth')
def weekly_user_growth():
    growth_data = calculate_weekly_growth('users', 'join_date')
    return jsonify(growth_data)

@app.route('/api/weekly_group_growth')
def weekly_group_growth():
    growth_data = calculate_weekly_growth('groups', 'join_date')
    return jsonify(growth_data)

@app.route('/api/weekly_message_growth')
def weekly_message_growth():
    growth_data = calculate_weekly_growth('messages', 'message_date')
    return jsonify(growth_data)

if __name__ == '__main__':
    app.run(debug=True)

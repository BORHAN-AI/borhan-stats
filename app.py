from flask import Flask, render_template, jsonify
from models import get_user_count, get_group_count, get_message_count_today
# from models import get_user_count, get_group_count, get_message_count_yesterday

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
        # message_count_today = get_message_count_yesterday()

        return jsonify({
            'user_count': user_count,
            'group_count': group_count,
            'message_count_today': message_count_today
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

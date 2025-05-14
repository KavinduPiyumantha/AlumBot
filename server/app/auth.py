from flask import Blueprint, request
from server.app.utils.token_helper import TokenHelper
from server.logger.logger_config import my_logger as logger

auth_bp = Blueprint('auth', __name__, url_prefix='/alumBot_api/auth')


@auth_bp.route('/get_token', methods=['POST'])
def get_token():
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return {
            'retcode': -20000,
            'message': 'user_id is required',
            'data': {}
        }
    
    # Check if authentication is required
    conn = None
    require_auth = False
    
    try:
        from server.app.utils.sqlite_client import get_db_connection
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if we have any accounts in the database
        cur.execute('SELECT COUNT(*) as count FROM t_account_tab')
        result = cur.fetchone()
        # If there are accounts, require authentication
        if result and result['count'] > 0:
            require_auth = True
            
        # If authentication is required, deny token generation without login
        if require_auth:
            return {
                'retcode': -20002,
                'message': 'Authentication required. Please login first.',
                'data': {}
            }
            
    except Exception as e:
        logger.error(f"Error checking authentication requirement: {e}")
    finally:
        if conn:
            conn.close()

    try:
        # generate token
        token = TokenHelper.generate_token(user_id)
        logger.success(f"Generate token: '{token}' with user_id: '{user_id}'")
        return {"retcode": 0, "message": "success", "data": {"token": token}}
    except Exception as e:
        logger.error(
            f"Generate token with user_id: '{user_id}' is failed, the exception is {e}"
        )
        return {'retcode': -20001, 'message': str(e), 'data': {}}

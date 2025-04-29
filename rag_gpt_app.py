import os
from dotenv import load_dotenv
from server.constant.env_constants import check_env_variables

# Load environment variables from .env file
load_dotenv(override=True)
check_env_variables()

from flask import Flask, send_from_directory, abort, request, jsonify
from flask_cors import CORS
from werkzeug.utils import safe_join
from server.app import account, auth, bot_config, common, files, intervention, queries, sitemaps, urls
from server.constant.constants import STATIC_DIR, MEDIA_DIR
from server.logger.logger_config import my_logger as logger


app = Flask(__name__, static_folder=STATIC_DIR)
CORS(app)


"""
Background:
In scenarios where using a dedicated static file server (like Nginx) is not feasible or desired, Flask can be configured to serve static files directly. This setup is particularly useful during development or in lightweight production environments where simplicity is preferred over the scalability provided by dedicated static file servers.

This Flask application demonstrates how to serve:
- Static media files from a dynamic path (`MEDIA_DIR`)
- The homepages and assets for two single-page applications (SPAs): 'alumBot' and 'alumbot-admin'.

Note:
While Flask is capable of serving static files, it's not optimized for the high performance and efficiency of a dedicated static file server like Nginx, especially under heavy load. For large-scale production use cases, deploying a dedicated static file server is recommended.

The provided routes include a dynamic route for serving files from a specified media directory and specific routes for SPA entry points and assets. This configuration ensures that SPA routing works correctly without a separate web server.
"""
# Dynamically serve files from the MEDIA_DIR
@app.route(f'/{MEDIA_DIR}/<path:filename>')
def serve_media_file(filename):
    # Use safe_join to securely combine the static folder path and filename
    file_path = safe_join(app.static_folder, MEDIA_DIR, filename)

    # Check if the file exists and serve it if so
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory(os.path.join(app.static_folder, MEDIA_DIR), filename)
    else:
        # Return a 404 error if the file does not exist
        return abort(404)


# Route for the homepage of the 'alumBot' site
@app.route('/alumBot', strict_slashes=False)
def index_chatbot():
    return send_from_directory(f'{app.static_folder}/alumBot', 'index.html')


# Route for serving other static files of the 'alumBot' application
@app.route('/alumBot/<path:path>')
def serve_static_chatbot(path):
    return send_from_directory(f'{app.static_folder}/alumBot', path)


# Route for the homepage of the 'alumbot-admin' site
@app.route('/alumbot-admin', strict_slashes=False)
def index_admin():
    return send_from_directory(f'{app.static_folder}/alumbot-admin', 'index.html')


# Route for serving other static files of the 'alumbot-admin' application
@app.route('/alumbot-admin/<path:path>')
def serve_static_admin(path):
    return send_from_directory(f'{app.static_folder}/alumbot-admin', path)


# Route for the homepage of the 'open-kf-admin' site - keeping the original route for backward compatibility
@app.route('/open-kf-admin', strict_slashes=False)
def index_admin_original():
    return send_from_directory(f'{app.static_folder}/alumbot-admin', 'index.html')


# Route for serving other static files of the 'open-kf-admin' application - keeping the original route for backward compatibility
@app.route('/open-kf-admin/<path:path>')
def serve_static_admin_original(path):
    return send_from_directory(f'{app.static_folder}/alumbot-admin', path)


# Route for the homepage of the 'open-kf-chatbot' site - keeping the original route for backward compatibility
@app.route('/open-kf-chatbot', strict_slashes=False)
def index_chatbot_original():
    return send_from_directory(f'{app.static_folder}/alumBot', 'index.html')


# Route for serving other static files of the 'open-kf-chatbot' application - keeping the original route for backward compatibility
@app.route('/open-kf-chatbot/<path:path>')
def serve_static_chatbot_original(path):
    return send_from_directory(f'{app.static_folder}/alumBot', path)


@app.route('/web/<path:filename>')
def serve_download_files(filename):
    # The file is directly located in app.static_folder (not in a subdirectory called 'web')
    file_path = safe_join(app.static_folder, filename)

    # Check if the file exists and serve it if so
    if os.path.exists(file_path) and os.path.isfile(file_path):
        # Get directory name from the filename
        dir_name = os.path.dirname(filename)
        # Get base filename from the full path
        base_filename = os.path.basename(filename)
        # Serve the file from the correct directory
        return send_from_directory(os.path.join(app.static_folder, dir_name), base_filename)
    else:
        # Return a 404 error if the file does not exist
        logger.error(f"Download file not found: {file_path}")
        return abort(404)


# Register all API routes from blueprints
app.register_blueprint(account.account_bp)
app.register_blueprint(auth.auth_bp)
app.register_blueprint(bot_config.bot_config_bp)
app.register_blueprint(common.common_bp)
app.register_blueprint(files.files_bp)
app.register_blueprint(intervention.intervention_bp)
app.register_blueprint(queries.queries_bp)
app.register_blueprint(sitemaps.sitemaps_bp)
app.register_blueprint(urls.urls_bp)

# Set up legacy API routes that redirect to the new API routes
# These are manual mappings for each endpoint to ensure proper forwarding

# Auth API
@app.route('/open_kf_api/auth/get_token', methods=['POST'])
def legacy_auth_get_token():
    logger.info("Redirecting API request from /open_kf_api/auth/get_token to /alumBot_api/auth/get_token")
    return auth.get_token()

# Account API
@app.route('/open_kf_api/account/login', methods=['POST'])
def legacy_account_login():
    logger.info("Redirecting API request from /open_kf_api/account/login to /alumBot_api/account/login")
    return account.login()

@app.route('/open_kf_api/account/update_password', methods=['POST'])
def legacy_account_update_password():
    logger.info("Redirecting API request from /open_kf_api/account/update_password to /alumBot_api/account/update_password")
    return account.update_password()

# Bot Config API
@app.route('/open_kf_api/bot_config/get_bot_setting', methods=['POST'])
def legacy_get_bot_setting():
    logger.info("Redirecting API request from /open_kf_api/bot_config/get_bot_setting to /alumBot_api/bot_config/get_bot_setting")
    return bot_config.get_bot_setting()

@app.route('/open_kf_api/bot_config/update_bot_setting', methods=['POST'])
def legacy_update_bot_setting():
    logger.info("Redirecting API request from /open_kf_api/bot_config/update_bot_setting to /alumBot_api/bot_config/update_bot_setting")
    return bot_config.update_bot_setting()

# Common API
@app.route('/open_kf_api/common/upload_picture', methods=['POST'])
def legacy_upload_picture():
    logger.info("Redirecting API request from /open_kf_api/common/upload_picture to /alumBot_api/common/upload_picture")
    return common.upload_picture()

# Queries API - most important for chatbot functionality
@app.route('/open_kf_api/queries/smart_query', methods=['POST'])
def legacy_smart_query():
    logger.info("Redirecting API request from /open_kf_api/queries/smart_query to /alumBot_api/queries/smart_query")
    return queries.smart_query()

@app.route('/open_kf_api/queries/smart_query_stream', methods=['POST'])
def legacy_smart_query_stream():
    logger.info("Redirecting API request from /open_kf_api/queries/smart_query_stream to /alumBot_api/queries/smart_query_stream")
    return queries.smart_query_stream()

@app.route('/open_kf_api/queries/get_user_conversation_list', methods=['POST'])
def legacy_get_user_conversation_list():
    logger.info("Redirecting API request from /open_kf_api/queries/get_user_conversation_list to /alumBot_api/queries/get_user_conversation_list")
    return queries.get_user_conversation_list()

@app.route('/open_kf_api/queries/get_user_query_history_list', methods=['POST'])
def legacy_get_user_query_history_list():
    logger.info("Redirecting API request from /open_kf_api/queries/get_user_query_history_list to /alumBot_api/queries/get_user_query_history_list")
    return queries.get_user_query_history_list()

# Sitemaps API
@app.route('/open_kf_api/sitemaps/get_crawl_url_list', methods=['POST'])
def legacy_get_crawl_url_list():
    logger.info("Redirecting API request from /open_kf_api/sitemaps/get_crawl_url_list to /alumBot_api/sitemaps/get_crawl_url_list")
    return sitemaps.get_crawl_url_list()

@app.route('/open_kf_api/sitemaps/submit_crawl_site', methods=['POST'])
def legacy_submit_crawl_site():
    logger.info("Redirecting API request from /open_kf_api/sitemaps/submit_crawl_site to /alumBot_api/sitemaps/submit_crawl_site")
    return sitemaps.submit_crawl_site()

# Files API
@app.route('/open_kf_api/files/get_local_file_list', methods=['POST'])
def legacy_get_local_file_list():
    logger.info("Redirecting API request from /open_kf_api/files/get_local_file_list to /alumBot_api/files/get_local_file_list")
    return files.get_local_file_list()

@app.route('/open_kf_api/files/submit_local_file_list', methods=['POST'])
def legacy_submit_local_file_list():
    logger.info("Redirecting API request from /open_kf_api/files/submit_local_file_list to /alumBot_api/files/submit_local_file_list")
    return files.submit_local_file_list()

@app.route('/open_kf_api/files/delete_local_file_list', methods=['POST'])
def legacy_delete_local_file_list():
    logger.info("Redirecting API request from /open_kf_api/files/delete_local_file_list to /alumBot_api/files/delete_local_file_list")
    return files.delete_local_file_list()

# URLs API
@app.route('/open_kf_api/urls/get_isolated_url_list', methods=['POST'])
def legacy_get_isolated_url_list():
    logger.info("Redirecting API request from /open_kf_api/urls/get_isolated_url_list to /alumBot_api/urls/get_isolated_url_list")
    return urls.get_isolated_url_list()

@app.route('/open_kf_api/urls/submit_isolated_url_list', methods=['POST'])
def legacy_submit_isolated_url_list():
    logger.info("Redirecting API request from /open_kf_api/urls/submit_isolated_url_list to /alumBot_api/urls/submit_isolated_url_list")
    return urls.submit_isolated_url_list()

@app.route('/open_kf_api/urls/delete_isolated_url_list', methods=['POST'])
def legacy_delete_isolated_url_list():
    logger.info("Redirecting API request from /open_kf_api/urls/delete_isolated_url_list to /alumBot_api/urls/delete_isolated_url_list")
    return urls.delete_isolated_url_list()

# Catch-all for any API endpoints we haven't explicitly mapped
@app.route('/open_kf_api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def legacy_api_catchall(path):
    logger.warning(f"Unmapped API request to /open_kf_api/{path} - this route isn't explicitly handled")
    return jsonify({
        "retcode": -40004, 
        "message": f"This legacy API endpoint (/open_kf_api/{path}) isn't explicitly mapped. Please use /alumBot_api/{path} instead.", 
        "data": {}
    }), 404

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=7000)

"""
Flask application demonstrating secure vs. vulnerable file serving.

This application provides two parallel implementations:
- Vulnerable endpoints that allow path traversal
- Secure endpoints that prevent path traversal

Use this to understand the vulnerability and how to fix it.
"""

import os
from flask import Flask, jsonify, abort
from fileserver import read_file_safe, read_file_vulnerable

app = Flask(__name__)

# Base directory where files are stored
FILES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fixtures'))


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})


@app.route('/vulnerable/read/<filename>')
def read_vulnerable(filename):
    """
    VULNERABLE endpoint: Susceptible to path traversal.

    This endpoint demonstrates the vulnerability. You can request:
    - /vulnerable/read/hello.txt (OK)
    - /vulnerable/read/../../../etc/passwd (VULNERABLE - may work)

    In a real application, this would be a security hole.
    """
    try:
        content = read_file_vulnerable(FILES_DIR, filename)
        return jsonify({
            'status': 'ok',
            'filename': filename,
            'content': content,
            'warning': 'This endpoint is VULNERABLE to path traversal!'
        })
    except FileNotFoundError:
        abort(404)
    except Exception as e:
        return jsonify({'error': 'Internal error'}), 500


@app.route('/secure/read/<filename>')
def read_secure(filename):
    """
    SECURE endpoint: Protected against path traversal.

    This endpoint is protected. Requests like:
    - /secure/read/hello.txt (OK)
    - /secure/read/../../../etc/passwd (BLOCKED)

    are safely blocked.
    """
    try:
        content = read_file_safe(FILES_DIR, filename)
        return jsonify({
            'status': 'ok',
            'filename': filename,
            'content': content,
            'security': 'Path traversal protection enabled'
        })
    except PermissionError:
        abort(403)
    except FileNotFoundError:
        abort(404)
    except Exception as e:
        return jsonify({'error': 'Internal error'}), 500


@app.errorhandler(403)
def forbidden(error):
    """Handle forbidden access (path traversal attempts)."""
    return jsonify({
        'error': 'Forbidden',
        'reason': 'Access denied. Path traversal detected.'
    }), 403


@app.errorhandler(404)
def not_found(error):
    """Handle not found errors."""
    return jsonify({
        'error': 'Not found',
        'reason': 'The requested file does not exist.'
    }), 404


if __name__ == '__main__':
    os.makedirs(FILES_DIR, exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=False)

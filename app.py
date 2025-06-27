from flask import Flask, render_template, request, jsonify
from backend.cracker import crack_hash, pass_strength
import time
import hashlib
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route("/", methods=["GET"])
def index():
    """Serve the main page"""
    return render_template("index.html")

@app.route("/crack", methods=["POST"])
def crack_endpoint():
    """Handle hash cracking requests"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data received"
            }), 400

        algo = data.get("algo")
        input_type = data.get("input_type", "hash")
        wordlist = "wordlist.txt"
        target_hash = None

        print(f"DEBUG: Received data: {data}")  # Debug print

        # Validate algorithm
        if algo not in ["sha256", "md5", "sha1"]:
            return jsonify({
                "success": False,
                "error": "Invalid algorithm. Supported: sha256, md5, sha1"
            }), 400

        # Process input based on type
        if input_type == "hash":
            target_hash = data.get("target_hash", "").strip()
            if not target_hash:
                return jsonify({
                    "success": False,
                    "error": "Target hash is required"
                }), 400
        elif input_type == "password":
            password = data.get("target_password", "").strip()
            if not password:
                return jsonify({
                    "success": False,
                    "error": "Target password is required"
                }), 400
                
            # Generate hash from password
            if algo == "sha256":
                target_hash = hashlib.sha256(password.encode()).hexdigest()
            elif algo == "md5":
                target_hash = hashlib.md5(password.encode()).hexdigest()
            elif algo == "sha1":
                target_hash = hashlib.sha1(password.encode()).hexdigest()
        else:
            return jsonify({
                "success": False,
                "error": "Invalid input type"
            }), 400

        print(f"DEBUG: Target hash: {target_hash}")  # Debug print

        # Perform the cracking
        start = time.time()
        found = crack_hash(target_hash, wordlist, algo)
        end = time.time()

        return jsonify({
            "success": True,
            "mode": "crack",
            "found": found,
            "time": round(end - start, 4),
            "hash": target_hash,
            "algorithm": algo.upper(),
            "input_type": input_type
        })

    except FileNotFoundError as e:
        return jsonify({
            "success": False,
            "error": f"Wordlist file not found: {str(e)}"
        }), 500
    except Exception as e:
        print(f"DEBUG: Error in crack_endpoint: {e}")  # Debug print
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500

@app.route("/check", methods=["POST"])
def check_endpoint():
    """Handle password strength checking requests"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data received"
            }), 400

        password = data.get("password", "").strip()
        algo = data.get("algo")
        wordlist = "wordlist.txt"

        print(f"DEBUG: Check password data: {data}")  # Debug print

        # Validate inputs
        if not password:
            return jsonify({
                "success": False,
                "error": "Password is required"
            }), 400

        if algo not in ["sha256", "md5", "sha1"]:
            return jsonify({
                "success": False,
                "error": "Invalid algorithm. Supported: sha256, md5, sha1"
            }), 400

        # Generate hash for display
        if algo == "sha256":
            password_hash = hashlib.sha256(password.encode()).hexdigest()
        elif algo == "md5":
            password_hash = hashlib.md5(password.encode()).hexdigest()
        elif algo == "sha1":
            password_hash = hashlib.sha1(password.encode()).hexdigest()

        # Check password strength
        strength_result = pass_strength(password, wordlist, algo)
        
        return jsonify({
            "success": True,
            "mode": "check",
            "strength": strength_result["strength"],
            "guessable": strength_result["guessable"],
            "password_hash": password_hash,
            "algorithm": algo.upper()
        })

    except FileNotFoundError as e:
        return jsonify({
            "success": False,
            "error": f"Wordlist file not found: {str(e)}"
        }), 500
    except Exception as e:
        print(f"DEBUG: Error in check_endpoint: {e}")  # Debug print
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": "Method not allowed"
    }), 405

if __name__ == "__main__":
    print("Starting HashHunt Flask App...")
    print("Available endpoints:")
    print("  GET  / - Main page")
    print("  POST /crack - Hash cracking")
    print("  POST /check - Password strength checking")
    app.run(debug=True, host='127.0.0.1', port=5000)
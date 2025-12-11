from flask import Flask, request, jsonify
import random
import time

app = Flask(__name__)

# ... existing imports ...
import datetime

# --- 5. LOGGING/SAVING TOOLS ---

# Mock database storage
incident_logs = []

@app.route('/db/save_report', methods=['POST'])
def save_report():
    """Saves the monitoring report to the database."""
    data = request.json
    
    # Extract data from Dify
    report_content = data.get('report_content', 'No content')
    severity = data.get('severity', 'unknown')
    
    # Create a record
    new_record = {
        "id": len(incident_logs) + 1,
        "timestamp": datetime.datetime.now().isoformat(),
        "severity": severity,
        "content": report_content,
        "status": "logged"
    }
    
    incident_logs.append(new_record)
    
    # In a real app, you would run: 
    # db.execute("INSERT INTO incidents (content, severity) VALUES (...)")
    
    print(f"✅ [SAVED TO DB]: {new_record}") # Print to console to prove it worked
    
    return jsonify({
        "status": "success",
        "record_id": new_record["id"],
        "message": "Report saved successfully."
    })

# ... existing app.run ...

if __name__ == '__main__':
    # Run on port 5000
    app.run(debug=True, port=5000)
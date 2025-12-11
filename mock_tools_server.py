from flask import Flask, request, jsonify
import random
import time

app = Flask(__name__)

# --- 1. DB AGENT TOOLS ---

@app.route('/db/run_query', methods=['POST'])
def run_db_query():
    """Simulates running a SQL query."""
    data = request.json
    query = data.get('query', '')
    
    # Mock Logic: If query implies checking users, return user data
    if 'users' in query.lower():
        result = [
            {"id": 1, "status": "active", "last_login": "2023-10-25"},
            {"id": 2, "status": "locked", "last_login": "2023-10-20"}
        ]
    else:
        result = {"status": "success", "message": "Query executed successfully (Mock)"}
        
    return jsonify({
        "query": query,
        "execution_time_ms": random.randint(5, 150),
        "result": result
    })

@app.route('/db/health', methods=['POST'])
def check_db_health():
    """Simulates checking DB internal health (deadlocks, file size)."""
    # Mocking random issues occasionally
    is_healthy = random.choice([True, True, False]) 
    
    if is_healthy:
        return jsonify({
            "status": "healthy",
            "deadlocks": 0,
            "response_time_avg_ms": 45,
            "file_size_gb": 102.5
        })
    else:
        return jsonify({
            "status": "abnormal",
            "deadlocks": 2,
            "response_time_avg_ms": 2500, # Slow!
            "warning": "High deadlock rate detected"
        })

# --- 2. PROMETHEUS/GRAFANA TOOLS ---

@app.route('/monitoring/metrics', methods=['POST'])
def get_metrics():
    """Simulates Prometheus fetching CPU/Memory."""
    data = request.json
    service = data.get('service_name', 'all')
    
    cpu_load = random.randint(20, 95)
    memory_usage = random.randint(40, 80)
    
    alert = "none"
    if cpu_load > 90:
        alert = "critical_cpu_load"
        
    return jsonify({
        "service": service,
        "timestamp": time.time(),
        "metrics": {
            "cpu_usage_percent": cpu_load,
            "memory_usage_percent": memory_usage,
            "active_connections": random.randint(100, 5000)
        },
        "alert_status": alert
    })

# --- 3. APM TOOLS ---

@app.route('/monitoring/apm', methods=['POST'])
def get_apm_traces():
    """Simulates APM traces for latency checks."""
    return jsonify({
        "service": "payment-gateway",
        "p95_latency_ms": random.randint(200, 1200),
        "error_rate_percent": random.uniform(0.1, 5.0),
        "recent_errors": [
            {"code": 500, "msg": "Connection timeout", "count": 12},
            {"code": 503, "msg": "Service unavailable", "count": 2}
        ]
    })

# --- 4. ORGANIZATION TOOLS ---

@app.route('/org/info', methods=['POST'])
def get_org_info():
    """Returns mock info about who owns the service."""
    return jsonify({
        "service_owner": "Team FinTech",
        "on_call_engineer": "Alice Doe",
        "slack_channel": "#fintech-alerts"
    })

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
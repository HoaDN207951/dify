from fastmcp import FastMCP
import random
import time

# Initialize the FastMCP server
mcp = FastMCP("DevOps Agent Tools")

# --- 1. DB AGENT TOOLS ---

@mcp.tool()
def run_db_query(query: str) -> dict:
    """
    Simulates running a SQL query against the database.
    
    Args:
        query: The SQL query string to execute.
    """
    # Mock Logic: If query implies checking users, return user data
    if 'users' in query.lower():
        result = [
            {"id": 1, "status": "active", "last_login": "2023-10-25"},
            {"id": 2, "status": "locked", "last_login": "2023-10-20"}
        ]
    else:
        result = {"status": "success", "message": "Query executed successfully (Mock)"}
        
    return {
        "query": query,
        "execution_time_ms": random.randint(5, 150),
        "result": result
    }

@mcp.tool()
def check_db_health() -> dict:
    """
    Simulates checking DB internal health (deadlocks, file size, response time).
    Use this to determine if the database is experiencing performance issues.
    """
    # Mocking random issues occasionally
    is_healthy = random.choice([True, True, False]) 
    
    if is_healthy:
        return {
            "status": "healthy",
            "deadlocks": 0,
            "response_time_avg_ms": 45,
            "file_size_gb": 102.5
        }
    else:
        return {
            "status": "abnormal",
            "deadlocks": 2,
            "response_time_avg_ms": 2500, # Slow!
            "warning": "High deadlock rate detected"
        }

# --- 2. PROMETHEUS/GRAFANA TOOLS ---

@mcp.tool()
def get_metrics(service_name: str = 'all') -> dict:
    """
    Simulates Prometheus fetching CPU and Memory metrics for a specific service.
    
    Args:
        service_name: The name of the service to check (default: 'all').
    """
    cpu_load = random.randint(20, 95)
    memory_usage = random.randint(40, 80)
    
    alert = "none"
    if cpu_load > 90:
        alert = "critical_cpu_load"
        
    return {
        "service": service_name,
        "timestamp": time.time(),
        "metrics": {
            "cpu_usage_percent": cpu_load,
            "memory_usage_percent": memory_usage,
            "active_connections": random.randint(100, 5000)
        },
        "alert_status": alert
    }

# --- 3. APM TOOLS ---

@mcp.tool()
def get_apm_traces() -> dict:
    """
    Simulates APM traces for latency checks and error rates.
    Useful for debugging 500 errors or slow responses.
    """
    return {
        "service": "payment-gateway",
        "p95_latency_ms": random.randint(200, 1200),
        "error_rate_percent": random.uniform(0.1, 5.0),
        "recent_errors": [
            {"code": 500, "msg": "Connection timeout", "count": 12},
            {"code": 503, "msg": "Service unavailable", "count": 2}
        ]
    }

# --- 4. ORGANIZATION TOOLS ---

@mcp.tool()
def get_org_info() -> dict:
    """
    Returns mock info about who owns the service, on-call engineers, and communication channels.
    """
    return {
        "service_owner": "Team FinTech",
        "on_call_engineer": "Alice Doe",
        "slack_channel": "#fintech-alerts"
    }

if __name__ == '__main__':
    # Starts the server over Stdio (standard input/output) by default
    mcp.run(transport="sse")
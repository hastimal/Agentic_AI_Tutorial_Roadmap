import datetime

def get_current_time() -> str:
    """Retrieves the current date and time in ISO format.
    
    Returns:
        A string representation of the current datetime.
    """
    return datetime.datetime.now().isoformat()

def fetch_mock_system_status(service_name: str) -> str:
    """Queries and retrieves simulated system status, resource utilization, and health metrics.
    
    Args:
        service_name: The name of the service to query (e.g. 'database', 'auth', 'cache').
    
    Returns:
        A status summary string.
    """
    name_lower = service_name.lower()
    if "db" in name_lower or "database" in name_lower:
        return "Database: HEALTHY | CPU Usage: 14% | Active Connections: 42 | Replication Lag: 2ms"
    elif "auth" in name_lower:
        return "Auth Service: HEALTHY | Latency: 12ms | Token Issuance Rate: 8.5/s"
    elif "cache" in name_lower or "redis" in name_lower:
        return "Cache Service: HEALTHY | Memory Usage: 320MB/1GB | Hit Rate: 94.2%"
    else:
        return f"Service '{service_name}': UNKNOWN | Status: Operational (Default fallback)"

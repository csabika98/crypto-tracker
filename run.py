#!/usr/bin/env python3
"""
Service Orchestrator
"""
import threading
import time
import sys
from pathlib import Path
import subprocess

PROJECT_ROOT = Path(__file__).parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"

def run_init_db():
    """Initialize database"""
    print("Initializing database...")
    from backend.database.init_db import init_database
    init_database()
    print()

def run_collector():
    """Run data collector"""
    print("Starting data collector...")
    from backend.collector.main import main as collector_main
    collector_main()

def run_api():
    """Run API server"""
    print("Starting API server...")
    import uvicorn
    from backend.api.main import app
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
def run_frontend():
    """Run Next.js frontend"""
    print("Starting frontend...")
    subprocess.run(["npm", "run", "dev"], cwd=FRONTEND_DIR)

def main():
    print("="*50)
    print("CRYPTO TRACKER")
    print("="*50)
    print()
    
    run_init_db()
    
    collector_thread = threading.Thread(target=run_collector, daemon=True)
    collector_thread.start()
    print("Collector running in background")
    print()
    
 
    time.sleep(2)
    
    print("="*50)
    print("ALL SERVICES RUNNING")
    print("="*50)
    print()
    print("API: http://localhost:8000")
    print("Docs: http://localhost:8000/docs")
    print()
    print("Press Ctrl+C to stop")
    print()
    
    try:
        run_api()
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        sys.exit(0)

if __name__ == "__main__":
    main()

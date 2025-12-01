"""
Alembic Migration Sync Script
Syncs migration files from Docker container to local filesystem
"""

import subprocess
import time
import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

CONTAINER_NAME = "fastapi_app"
CONTAINER_MIGRATIONS_PATH = "/code/alembic/versions"
LOCAL_MIGRATIONS_PATH = "./alembic/versions"

class MigrationSyncHandler(FileSystemEventHandler):
    def __init__(self, container_name, container_path, local_path):
        self.container_name = container_name
        self.container_path = container_path
        self.local_path = local_path
        
    def sync_from_container(self):
        try:
            # Create local directory if it doesn't exist
            Path(self.local_path).mkdir(parents=True, exist_ok=True)
            # Copy files from container
            cmd = [
                "docker", "cp",
                f"{self.container_name}:{self.container_path}/.",
                self.local_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Synced migrations from container to {self.local_path}")
                return True
            else:
                print(f"❌ Error syncing: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Exception during sync: {e}")
            return False

def check_container_running(container_name):
    try:
        cmd = ["docker", "ps", "--filter", f"name={container_name}", "--format", "{{.Names}}"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return container_name in result.stdout
    except Exception as e:
        print(f"❌ Error checking container: {e}")
        return False

def list_container_migrations(container_name, container_path):
    try:
        cmd = ["docker", "exec", container_name, "ls", "-la", container_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        return None
    except Exception as e:
        print(f"❌ Error listing migrations: {e}")
        return None

def watch_and_sync(interval=5):
    print(f"🔍 Starting migration sync watcher...")
    print(f"📦 Container: {CONTAINER_NAME}")
    print(f"📂 Local path: {LOCAL_MIGRATIONS_PATH}")
    print(f"⏱️  Check interval: {interval} seconds")
    print("-" * 50)
    
    handler = MigrationSyncHandler(
        CONTAINER_NAME,
        CONTAINER_MIGRATIONS_PATH,
        LOCAL_MIGRATIONS_PATH
    )
    last_sync = None 
    while True:
        try:
            if not check_container_running(CONTAINER_NAME):
                print(f"⚠️  Container '{CONTAINER_NAME}' is not running. Waiting...")
                time.sleep(interval)
                continue
            
            # Get current state of migrations in container
            current_state = list_container_migrations(
                CONTAINER_NAME,
                CONTAINER_MIGRATIONS_PATH
            )
            
            # If state changed, sync
            if current_state and current_state != last_sync:
                print(f"\n🔄 Changes detected in container migrations...")
                if handler.sync_from_container():
                    last_sync = current_state
                    print(f"✨ Sync completed at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print(f"✓ No changes detected ({time.strftime('%H:%M:%S')})", end="\r")
            
            time.sleep(interval)
            
        except KeyboardInterrupt:
            print("\n\n👋 Stopping migration sync watcher...")
            break
        except Exception as e:
            print(f"\n❌ Error in watch loop: {e}")
            time.sleep(interval)


if __name__ == "__main__":
    watch_and_sync(interval=5)
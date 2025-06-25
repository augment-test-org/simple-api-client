#!/usr/bin/env python3
"""
Setup script for the API client environment.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False

def check_python():
    """Check if Python 3 is available."""
    try:
        version = subprocess.check_output([sys.executable, "--version"], text=True).strip()
        print(f"✅ Python found: {version}")
        return True
    except Exception as e:
        print(f"❌ Python check failed: {e}")
        return False

def setup_virtual_environment():
    """Create and activate virtual environment."""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    return run_command(f"{sys.executable} -m venv venv", "Creating virtual environment")

def install_dependencies():
    """Install required packages."""
    if os.name == 'nt':  # Windows
        pip_path = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        pip_path = "venv/bin/pip"
    
    return run_command(f"{pip_path} install -r requirements.txt", "Installing dependencies")

def create_config_files():
    """Create configuration files from examples."""
    files_created = []
    
    # Create .env file if it doesn't exist
    if not Path(".env").exists() and Path(".env.example").exists():
        run_command("cp .env.example .env", "Creating .env file")
        files_created.append(".env")
    
    # Create token.txt file if it doesn't exist
    if not Path("token.txt").exists() and Path("token.txt.example").exists():
        run_command("cp token.txt.example token.txt", "Creating token.txt file")
        files_created.append("token.txt")
    
    if files_created:
        print(f"📝 Created configuration files: {', '.join(files_created)}")
        print("⚠️  Please edit these files with your actual values!")
    
    return True

def main():
    """Main setup function."""
    print("🚀 Setting up API Client Environment")
    print("=" * 50)
    
    # Check Python
    if not check_python():
        sys.exit(1)
    
    # Setup virtual environment
    if not setup_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create config files
    create_config_files()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit 'token.txt' with your actual bearer token")
    print("2. Edit '.env' with your API base URL")
    
    if os.name == 'nt':  # Windows
        print("3. Activate virtual environment: venv\\Scripts\\activate")
    else:  # Unix/Linux/macOS
        print("3. Activate virtual environment: source venv/bin/activate")
    
    print("4. Run the API client: python api_client.py")

if __name__ == "__main__":
    main()

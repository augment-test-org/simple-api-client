# Simple Python API Client

This repository contains a simple Python script for making API calls with bearer token authentication. The token is read from a local file for security.

### Quick Setup

1. **Run the setup script:**
   ```bash
   python setup.py
   ```

2. **Edit configuration files:**
   - Edit `token.txt` with your actual bearer token
   - Edit `.env` with your API base URL

3. **Activate virtual environment:**
   ```bash
   # On Linux/macOS
   source venv/bin/activate

   # On Windows
   venv\Scripts\activate
   ```

4. **Run the API client:**
   ```bash
   python api_client.py
   ```

### Manual Setup

If you prefer to set up manually:

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create configuration files:**
   ```bash
   cp .env.example .env
   cp token.txt.example token.txt
   ```

4. **Edit the files with your actual values**

### Usage

The `APIClient` class supports GET, POST, PUT, and DELETE requests:

```python
from api_client import APIClient

# Initialize client
client = APIClient(token_file="token.txt", base_url="https://api.example.com")

# Make requests
response = client.get("/api/users")
response = client.post("/api/users", json_data={"name": "John"})
response = client.put("/api/users/1", json_data={"name": "Jane"})
response = client.delete("/api/users/1")
```

### Testing

Run the test suite to verify everything works:

```bash
python test_api_client.py
```

### Files

- `api_client.py` - Main API client script
- `setup.py` - Automated setup script
- `test_api_client.py` - Test suite
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template
- `token.txt.example` - Token file template

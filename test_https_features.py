#!/usr/bin/env python3
"""
Test HTTPS features
"""
import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings for self-signed certificate
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

def test_https():
    print("🔐 Testing HTTPS Features")
    print("=" * 40)
    
    try:
        # Test the home page with SSL
        response = requests.get('https://localhost:8443', verify=False)
        
        print(f"✅ HTTPS Connection Successful")
        print(f"Status Code: {response.status_code}")
        print(f"URL: {response.url}")
        
        # Check security headers
        security_headers = [
            'X-Content-Type-Options',
            'X-Frame-Options', 
            'X-XSS-Protection',
            'Content-Security-Policy'
        ]
        
        print("\n🔒 Security Headers:")
        for header in security_headers:
            value = response.headers.get(header, 'Not set')
            print(f"  {header}: {value}")
            
    except Exception as e:
        print(f"❌ HTTPS Test Failed: {e}")
        print("Make sure the server is running on https://localhost:8443")

if __name__ == '__main__':
    test_https()

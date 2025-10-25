"""
Diagnostic script to check OAuth configuration
"""
import json
import os

def check_client_secret():
    """Check client_secret.json configuration"""
    client_secret_path = 'client_secret.json'
    
    if not os.path.exists(client_secret_path):
        print("❌ client_secret.json not found!")
        return
    
    print("✅ client_secret.json exists")
    
    try:
        with open(client_secret_path, 'r') as f:
            data = json.load(f)
        
        # Check structure
        if 'web' in data:
            client_type = 'web'
            config = data['web']
        elif 'installed' in data:
            client_type = 'installed'
            config = data['installed']
        else:
            print("❌ Unknown client type in client_secret.json")
            return
        
        print(f"\n📋 Client Configuration:")
        print(f"   Type: {client_type}")
        print(f"   Client ID: {config.get('client_id', 'NOT FOUND')[:50]}...")
        print(f"   Auth URI: {config.get('auth_uri', 'NOT FOUND')}")
        print(f"   Token URI: {config.get('token_uri', 'NOT FOUND')}")
        
        # Check redirect URIs
        redirect_uris = config.get('redirect_uris', [])
        print(f"\n🔗 Configured Redirect URIs in client_secret.json:")
        for uri in redirect_uris:
            print(f"   - {uri}")
        
        print(f"\n🎯 Expected Redirect URI for your app:")
        print(f"   - http://127.0.0.1:8000/oauth2callback/")
        print(f"   - http://localhost:8000/oauth2callback/")
        
        # Check if expected URIs are in the list
        expected_uris = [
            'http://127.0.0.1:8000/oauth2callback/',
            'http://localhost:8000/oauth2callback/'
        ]
        
        missing_uris = [uri for uri in expected_uris if uri not in redirect_uris]
        
        if missing_uris:
            print(f"\n⚠️  ISSUE FOUND: Missing redirect URIs!")
            print(f"   You need to add these URIs to your Google Cloud Console:")
            for uri in missing_uris:
                print(f"   - {uri}")
            print(f"\n📝 Steps to fix:")
            print(f"   1. Go to: https://console.cloud.google.com/apis/credentials")
            print(f"   2. Click on your OAuth 2.0 Client ID")
            print(f"   3. Add the missing URIs to 'Authorized redirect URIs'")
            print(f"   4. Click 'Save'")
        else:
            print(f"\n✅ All expected redirect URIs are configured!")
        
        # Check client type recommendation
        if client_type == 'installed':
            print(f"\n⚠️  WARNING: You're using 'installed' app credentials")
            print(f"   For a Django web app, you should use 'Web application' credentials")
            print(f"\n📝 Steps to fix:")
            print(f"   1. Go to: https://console.cloud.google.com/apis/credentials")
            print(f"   2. Create new OAuth 2.0 Client ID")
            print(f"   3. Select 'Web application' as the application type")
            print(f"   4. Add redirect URIs:")
            print(f"      - http://127.0.0.1:8000/oauth2callback/")
            print(f"      - http://localhost:8000/oauth2callback/")
            print(f"   5. Download the new client_secret.json")
            print(f"   6. Replace your current client_secret.json")
        
    except json.JSONDecodeError:
        print("❌ client_secret.json is not valid JSON!")
    except Exception as e:
        print(f"❌ Error reading client_secret.json: {e}")

if __name__ == "__main__":
    print("🔍 OAuth Configuration Checker\n")
    print("=" * 60)
    check_client_secret()
    print("=" * 60)

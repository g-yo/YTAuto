"""
Quick verification script to check OAuth setup
Run this before attempting OAuth flow
"""
import json
import os
import sys

def verify_setup():
    """Verify OAuth setup is correct"""
    print("🔍 Verifying OAuth Setup\n")
    print("=" * 70)
    
    issues = []
    warnings = []
    
    # Check 1: client_secret.json exists
    print("\n1️⃣  Checking client_secret.json...")
    if not os.path.exists('client_secret.json'):
        issues.append("❌ client_secret.json not found!")
        print("   ❌ NOT FOUND")
    else:
        print("   ✅ Found")
        
        # Check 2: Valid JSON
        print("\n2️⃣  Checking JSON validity...")
        try:
            with open('client_secret.json', 'r') as f:
                data = json.load(f)
            print("   ✅ Valid JSON")
            
            # Check 3: Client type
            print("\n3️⃣  Checking client type...")
            if 'web' in data:
                print("   ✅ Web application (correct)")
                config = data['web']
            elif 'installed' in data:
                print("   ⚠️  Installed application")
                warnings.append("You're using 'installed' app credentials. For Django, use 'Web application'")
                config = data['installed']
            else:
                print("   ❌ Unknown client type")
                issues.append("Unknown client type in client_secret.json")
                config = {}
            
            # Check 4: Required fields
            print("\n4️⃣  Checking required fields...")
            required_fields = ['client_id', 'client_secret', 'auth_uri', 'token_uri']
            for field in required_fields:
                if field in config:
                    print(f"   ✅ {field}")
                else:
                    print(f"   ❌ {field} missing")
                    issues.append(f"Missing {field} in client_secret.json")
            
            # Check 5: Redirect URIs
            print("\n5️⃣  Checking redirect URIs...")
            redirect_uris = config.get('redirect_uris', [])
            expected_uri = 'http://127.0.0.1:8000/oauth2callback/'
            
            if expected_uri in redirect_uris:
                print(f"   ✅ {expected_uri}")
            else:
                print(f"   ⚠️  {expected_uri} not in client_secret.json")
                warnings.append(f"Add {expected_uri} to redirect URIs in Google Cloud Console")
            
            # Check 6: Client ID format
            print("\n6️⃣  Checking client ID format...")
            client_id = config.get('client_id', '')
            if client_id.endswith('.apps.googleusercontent.com'):
                print(f"   ✅ Valid format")
                print(f"   📋 Client ID: {client_id[:50]}...")
            else:
                print(f"   ⚠️  Unusual client ID format")
                warnings.append("Client ID doesn't match expected format")
            
        except json.JSONDecodeError as e:
            print(f"   ❌ Invalid JSON: {e}")
            issues.append("client_secret.json is not valid JSON")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            issues.append(f"Error reading client_secret.json: {e}")
    
    # Check 7: Django settings
    print("\n7️⃣  Checking Django configuration...")
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_shorts_app.settings')
        django.setup()
        
        from django.conf import settings
        
        if hasattr(settings, 'YOUTUBE_CLIENT_SECRETS_FILE'):
            print(f"   ✅ YOUTUBE_CLIENT_SECRETS_FILE configured")
        else:
            print(f"   ❌ YOUTUBE_CLIENT_SECRETS_FILE not in settings")
            issues.append("YOUTUBE_CLIENT_SECRETS_FILE not configured in settings.py")
        
        if hasattr(settings, 'YOUTUBE_SCOPES'):
            print(f"   ✅ YOUTUBE_SCOPES configured")
        else:
            print(f"   ❌ YOUTUBE_SCOPES not in settings")
            issues.append("YOUTUBE_SCOPES not configured in settings.py")
            
    except Exception as e:
        print(f"   ⚠️  Could not verify Django settings: {e}")
        warnings.append("Could not verify Django settings")
    
    # Summary
    print("\n" + "=" * 70)
    print("\n📊 SUMMARY\n")
    
    if not issues and not warnings:
        print("✅ All checks passed! Your OAuth setup looks good.")
        print("\n📝 Next steps:")
        print("   1. Make sure you've added the redirect URI in Google Cloud Console:")
        print("      https://console.cloud.google.com/apis/credentials")
        print("   2. Verify the redirect URI is: http://127.0.0.1:8000/oauth2callback/")
        print("   3. Restart your Django server")
        print("   4. Try the OAuth flow again")
        return True
    
    if warnings:
        print("⚠️  WARNINGS:")
        for warning in warnings:
            print(f"   • {warning}")
        print()
    
    if issues:
        print("❌ ISSUES FOUND:")
        for issue in issues:
            print(f"   • {issue}")
        print("\n📝 Please fix these issues before proceeding.")
        print("   See OAUTH_FIX_GUIDE.md for detailed instructions.")
        return False
    
    return True

if __name__ == "__main__":
    success = verify_setup()
    sys.exit(0 if success else 1)

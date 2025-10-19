# PowerShell Script to upload cookies.txt to EC2 instance
# Usage: .\upload_cookies_to_ec2.ps1

# ============ CONFIGURATION - UPDATE THESE VALUES ============
$EC2_USER = "ubuntu"                                    # EC2 username (ubuntu, ec2-user, etc.)
$EC2_HOST = "your-ec2-ip-or-hostname"                  # EC2 public IP or hostname
$EC2_KEY = "path\to\your-key.pem"                      # Path to your EC2 SSH key
$PROJECT_PATH = "/home/ubuntu/YtAut"                   # Project path on EC2
# ==============================================================

Write-Host "`n🚀 YouTube Cookies Upload to EC2`n" -ForegroundColor Yellow

# Check if cookies.txt exists locally
if (-Not (Test-Path "cookies\cookies.txt")) {
    Write-Host "❌ Error: cookies\cookies.txt not found!" -ForegroundColor Red
    Write-Host "`nPlease export your YouTube cookies first:" -ForegroundColor Yellow
    Write-Host "1. Install browser extension 'Get cookies.txt LOCALLY'"
    Write-Host "2. Go to youtube.com (make sure you're logged in)"
    Write-Host "3. Click the extension and export cookies"
    Write-Host "4. Save to cookies\cookies.txt"
    exit 1
}

Write-Host "✅ Found cookies.txt locally" -ForegroundColor Green

# Check if SSH key exists
if (-Not (Test-Path $EC2_KEY)) {
    Write-Host "❌ Error: SSH key not found at $EC2_KEY" -ForegroundColor Red
    Write-Host "Please update EC2_KEY variable in this script" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n📤 Uploading cookies to EC2...`n" -ForegroundColor Yellow

# Check if using WSL or native Windows SSH
$useWSL = $false
if (Get-Command wsl -ErrorAction SilentlyContinue) {
    $response = Read-Host "Use WSL for upload? (Y/n)"
    if ($response -eq "" -or $response -eq "Y" -or $response -eq "y") {
        $useWSL = $true
    }
}

try {
    if ($useWSL) {
        # Convert Windows path to WSL path
        $wslCookiesPath = wsl wslpath -a "cookies\cookies.txt"
        $wslKeyPath = wsl wslpath -a $EC2_KEY
        
        # Create cookies directory on EC2
        wsl ssh -i $wslKeyPath "$EC2_USER@$EC2_HOST" "mkdir -p $PROJECT_PATH/cookies"
        
        # Upload cookies.txt
        wsl scp -i $wslKeyPath $wslCookiesPath "$EC2_USER@$EC2_HOST`:$PROJECT_PATH/cookies/"
    }
    else {
        # Using Windows native SSH (requires OpenSSH)
        # Create cookies directory on EC2
        ssh -i $EC2_KEY "$EC2_USER@$EC2_HOST" "mkdir -p $PROJECT_PATH/cookies"
        
        # Upload cookies.txt
        scp -i $EC2_KEY "cookies\cookies.txt" "$EC2_USER@$EC2_HOST`:$PROJECT_PATH/cookies/"
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ Cookies uploaded successfully!" -ForegroundColor Green
        Write-Host "🎉 Your EC2 instance can now download YouTube videos" -ForegroundColor Green
        Write-Host "`nNext steps:" -ForegroundColor Yellow
        Write-Host "1. SSH into your EC2 instance"
        Write-Host "2. Verify cookies file: ls -la $PROJECT_PATH/cookies/"
        Write-Host "3. Run your Django app and test video download"
    }
    else {
        throw "Upload failed"
    }
}
catch {
    Write-Host "`n❌ Upload failed. Please check:" -ForegroundColor Red
    Write-Host "  - EC2 instance is running and accessible"
    Write-Host "  - SSH key has correct permissions (chmod 400 on Linux)"
    Write-Host "  - EC2_USER, EC2_HOST, and EC2_KEY are correct"
    Write-Host "  - Security group allows SSH (port 22)"
    exit 1
}

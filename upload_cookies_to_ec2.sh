#!/bin/bash
# Script to upload cookies.txt to EC2 instance
# Usage: ./upload_cookies_to_ec2.sh

# Configuration - UPDATE THESE VALUES
EC2_USER="ubuntu"                                    # EC2 username (ubuntu, ec2-user, etc.)
EC2_HOST="your-ec2-ip-or-hostname"                  # EC2 public IP or hostname
EC2_KEY="path/to/your-key.pem"                      # Path to your EC2 SSH key
PROJECT_PATH="/home/ubuntu/YtAut"                   # Project path on EC2

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🚀 YouTube Cookies Upload to EC2${NC}\n"

# Check if cookies.txt exists locally
if [ ! -f "cookies/cookies.txt" ]; then
    echo -e "${RED}❌ Error: cookies/cookies.txt not found!${NC}"
    echo -e "${YELLOW}Please export your YouTube cookies first:${NC}"
    echo "1. Install browser extension 'Get cookies.txt LOCALLY'"
    echo "2. Go to youtube.com (logged in)"
    echo "3. Export cookies and save to cookies/cookies.txt"
    exit 1
fi

echo -e "${GREEN}✅ Found cookies.txt locally${NC}"

# Check if SSH key exists
if [ ! -f "$EC2_KEY" ]; then
    echo -e "${RED}❌ Error: SSH key not found at $EC2_KEY${NC}"
    echo "Please update EC2_KEY variable in this script"
    exit 1
fi

echo -e "${YELLOW}📤 Uploading cookies to EC2...${NC}"

# Create cookies directory on EC2 if it doesn't exist
ssh -i "$EC2_KEY" "$EC2_USER@$EC2_HOST" "mkdir -p $PROJECT_PATH/cookies"

# Upload cookies.txt
scp -i "$EC2_KEY" cookies/cookies.txt "$EC2_USER@$EC2_HOST:$PROJECT_PATH/cookies/"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Cookies uploaded successfully!${NC}"
    echo -e "${GREEN}🎉 Your EC2 instance can now download YouTube videos${NC}"
else
    echo -e "${RED}❌ Upload failed. Check your EC2 credentials and connection.${NC}"
    exit 1
fi

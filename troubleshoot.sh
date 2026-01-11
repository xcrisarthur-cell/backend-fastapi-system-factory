#!/bin/bash

echo "========================================================"
echo "Matrix Deployment Troubleshooter"
echo "========================================================"

echo -e "\n1. Checking if Nginx is running..."
if systemctl is-active --quiet nginx; then
    echo "[OK] Nginx is running"
else
    echo "[ERROR] Nginx is NOT running"
    echo "Try running: sudo systemctl start nginx"
fi

echo -e "\n2. Checking if Port 1101 is listening..."
if ss -tulpn | grep :1101 > /dev/null; then
    echo "[OK] Port 1101 is OPEN and listening"
else
    echo "[ERROR] Port 1101 is NOT listening"
    echo "Possible causes:"
    echo "  - Nginx config not linked to sites-enabled"
    echo "  - Nginx not restarted"
    echo "  - Config syntax error"
fi

echo -e "\n3. Checking Nginx Configuration Syntax..."
sudo nginx -t

echo -e "\n4. Checking Firewall (UFW)..."
if command -v ufw > /dev/null; then
    sudo ufw status | grep 1101
else
    echo "UFW not installed (skipping)"
fi

echo -e "\n5. Checking Docker Containers..."
# Navigate to directory if possible, or just list all
sudo docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep matrix

echo -e "\n6. Checking Local Backend Connection (from inside server)..."
if curl -s http://127.0.0.1:8000/health > /dev/null; then
    echo "[OK] Backend is reachable locally at 127.0.0.1:8000"
else
    echo "[ERROR] Cannot reach backend locally at 127.0.0.1:8000"
    echo "Check if Docker container is running and ports are mapped correctly."
fi

echo -e "\n========================================================"
echo "SUGGESTED FIXES:"
echo "1. If Port 1101 is not listening:"
echo "   Run: sudo ln -sf /etc/nginx/sites-available/matrix_backend_api /etc/nginx/sites-enabled/"
echo "   Run: sudo systemctl restart nginx"
echo ""
echo "2. If UFW is active but 1101 is missing:"
echo "   Run: sudo ufw allow 1101/tcp"
echo ""
echo "3. If everything looks OK but still can't connect:"
echo "   Check your VPS Provider's Firewall (AWS Security Group / DigitalOcean Firewall / etc)"
echo "   Ensure Inbound Traffic for Port 1101 is allowed."
echo "========================================================"

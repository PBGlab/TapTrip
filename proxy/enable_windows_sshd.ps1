# PowerShell：一鍵啟用 Windows 10/11 內建 OpenSSH Server

Write-Host "🔐 啟用 Windows SSH Server 中..."
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'

# 確認防火牆已開放 Port 22
Write-Host "🧱 設定防火牆規則（允許 22 port）..."
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22

Write-Host "✅ OpenSSH Server 已啟用完成！"
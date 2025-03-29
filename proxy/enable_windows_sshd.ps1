# PowerShell：自動安裝 & 啟用 Windows 10/11 內建 OpenSSH Server
# 適用情境：第一次換電腦時直接一鍵處理完

# 檢查 OpenSSH Server 是否已安裝
$capability = Get-WindowsCapability -Online | Where-Object { $_.Name -like 'OpenSSH.Server*' }

if ($capability.State -ne 'Installed') {
    Write-Host "📦 尚未安裝 OpenSSH Server，開始安裝中..."
    Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

    Write-Host "✅ 安裝完成，繼續啟用服務..."
} else {
    Write-Host "✅ 已經安裝 OpenSSH Server，跳過安裝"
}

# 啟動 sshd 服務
Write-Host "🔐 啟動 Windows SSH Server..."
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'

# 確認防火牆已開放 Port 22
Write-Host "🧱 設定防火牆規則（允許 22 port）..."
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22 -ErrorAction SilentlyContinue

Write-Host "🎉 OpenSSH Server 已啟用完成，可以讓 EC2 連回這台電腦了！"

# TapTrip 本地代理腳本工具

這是用於在「本地電腦」執行 SOCKS5 Proxy，讓 EC2 爬蟲能透過你家 IP 執行的工具。

---

## 🛠 功能說明

| 檔案                    | 說明                                 |
|-------------------------|--------------------------------------|
| `local_proxy_setup.sh`     | 啟動 SOCKS5 Proxy（EC2 會連這台）        |
| `enable_windows_sshd.ps1`  | 啟用 Windows 內建 OpenSSH Server 功能     |

---

## 🔁 多機同步使用說明（本地 + EC2）

1. 開 VS Code 的「本地資料夾」
2. 開一個終端機，執行：
   ```bash
   bash proxy/local_proxy_setup.sh.
3.個 VS Code 連接 EC2，執行：
    bash proxy_tunnel.sh
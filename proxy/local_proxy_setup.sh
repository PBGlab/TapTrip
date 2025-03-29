#!/bin/bash
# 啟動本地 SOCKS5 Proxy（在家用機器執行）
# 讓 EC2 透過這台電腦的 IP 上網

PORT=1080

echo "✅ 啟動本地 SOCKS5 Proxy（PORT: $PORT）"
ssh -D $PORT -N -q localhost


#jack
#ssh -D 1080 style@210.209.244.174
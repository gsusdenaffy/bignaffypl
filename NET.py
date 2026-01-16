# Get your network info
ipconfig

# Ping sweep scan
Write-Host "`nScanning network..." -ForegroundColor Yellow

$network = "192.168.1"
1..254 | ForEach-Object {
    $ip = "$network.$_"
    $ping = Test-Connection -ComputerName $ip -Count 1 -Quiet -ErrorAction SilentlyContinue
    
    if ($ping) {
        try {
            $hostname = [System.Net.Dns]::GetHostEntry($ip).HostName
        } catch {
            $hostname = "Unknown"
        }
        Write-Host "Found: $ip - $hostname" -ForegroundColor Green
    }
}

Write-Host "`nScan complete!" -ForegroundColor Cyan
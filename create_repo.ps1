# Create new GitHub repo and push
$ghExe = "$env:TEMP\gh\bin\gh.exe"
$workDir = "C:\Users\Administrator\7226-hk-backtest-strategy"

Set-Location $workDir

Write-Host "Creating GitHub repo '7226-hk-backtest-strategy'..."
& $ghExe repo create 7226-hk-backtest-strategy --public --source=. --push --description "7226.HK Stock Backtest Strategy & Correlation Analysis"

Write-Host "Done!"
# Roda os testes de paridade desktop x smartphone (tests/paridade_mobile.js) e a auditoria de acessibilidade (tests/acessibilidade.js).
# Uso (na pasta do repositorio):  powershell -File source\portal\tests\rodar_testes_mobile.ps1
# Requer: http-server e playwright-cli globais; o site ja montado em .\site
$ErrorActionPreference = "Stop"
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
$srv = Start-Process -FilePath "cmd.exe" -ArgumentList "/c","http-server `"$repo\site`" -p 8793 -a 127.0.0.1 -c-1 --silent" -PassThru -WindowStyle Hidden
Start-Sleep 4
$code = 0
try {
  playwright-cli open http://127.0.0.1:8793/ | Out-Null

  $out = playwright-cli --raw run-code --filename="$PSScriptRoot\paridade_mobile.js" | Select-Object -Last 1
  $r = ($out | ConvertFrom-Json) | ConvertFrom-Json
  if ($r.ok) { Write-Host "OK: paridade desktop x celular ($($r.perfis -join ', '))" -ForegroundColor Green }
  else { Write-Host "FALHAS DE PARIDADE ($($r.falhas.Count)):" -ForegroundColor Red; $r.falhas | ForEach-Object { Write-Host " - $_" }; $code = 1 }
  if ($r.avisos.Count) { Write-Host "Avisos:"; $r.avisos | ForEach-Object { Write-Host " ~ $_" } }

  $out2 = playwright-cli --raw run-code --filename="$PSScriptRoot\acessibilidade.js" | Select-Object -Last 1
  $a = ($out2 | ConvertFrom-Json) | ConvertFrom-Json
  if ($a.ok) { Write-Host "OK: acessibilidade (nomes para leitores de tela) sem pendencias" -ForegroundColor Green }
  else { Write-Host "ACESSIBILIDADE ($($a.total)):" -ForegroundColor Red; $a.problemas | ForEach-Object { Write-Host " - $_" }; $code = 1 }

  playwright-cli close | Out-Null
} finally {
  Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match "http-server" -and $_.CommandLine -match "8793" } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
}
exit $code

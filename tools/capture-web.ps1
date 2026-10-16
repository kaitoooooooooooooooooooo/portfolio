# Captures des démos web (Chrome sans fenêtre, profil temporaire) → previews-src\raw\<nom>.png
#   powershell -ExecutionPolicy Bypass -File tools\capture-web.ps1 [nom ...]
# Les captures brutes sont ensuite passées en noir et blanc par tools\make-previews.py.
param([string[]]$Only)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$raw = Join-Path $root 'previews-src\raw'
$profile = Join-Path $root 'previews-src\chrome'
New-Item -ItemType Directory -Force $raw, $profile | Out-Null
$chrome = @('C:\Program Files\Google\Chrome\Application\chrome.exe', 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe') | Where-Object { Test-Path $_ } | Select-Object -First 1
$u = 'https://kaitoooooooooooooooooooo.github.io'

# nom, adresse, taille de fenêtre, temps laissé à la page pour se charger (ms)
$shots = @(
  @('nova-strike', "$u/Nova-Strike/", '1280,800', 6000),
  @('crypto-widget', "$u/cryptoTrackerWidget/", '1280,800', 10000),
  @('countdown-widget', "$u/CountdownWidget.github.io/", '1280,800', 4000),
  @('3d-viewer', "$u/3dview.github.io/", '1280,800', 9000)
)
foreach ($s in $shots) {
  if ($Only -and $s[0] -notin $Only) { continue }
  $out = Join-Path $raw "$($s[0]).png"
  $args = @('--headless=new', '--hide-scrollbars', '--no-first-run', '--no-default-browser-check', "--user-data-dir=$profile",
    '--use-angle=swiftshader', '--enable-unsafe-swiftshader', "--window-size=$($s[2])", '--force-device-scale-factor=2',
    "--virtual-time-budget=$($s[3])", "--screenshot=$out", $s[1])
  Start-Process -FilePath $chrome -ArgumentList $args -Wait -WindowStyle Hidden -RedirectStandardError (Join-Path $profile 'err.txt')
  if (Test-Path $out) { "$($s[0]) : $([math]::Round((Get-Item $out).Length / 1KB)) Ko" } else { "$($s[0]) : ÉCHEC" }
}

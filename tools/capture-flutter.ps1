# Captures d'écran d'une application Flutter compilée pour le web, au format téléphone.
#   powershell -ExecutionPolicy Bypass -File tools\capture-flutter.ps1 -Web <dossier build\web> -Name bookedo -Routes "/","/#/list"
# Largeur 500 px : Chrome n'accepte pas de fenêtre plus étroite (sinon l'appli est coupée à droite).
# Sert le dossier sur un port local le temps des captures → previews-src\raw\<nom>-1.png, -2.png…
param(
  [Parameter(Mandatory)] [string]$Web,
  [Parameter(Mandatory)] [string]$Name,
  [Parameter(Mandatory)] [string[]]$Routes,
  [int]$Port = 5199,
  [int]$Wait = 9000
)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$raw = Join-Path $root 'previews-src\raw'
$profile = Join-Path $root 'previews-src\chrome'
New-Item -ItemType Directory -Force $raw, $profile | Out-Null
$chrome = @('C:\Program Files\Google\Chrome\Application\chrome.exe', 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe') | Where-Object { Test-Path $_ } | Select-Object -First 1
# -File accepte "a,b" en une seule chaîne : on redécoupe.
$Routes = $Routes | ForEach-Object { $_ -split ',' } | Where-Object { $_ }

$server = Start-Process -FilePath 'php' -ArgumentList @('-S', "127.0.0.1:$Port", '-t', $Web) -PassThru -WindowStyle Hidden
try {
  Start-Sleep -Milliseconds 800
  $i = 0
  foreach ($r in $Routes) {
    $i++
    $out = Join-Path $raw "$Name-$i.png"
    $args = @('--headless=new', '--hide-scrollbars', '--no-first-run', '--no-default-browser-check', "--user-data-dir=$profile",
      '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--window-size=500,1000', '--force-device-scale-factor=2',
      "--virtual-time-budget=$Wait", "--screenshot=$out", "http://127.0.0.1:$Port$r")
    Start-Process -FilePath $chrome -ArgumentList $args -Wait -WindowStyle Hidden -RedirectStandardError (Join-Path $profile 'err.txt')
    if (Test-Path $out) { "$Name-$i ($r) : $([math]::Round((Get-Item $out).Length / 1KB)) Ko" } else { "$Name-$i ($r) : ÉCHEC" }
  }
} finally {
  Stop-Process -Id $server.Id -Force -ErrorAction SilentlyContinue
}

# Crée dist\portfolio.zip, à extraire à la racine de kaito-lab.ch : le portfolio (site\) et
# l'application Recto, prise dans son propre dépôt (..\Recto\site), sous recto\.
#   powershell -ExecutionPolicy Bypass -File tools\package.ps1
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$site = Join-Path $root 'site'
$recto = Join-Path (Split-Path -Parent $root) 'Recto\site'
if (-not (Test-Path (Join-Path $recto 'index.html'))) { throw "Recto introuvable : $recto" }
$dist = Join-Path $root 'dist'
New-Item -ItemType Directory -Force $dist | Out-Null
$zip = Join-Path $dist 'portfolio.zip'
if (Test-Path $zip) { Remove-Item $zip -Force -Confirm:$false }
Add-Type -AssemblyName System.IO.Compression, System.IO.Compression.FileSystem
$archive = [IO.Compression.ZipFile]::Open($zip, 'Create')

# Ajoute les fichiers de $dir sous $prefix (chemins avec / : lisibles par le Web FTP).
function Add-Tree($dir, $prefix, $skip) {
  Get-ChildItem $dir -Recurse -File -Force | ForEach-Object {
    $rel = $prefix + $_.FullName.Substring($dir.Length + 1).Replace('\', '/')
    if (& $skip $rel) { return }
    [void][IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive, $_.FullName, $rel, 'Optimal')
  }
}
try {
  # site\recto est une jonction vers le dépôt de Recto (aperçu en local) : on la saute ici.
  Add-Tree $site '' { param($rel) $rel -like 'recto/*' }
  # Recto : la base et la clé secrète restent sur la machine (seul le .htaccess du dossier part).
  Add-Tree $recto 'recto/' { param($rel) ($rel -like 'recto/api/data/*' -and $rel -ne 'recto/api/data/.htaccess') -or $rel -match '\.(sqlite|sqlite-wal|sqlite-shm|key)$' }
} finally { $archive.Dispose() }
"OK : $zip ($([math]::Round((Get-Item $zip).Length / 1KB)) Ko)"

# LAB-11 controlled GitHub publication. Runs only from the extracted public package.
$ErrorActionPreference = 'Stop'
$Repo = 'r3eskelsen/eskelsen-business-website-demo'
$Root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
Set-Location -LiteralPath $Root
Write-Host '=== LAB-11 GITHUB PUBLICATION PREFLIGHT ===' -ForegroundColor Cyan
Write-Host "Target: https://github.com/$Repo"

foreach ($Command in @('git', 'gh')) {
    if (-not (Get-Command $Command -ErrorAction SilentlyContinue)) {
        throw "$Command not found. Install Git for Windows and GitHub CLI before publishing."
    }
}

$Forbidden = @('.env', 'local_leads.sqlite3', '.venv', 'private', 'secrets.json')
foreach ($name in $Forbidden) {
    if (Test-Path -LiteralPath (Join-Path $Root $name)) {
        throw "Forbidden item in extraction directory: $name. Extract into a CLEAN folder."
    }
}
if (-not (Test-Path -LiteralPath 'PUBLIC_SHA256_MANIFEST.txt')) { throw 'Missing public manifest' }
$ManifestLines = @(Get-Content -LiteralPath 'PUBLIC_SHA256_MANIFEST.txt' | Where-Object { $_.Trim() })
$PublicFiles = @()
foreach ($line in $ManifestLines) {
    if ($line -notmatch '^([0-9A-Fa-f]{64})  (.+)$') { throw "Invalid manifest entry: $line" }
    $expected = $Matches[1].ToUpperInvariant()
    $relative = $Matches[2]
    if ($relative.StartsWith('/') -or $relative.Contains('..') -or $relative.Contains(':')) { throw "Unsafe manifest path: $relative" }
    $filePath = Join-Path $Root ($relative -replace '/', [IO.Path]::DirectorySeparatorChar)
    if (-not (Test-Path -LiteralPath $filePath -PathType Leaf)) { throw "Missing manifest file: $relative" }
    $actual = (Get-FileHash -LiteralPath $filePath -Algorithm SHA256).Hash.ToUpperInvariant()
    if ($actual -ne $expected) { throw "SHA256 mismatch: $relative" }
    $PublicFiles += $relative
}
Write-Host ("MANIFEST_SHA256=PASS ({0} files)" -f $PublicFiles.Count) -ForegroundColor Green

& gh auth status
if ($LASTEXITCODE -ne 0) { throw 'GitHub CLI login required: gh auth login' }
$who = (& gh api user --jq .login).Trim()
if ($LASTEXITCODE -ne 0 -or $who -ne 'r3eskelsen') {
    throw "Authenticated as '$who', expected r3eskelsen. Sign in to the correct GitHub account."
}

if (-not (Test-Path -LiteralPath '.git')) {
    $previousErrorAction = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try { & git rev-parse --is-inside-work-tree 2>$null | Out-Null; $isExistingTree = ($LASTEXITCODE -eq 0) }
    finally { $ErrorActionPreference = $previousErrorAction }
    if ($isExistingTree) { throw 'Extracted folder is inside a DIFFERENT Git repository; use a clean standalone folder.' }
}
$ExistingRemote = $false
$previousErrorAction = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
try { & gh repo view $Repo --json nameWithOwner --jq .nameWithOwner 2>$null | Out-Null; $ExistingRemote = ($LASTEXITCODE -eq 0) }
finally { $ErrorActionPreference = $previousErrorAction }
if ($ExistingRemote) {
    Write-Host 'Target repository already exists. Checking for refs...'
    $refs = @(& git ls-remote "https://github.com/$Repo.git" 2>$null)
    if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect remote; check git credential helper: gh auth setup-git' }
    if ($refs.Count -gt 0) { throw 'Remote repository is NOT empty. Stopping without overwriting any history.' }
} else {
    Write-Host 'Target does not exist; creating PUBLIC repository.'
    & gh repo create $Repo --public --description 'Local responsive website and synthetic FastAPI lead capture lab with tests and evidence.'
    if ($LASTEXITCODE -ne 0) { throw 'Failed to create GitHub repository' }
}

if (-not (Test-Path -LiteralPath '.git')) {
    & git init -b main
    if ($LASTEXITCODE -ne 0) { throw 'git init failed' }
}
& git branch --show-current | Out-Null
$branch = (& git branch --show-current).Trim()
if ($branch -ne 'main') { throw "Local branch '$branch' is not main; no automatic branch replacement" }
$previousErrorAction = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
try { & git remote get-url origin 2>$null | Out-Null; $NoOrigin = ($LASTEXITCODE -ne 0) }
finally { $ErrorActionPreference = $previousErrorAction }
if ($NoOrigin) {
    & git remote add origin "https://github.com/$Repo.git"
    if ($LASTEXITCODE -ne 0) { throw 'Failed to configure remote' }
} else {
    $url = (& git remote get-url origin).Trim()
    if ($url -ne "https://github.com/$Repo.git") { throw "Unexpected origin remote: $url" }
}

foreach ($f in $PublicFiles) {
    & git add -- $f
    if ($LASTEXITCODE -ne 0) { throw "Failed staging: $f" }
}
& git add -- 'PUBLIC_SHA256_MANIFEST.txt'
if ($LASTEXITCODE -ne 0) { throw 'Failed staging public manifest' }

& git diff --cached --quiet
if ($LASTEXITCODE -eq 0) { throw 'Nothing staged: repository may already be committed' }
& git commit -m 'Publish LAB-11 business website and synthetic lead capture demo'
if ($LASTEXITCODE -ne 0) { throw 'git commit failed. Configure git user.name and user.email first.' }
& git push -u origin main
if ($LASTEXITCODE -ne 0) { throw 'git push failed. Check authentication; no remote overwrite attempted.' }
Write-Host 'GITHUB_UPLOAD=PASS' -ForegroundColor Green
Write-Host "Verify: https://github.com/$Repo"

Param(
    [string]$Task = "help"
)

function Show-Help {
    Write-Host "Tasks: install, lint, test, docker-build, docker-run, shell, clean"
}

function Install {
    python -m venv .venv
    .\.venv\Scripts\pip.exe install --upgrade pip
    .\.venv\Scripts\pip.exe install -r requirements.txt
}

function Lint {
    if (Test-Path .\.venv\Scripts\flake8.exe) {
        .\.venv\Scripts\flake8.exe .
    } else {
        Write-Host "flake8 not found in .venv. Run 'Install' first or use global flake8."
    }
}

function Test-Run {
    if (Test-Path .\.venv\Scripts\pytest.exe) {
        .\.venv\Scripts\pytest.exe
    } else {
        Write-Host "pytest not found in .venv. Run 'Install' first or use global pytest."
    }
}

function Build {
    docker build -t leaffliction-dev .
}

function Run {
    docker run --name leaffliction-container --rm -it -v ${PWD}:/app leaffliction-dev
}

function Shell {
    Write-Host "Activate with: . \.\.venv\\Scripts\\Activate.ps1"
}

function Clean {
    Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue
    Get-ChildItem -Recurse -Include __pycache__ | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
}

switch ($Task.ToLower()) {
    "install" { Install }
    "lint" { Lint }
    "test" { Test-Run }
    "build" { Build }
    "run" { Run }
    "shell" { Shell }
    "clean" { Clean }
    default { Show-Help }
}

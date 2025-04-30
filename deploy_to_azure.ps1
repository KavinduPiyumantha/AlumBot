# deploy_to_azure.ps1 - PowerShell script for AlumBot deployment to Azure

param (
    [switch]$Help,
    [switch]$Clean,
    [switch]$Recreate,
    [string]$ResourceGroup = "AlumBotResourceGroup",
    [string]$ContainerName = "alumbot-container",
    [string]$AcrName = "alumbotreg",
    [string]$DnsName = "alumbot",
    [string]$Location = "eastus"
)

# Display help message
function Show-Help {
    # ...existing code...
}

# Show help if requested
if ($Help) {
    Show-Help
}

# Step 1: Start deployment
Write-Host "Starting AlumBot deployment to Azure..." -ForegroundColor Cyan

# Step 1.5: Switch to production environment
Write-Host "Switching to production environment..." -ForegroundColor Yellow
Copy-Item -Path ".env.production" -Destination ".env" -Force
Write-Host "Using production environment variables" -ForegroundColor Green

# Step 2: Clean databases if requested
if ($Clean) {
    # ...existing code...
}

# Continue with the rest of the deployment steps
# ...existing code...
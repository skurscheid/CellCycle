# change ExecutionPolicy first, otherwise AzureRM won't be installed
Set-ExecutionPolicy RemoteSigned

Install-Module -Name AzureRM

# Import the module into the PowerShell session
Import-Module AzureRM
# Connect to Azure with an interactive dialog for sign-in
Connect-AzureRmAccount

Update-Module -Name AzureRM

# select location for the resourceGroup

Get-AzureRmLocation | select Location
$location = "australiaeast"

# set name for resourceGroup
$resourceGroup = "CellCycle"

# create new resourceGroup
New-AzureRmResourceGroup -Name $resourceGroup -Location $location

# create actual storageAccount
$storageAccount = New-AzureRmStorageAccount -ResourceGroupName $resourceGroup `
  -Name "cellcycledata" `
  -Location $location `
  -SkuName Standard_LRS `
  -Kind Storage

$ctx = $storageAccount.Context

# a container is required to hold the blobs or other endpoints
$containerName = "bams"
New-AzureStorageContainer -Name $containerName -Context $ctx -Permission blob

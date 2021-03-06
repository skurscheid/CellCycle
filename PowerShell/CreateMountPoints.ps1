$resourceGroupName = "CellCycle"
$storageAccountName = "cellcycledata"
$fileShareName = "data"

# These commands require you to be logged into your Azure account, run Login-AzureRmAccount if you haven't
# already logged in.
$storageAccount = Get-AzureRmStorageAccount -ResourceGroupName $resourceGroupName -Name $storageAccountName
$storageAccountKeys = Get-AzureRmStorageAccountKey -ResourceGroupName $resourceGroupName -Name $storageAccountName

# The cmdkey utility is a command-line (rather than PowerShell) tool. We use Invoke-Expression to allow us to
# consume the appropriate values from the storage account variables. The value given to the add parameter of the
# cmdkey utility is the host address for the storage account, <storage-account>.file.core.windows.net for Azure
# Public Regions. $storageAccount.Context.FileEndpoint is used because non-Public Azure regions, such as soverign
# clouds or Azure Stack deployments, will have different hosts for Azure file shares (and other storage resources).
Invoke-Expression -Command "cmdkey /add:$([System.Uri]::new($storageAccount.Context.FileEndPoint).Host) " + `
    "/user:AZURE\$($storageAccount.StorageAccountName) /pass:$($storageAccountKeys[0].Value)"



$fileShare = Get-AzureStorageShare -Context $storageAccount.Context | Where-Object {
    $_.Name -eq $fileShareName -and $_.IsSnapshot -eq $false
}

if ($fileShare -eq $null) {
    throw [System.Exception]::new("Azure file share not found")
}

# The value given to the root parameter of the New-PSDrive cmdlet is the host address for the storage account,
# <storage-account>.file.core.windows.net for Azure Public Regions. $fileShare.StorageUri.PrimaryUri.Host is
# used because non-Public Azure regions, such as soverign clouds or Azure Stack deployments, will have different
# hosts for Azure file shares (and other storage resources).
$password = ConvertTo-SecureString -String $storageAccountKeys[0].Value -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential -ArgumentList "AZURE\$($storageAccount.StorageAccountName)", $password
New-PSDrive -Name V -PSProvider FileSystem -Root "\\$($fileShare.StorageUri.PrimaryUri.Host)\$($fileShare.Name)" -Credential $credential -Persist

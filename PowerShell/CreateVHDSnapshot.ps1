$resourceGroupName = "CellCycle"
$location= "australiasoutheast"
$vmName = "CellCycleVM"
$snapshotName = "preUpdate20181101"

$vm = get-azurermvm -ResourceGroupName $resourceGroupName -Name $vmName
$snapshot =  New-AzureRmSnapshotConfig -SourceUri $vm.StorageProfile.OsDisk.ManagedDisk.Id -Location $location -CreateOption copy
New-AzureRmSnapshot -Snapshot $snapshot -SnapshotName $snapshotName -ResourceGroupName $resourceGroupName

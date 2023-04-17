# Synchronize Directories Script v1.2
# Created by John Kesig

# This script is designed to synchronize one directory to another. Then it will generate a robocopy script that will get run and saved in the Windows Task Scheduler
# This was designed to be run while you are in the folder you want to synchronize. For that, I created a command in the right-click context menu to do this. You
# absolutely could change this to choose both source and destination directories. I also wanted this to be as native to the OS as possible so I didn't go with Python for this

Add-Type -AssemblyName System.Windows.Forms

# Gets and stores the starting folder
Function Source($sourceDirectory='')
{
    $rootDirectory = Get-Item .

    return $rootDirectory
}

# Prompts the user to select the destination directory they want to synchronize to
Function Destination($destinationDirectory='')
{
    $folder = New-Object System.Windows.Forms.FolderBrowserDialog
    $folder.Description = 'Choose Destination Folder to Synchronize'

    if($folder.ShowDialog() -eq "Ok")
    {
        $folderpath += $folder.SelectedPath
    }

    return $folderpath
}

# Creates the Synchronization script to be used by the Task Scheduler 
Function CreateSyncScript($syncScriptPath='')
{
    # We have to do a bit of error checking here, because the spaces in file paths will create problems so I implemented an escape character
    $sourceLocation = $source
    $sourceLocation = $sourceLocation -replace ' ', '` '

    $destinationLocation = $destination 
    $destinationLocation = $destinationLocation -replace ' ', '` '

    # Get Date and Time for logging
    $date = Get-Date -Format 'MMddyyyHHmm'
    $logName = '{0} Copy Log - {1}' -f $shortname,$date
    $logName = $logName -replace ' ', '` '

    # This is where the powershell script will be stored. Feel free to change this if you want
    $scriptDirectory = 'C:\SyncScripts\'
    $logDirectory = 'C:\SyncScripts\Logs\'
    $reportDirectory = '{0}{1}\' -f $logDirectory,$shortname
    
    # Test if the Script Directory exists. If it doesn't, it will create it.
    if(!(Test-Path -PathType Container $scriptDirectory))
    {
        New-Item -ItemType Directory -Path $scriptDirectory
    }

    if(!(Test-Path -PathType Container $logDirectory))
    {
        New-Item -ItemType Directory -Path $logDirectory
    }

    if(!(Test-Path -PathType Container $reportDirectory))
    {
        New-Item -ItemType Directory -Path $reportDirectory
    }

    # This is the script that will be run by Powershell to synchronize the two locations
    $script = 'robocopy {0} {1} *.* -e /v /tee /log:{2}{3}.txt' -f $sourceLocation,$destinationLocation,$reportDirectory,$logName

    # Test to see if the sync script file already exists. If it doesn't, it will create the file
    $testPath = Test-Path -PathType Leaf -Path $scriptDirectory$sourceShortName.ps1

    if($testPath -ne $true)
    {
        $scriptPath = New-Item -Path $scriptDirectory$sourceShortName.ps1
        Set-Content -Path $scriptPath -Value $script
    }

    return $scriptPath
}

# Creates the Task for the Task Scheduler
Function CreateTask()
{
    # Create everything associated with the Task
    # The Name is the folder you are doing a robocopy from and to
    $name = 'Synchronize {0} to {1}' -f $sourceShortName,$destinationShortName

    # The action is going to be launched by Powershell and it will run the script located in the Script Path above
    $action = New-ScheduledTaskAction -Execute 'PowerShell.exe' -Argument $scriptPath

    # You can designate a time and frequency here
    $trigger = New-ScheduledTaskTrigger -Daily -At '7:00 PM'

    $description = 'Synchronizes {0} to {1}' -f $sourceShortName,$destinationShortName

    # This script used to run when you go into idle, but sometimes people don't have Idle enabled so I removed it
    $settings = New-ScheduledTaskSettingsSet -IdleDuration 00:15:00 -DontStopOnIdleEnd

    $task = New-ScheduledTask -Description $description -Action $action -Trigger $trigger -Settings $settings

    # Register the task to the Task Manager
    Register-ScheduledTask -TaskName $name -InputObject $task

    # Enable and Start the Task
    Enable-ScheduledTask -TaskName $name
    Start-ScheduledTask -TaskName $name
}

# Gather the source folder this script will pull from (It will take from the one you initiated the script in)
$source = Source

# Allow the user to choose where they want the files to be synchronized to 
$destination = Destination

# Only get the names for the directories
$sourceShortName = $source|Split-Path -Leaf
$destinationShortName = $destination|Split-Path -Leaf

# Create the sync script that will be run for Task Scheduler
$syncScript = CreateSyncScript($source,$destination,$sourceShortName)
$scriptPath = $syncScript[2]

# Check to see if the $syncScript variable doesn't come back empty. IF it does then it prompts the user that a script has already been created
# If the script comes back with a path, it will create the task and prompt the user that everything has been completed
if($scriptPath -eq $null)
{
    [System.Windows.Forms.MessageBox]::Show('Your Sync Script has already been created. Check your SyncScripts folder')
} else {
    $task = CreateTask($sourceShortName,$destinationShortName,$scriptPath)
    [System.Windows.Forms.MessageBox]::Show('Your Sync Task has been generated. Please go to Task Scheduler to see your sync job. A log will be generated the next time the task is run')
}
# Parameters
$logFile = "C:\path\to\your\docker\log.txt"
$logName = "Application"
$source = "DockerLogParser"

# Ensure the source exists
if (![System.Diagnostics.EventLog]::SourceExists($source)) {
    [System.Diagnostics.EventLog]::CreateEventSource($source, $logName)
}

# Read, parse and write log entries
Get-Content -Path $logFile | ForEach-Object {
    if ($_ -match '^\[(?<timestamp>.*?)\]\[(?<source>.*?)\]\[(?<sev_short>.)\] time="(?<time_inner>.*?)" level=(?<severity>.*?) msg="(?<message>.*)"') {
        $severity = $matches['severity']
        $parsedTime = $matches['timestamp']

        # Determine EventLog EntryType
        $entryType = switch ($severity) {
            "info" { "Information" }
            "warning" { "Warning" }
            "error" { "Error" }
            default { "Information" }
        }

        $logMessage = "Timestamp: $parsedTime | Source: $($matches['source']) | Message: $($matches['message'])"

        Write-EventLog -LogName $logName -Source $source -EntryType $entryType -EventId 1 -Message $logMessage
    }
}
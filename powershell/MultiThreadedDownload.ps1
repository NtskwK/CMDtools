function PartiallyDownload-File([String]$Uri, [String]$OutFile, [Int64]$Start, [Int64]$End = 0, [String]$UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36') {
    [Net.ServicePointManager]::DefaultConnectionLimit = [Int32]::MaxValue
    $Request = [Net.WebRequest]::Create($Uri)
    if ($End) {
        $Request.AddRange($Start, $End)
    }
    else {
        $Request.AddRange($Start)
    }
    $Request.UserAgent = $UserAgent
    $Request.Proxy = $null
    $Response = $Request.GetResponse()
    $Stream = $Response.GetResponseStream()
    $File = [IO.File]::Create($OutFile)
    $Stream.CopyTo($File)
    $File.Close()
    $Stream.Close()
    $Response.Close()
}

function Merge-File([String[]]$Source, [String]$Destination) {
    $Source = $Source.Clone()
    for ($i = 0; $i -lt $Source.Length; $i++) {
        $Source[$i] = '"' + $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Source[$i]) + '"'
    }
    cmd /c copy /b /y ($Source -join '+') $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Destination) | Out-Null
}

function MultiThreadDownload-File([String]$Uri, [String]$OutFile, [Int32]$ThreadCount = 4, [Int32]$MinSliceSize = 256KB, [String]$UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36') {
    [Net.ServicePointManager]::DefaultConnectionLimit = [Int32]::MaxValue
    [Int64]$Length = (Invoke-WebRequest $Uri -Method Head -UseBasicParsing -Proxy $null).Headers.'Content-Length'
    [String[]]$Part = @()
    [Int64[]]$Start = @()
    [Int64[]]$End = @()
    [Management.Automation.PowerShell[]]$Job = @()
    [Object[]]$Handle = @()
    if (($MinSliceSize * $ThreadCount) -gt $Length) { $ThreadCount = [Math]::Floor($Length / $MinSliceSize) }

    for ($i = 0; $i -lt $ThreadCount; $i++) {
        $Start += $End[$i - 1] + [Int64](!!$i)
        $End += [Math]::Round($Length / $ThreadCount * ($i + 1))
        $Part += $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath([GUID]::NewGuid().ToString('N') + '.bin')
        $Job += [PowerShell]::Create().AddScript(${Function:PartiallyDownload-File}).AddParameter('Uri', $Uri).AddParameter('OutFile', $Part[$i]).AddParameter('Start', $Start[$i]).AddParameter('End', $End[$i]).AddParameter('UserAgent', $UserAgent)
        $Handle += $Job[$i].BeginInvoke()
    }

    [Double]$Progress = 0
    [Int32]$Interval = 200
    [Boolean]$Complete = $false
    while (!$Complete) {
        Start-Sleep -Milliseconds $Interval

        $Complete = $true
        for ($i = 0; $i -lt $ThreadCount; $i++) {
            if (!$Handle[$i].IsCompleted) {
                $Complete = $false
                break
            }
        }

        for ($i = 0; $i -lt $ThreadCount; $i++) {
            if (!(Test-Path $Part[$i])) { continue }
            $Progress = (Get-Item $Part[$i]).Length / ($End[$i] - $Start[$i] + 1) * 100
            Write-Progress -Id $i -Activity ('Thread #{0} {1} - {2}' -f $i, $Start[$i], $End[$i]) -Status ('{0} / {1} {2:f2}%' -f (Get-Item $Part[$i]).Length, ($End[$i] - $Start[$i] + 1), $Progress) -PercentComplete $Progress
        }
    }

    for ($i = 0; $i -lt $ThreadCount; $i++) {
        Write-Progress -Id $i -Activity ('Thread {0} - {1}' -f $Start[$i], $End[$i]) -Completed
        $Job[$i].EndInvoke($Handle[$i])
        $Job[$i].Runspace.Close()
        $Job[$i].Dispose()
    }

    Merge-File -Source $Part -Destination $OutFile
    foreach ($p in $Part) { Remove-Item $p }
}

# Test
MultiThreadDownload-File -Uri 'https://wp.natsuu.tk/api/raw/?path=/%E9%95%9C%E5%83%8F/Office/HomeStudent2021Retail.img' -OutFile 'HomeStudent2021Retail.img' -ThreadCount 8
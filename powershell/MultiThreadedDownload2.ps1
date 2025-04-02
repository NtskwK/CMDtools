<#
.SYNOPSIS
    使用多线程下载文件并保存到指定位置。

.DESCRIPTION
    此脚本通过多线程方式下载文件，支持自定义线程数和分片大小。
    如果未指定输出文件路径，则默认保存到当前工作目录。

.PARAMETER Uri
    要下载的文件的 URL。
    示例: https://example.com/file.zip

.PARAMETER OutFile
    保存文件的路径。如果未指定，则默认为当前工作目录下的文件名。
    示例: C:\Downloads\file.zip

.PARAMETER ThreadCount
    下载线程数。默认为 4。
    示例: 8

.PARAMETER MinSliceSize
    每个线程的最小分片大小。默认为 256KB。
    示例: 512KB

.EXAMPLE
    .\MultiThreadedDownload_hello.ps1 -Uri "https://example.com/file.zip" -OutFile "C:\Downloads\file.zip" -ThreadCount 8 -MinSliceSize 512KB

    使用 8 个线程下载文件，并将其保存到指定路径。

.EXAMPLE
    .\MultiThreadedDownload_hello.ps1 -Uri "https://example.com/file.zip"

    使用默认线程数和分片大小下载文件，并将其保存到当前工作目录。

.NOTES
    author: 小透明・宸, Natsuu
    version: 2.0
    release date: 2025-4-2
    docs: https://akarin.dev/2019/06/05/powershell-multithread-download/
#>

param (
    [String]$Uri,
    [String]$OutFile,
    [Int32]$ThreadCount = 4,
    [Int32]$MinSliceSize = 256KB,
    [Switch]$h,
    [Switch]$help
)

function Show-Help {
    Write-Host @"
Usage: .\MultiThreadedDownload_hello.ps1 -Uri <URL> [-OutFile <OutputFile>] [-ThreadCount <Threads>] [-MinSliceSize <Size>]

Parameters:
    -Uri            要下载的文件的 URL。
    -OutFile        保存文件的路径。如果未指定，则默认为当前工作目录下的文件名。
    -ThreadCount    下载线程数。默认为 4。
    -MinSliceSize   每个线程的最小分片大小。默认为 256KB。
    -h, --help      显示此帮助信息。

Examples:
    .\MultiThreadedDownload_hello.ps1 -Uri "https://example.com/file.zip" -OutFile "C:\Downloads\file.zip" -ThreadCount 8 -MinSliceSize 512KB
    .\MultiThreadedDownload_hello.ps1 -Uri "https://example.com/file.zip"
"@
    exit
}

if ($h -or $help) {
    Show-Help
}

if (-not $Uri) {
    Write-Host "Error: Uri parameter is required."
    Show-Help
}

if (-not $OutFile) {
    $OutFile = Join-Path -Path (Get-Location) -ChildPath (Split-Path -Leaf $Uri)
    Write-Host "Output file not specified. Using default: $OutFile"
}

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

# 调用下载函数
MultiThreadDownload-File -Uri $Uri -OutFile $OutFile -ThreadCount $ThreadCount -MinSliceSize $MinSliceSize
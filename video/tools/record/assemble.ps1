# Assemble a recorded shot into a 30 fps H.264 MP4 and a contact sheet at its marks. Arg: shot directory.
param([string]$Dir, [string]$Out)
$env:Path += ";$env:LOCALAPPDATA\Microsoft\WinGet\Links"
Push-Location $Dir
ffmpeg -v error -y -f concat -safe 0 -i list.txt -vf "fps=30,scale=1920:1080:flags=lanczos,format=yuv420p" -c:v libx264 -preset slow -crf 14 -movflags +faststart $Out
$marks = (Get-Content marks.json -Raw | ConvertFrom-Json).marks
New-Item -ItemType Directory -Force check | Out-Null
foreach ($m in $marks) {
  $t = [Math]::Max($m.t + 0.8, 0)
  ffmpeg -v error -y -ss $t -i $Out -frames:v 1 ("check/" + $m.label + ".png")
}
Pop-Location
ffprobe -v error -show_entries format=duration -of csv=p=0 $Out

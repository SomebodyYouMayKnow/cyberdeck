$ErrorActionPreference = 'Stop'
[xml]$doc = Get-Content -LiteralPath "$PSScriptRoot/proxmark3.sch" -Raw
$schematic = $doc.eagle.drawing.schematic
$names = @{}
foreach ($part in $schematic.parts.part) {
    $old = $part.GetAttribute('name')
    $names[$old] = 'PM3_' + $old.Replace('$','X')
    $part.SetAttribute('name', $names[$old])
}
foreach ($node in $doc.SelectNodes('//instance | //pinref')) {
    $node.SetAttribute('part', $names[$node.GetAttribute('part')])
}
foreach ($net in $doc.SelectNodes('//net')) {
    if ($net.name -ne 'GND') { $net.SetAttribute('name', 'PM3_' + $net.name.Replace('$','_').Replace('+','')) }
}
# Supply-symbol pins must match renamed global supply nets.
foreach ($symbol in $doc.SelectNodes('//symbol')) {
    foreach ($pin in $symbol.SelectNodes('pin[@direction="sup"]')) {
        if ($pin.name -ne 'GND') {
            $old = $pin.name
            $new = 'PM3_' + $old.Replace('+','')
            $pin.SetAttribute('name', $new)
            foreach ($t in $symbol.SelectNodes('text')) { $t.InnerText = $new }
        }
    }
}
# SAM7S512 and SAM7S64 share the 64-lead pinout; retain reference pin mapping.
foreach ($node in $doc.SelectNodes('//*[@name="AT91SAM7S64"]')) { $node.SetAttribute('name','AT91SAM7S512') }
foreach ($node in $doc.SelectNodes('//*[@symbol="AT91SAM7S64"]')) { $node.SetAttribute('symbol','AT91SAM7S512') }
foreach ($node in $doc.SelectNodes('//*[@deviceset="AT91SAM7S64"]')) { $node.SetAttribute('deviceset','AT91SAM7S512'); $node.SetAttribute('value','AT91SAM7S512-AU') }
foreach ($t in $doc.SelectNodes('//text[text()="AT91SAM7S64"]')) { $t.InnerText='AT91SAM7S512' }
$titles=@('POWER AND USB','FPGA AND ADC','ARM PROCESSOR','LF HF RECEIVER','ANTENNA DRIVERS')
$i=0
foreach ($sheet in $schematic.sheets.sheet) {
    $text=$doc.CreateElement('text')
    foreach ($kv in @{x='5';y='205';size='2.0';layer='97'}.GetEnumerator()) { $text.SetAttribute($kv.Key,$kv.Value) }
    $text.InnerText='NEONRED / PROXMARK3 - '+$titles[$i]+' - REFERENCE INTEGRATION, NOT RELEASED'
    [void]$sheet.plain.AppendChild($text)
    $note=$doc.CreateElement('text')
    foreach ($kv in @{x='5';y='198';size='1.27';layer='97'}.GetEnumerator()) { $note.SetAttribute($kv.Key,$kv.Value) }
    $note.InnerText='Source: Proxmark/proxmark3 doc/proxmark3.sch. USB device to Pi USB hub. Do not join internal rails to ESP32 rails.'
    [void]$sheet.plain.AppendChild($note)
    $i++
}
$out=Join-Path $PSScriptRoot 'NEONRED_Proxmark3.sch'
$doc.Save($out)
# Verify every reference circuit pin is retained on its original net after renaming.
[xml]$original=Get-Content -LiteralPath "$PSScriptRoot/proxmark3.sch" -Raw
$expected=@($original.SelectNodes('//net') | ForEach-Object {
    $netName=if($_.name -eq 'GND') {'GND'} else {'PM3_'+$_.name.Replace('$','_').Replace('+','')}
    foreach($pin in $_.SelectNodes('.//pinref')) { "$netName|$($names[$pin.part])|$($pin.gate)|$($pin.pin)" }
}) | Sort-Object
$actual=@($doc.SelectNodes('//net') | ForEach-Object {
    $netName=$_.name
    foreach($pin in $_.SelectNodes('.//pinref')) { "$netName|$($pin.part)|$($pin.gate)|$($pin.pin)" }
}) | Sort-Object
if(Compare-Object $expected $actual) { throw 'Netlist mismatch' }
"Prepared $out; verified $($actual.Count) pin-to-net memberships across $i sheets."

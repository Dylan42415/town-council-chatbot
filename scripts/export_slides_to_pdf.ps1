$pptxPath = "C:\Users\Dfault\Downloads\Hackaton\condo-request-classifier\output\slides\Town_Council_Chatbot_Showcase.pptx"
$pdfPath = "C:\Users\Dfault\Downloads\Hackaton\condo-request-classifier\output\slides\Town_Council_Chatbot_Showcase.pdf"

try {
    $ppt = New-Object -ComObject PowerPoint.Application
    $pres = $ppt.Presentations.Open($pptxPath, [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
    $pres.SaveAs($pdfPath, 32) # 32 = ppSaveAsPDF
    $pres.Close()
    $ppt.Quit()
    [System.GC]::Collect()
    Write-Output "PDF exported successfully: $pdfPath"
} catch {
    Write-Output "Error exporting PDF: $_"
}

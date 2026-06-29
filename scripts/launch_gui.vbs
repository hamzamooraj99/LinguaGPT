Option Explicit

Dim fileSystem, scriptsDirectory, projectRoot, launcher, shell

Set fileSystem = CreateObject("Scripting.FileSystemObject")
scriptsDirectory = fileSystem.GetParentFolderName(WScript.ScriptFullName)
projectRoot = fileSystem.GetParentFolderName(scriptsDirectory)
launcher = projectRoot & "\launcher\publish\LinguaGPT.Launcher.exe"

If Not fileSystem.FileExists(launcher) Then
    MsgBox "LinguaGPT is not set up yet. Run setup_launcher.cmd first.", 16, "LinguaGPT MCP"
    WScript.Quit 1
End If

Set shell = CreateObject("WScript.Shell")
shell.Run Chr(34) & launcher & Chr(34), 1, False

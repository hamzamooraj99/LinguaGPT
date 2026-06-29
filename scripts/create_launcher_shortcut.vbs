Option Explicit

Dim projectRoot, shell, desktop, shortcut, shortcutPath

If WScript.Arguments.Count <> 1 Then
    WScript.Echo "Expected the LinguaGPT project directory."
    WScript.Quit 1
End If

projectRoot = WScript.Arguments(0)
Set shell = CreateObject("WScript.Shell")
desktop = shell.SpecialFolders("Desktop")
shortcutPath = desktop & "\LinguaGPT MCP.lnk"

Set shortcut = shell.CreateShortcut(shortcutPath)
shortcut.TargetPath = shell.ExpandEnvironmentStrings("%SystemRoot%\System32\wscript.exe")
shortcut.Arguments = Chr(34) & projectRoot & "\scripts\launch_gui.vbs" & Chr(34)
shortcut.WorkingDirectory = projectRoot
shortcut.IconLocation = projectRoot & "\logo\linguagpt.ico,0"
shortcut.Description = "Start and stop the LinguaGPT MCP server"
shortcut.WindowStyle = 1
shortcut.Save

WScript.Echo "Created: " & shortcutPath

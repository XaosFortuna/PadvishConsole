#include <MsgBoxConstants.au3>
#include <AutoItConstants.au3>


Local $SleepTime = 1000
Func FindAgentFile()
;~ FIND AGENT FILE
FileChangeDir(@ComSpec)
$AgentFile = FileFindFirstFile(@WorkingDir & "\PadvishTSAgent" & "*")
If $AgentFile = -1 Then
   MsgBox($MB_SYSTEMMODAL, "", "Agent File Not Found")
EndIf
$file = FileFindNextFile($AgentFile)
Local $AgentFilePath = @WorkingDir & "\" & $file
Return $AgentFilePath
EndFunc

Func RunApplication()
;~ RUN APPLICATION
Run("C:\Program Files (x86)\AmnPardaz\Server\AmnPardazManagementConsole.exe")
Sleep($SleepTime * 2)
Local $WindowTitle = WinGetTitle("[CLASS:Qt5QWindowIcon]")
WinWait($WindowTitle, "")
WinActivate($WindowTitle, "")
Send("{DOWN}")
sleep($SleepTime)
EndFunc

func ConsoleLogIn()
;~ LOGIN
If WinExists("[TITLE:Login]")Then
   WinActivate("[CLASS:Qt5QWindowIcon]", "Login")
   Sleep($SleepTime)
   Send("admin")
   sleep($SleepTime)
   Send("{TAB}")
   Sleep($SleepTime)
   Send("{ENTER}")
   Sleep($SleepTime * 3)
Else
   MsgBox($MB_SYSTEMMODAL, "", "Problem With Logging In")
EndIf
EndFunc

Func CreateTask()
;~ CREATE TASK
Local $WindowTitle = WinGetTitle("[CLASS:Qt5QWindowIcon]")
WinActivate($WindowTitle, "")
Send("+{F10}")
Sleep($SleepTime)
Send("{DOWN 7}")
Sleep($SleepTime)
Send("{ENTER}")
Sleep($SleepTime * 1.5)
Send(FindAgentFile())
Send("{TAB 2}")
Send("{ENTER}")
EndFunc





RunApplication()
ConsoleLogIn()
CreateTask()

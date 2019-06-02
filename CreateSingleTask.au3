#include <MsgBoxConstants.au3>
#include <AutoItConstants.au3>
#include <Array.au3>
#include <Date.au3>
#include <File.au3>


$SleepTime = 500


Func ClientIpList()
   if FileExists(@WorkingDir & "\ClientIPList.txt")Then
   $file = @WorkingDir & "\ClientIPList.txt"
   Global $LinesArray[0]
   FileOpen($file, 0)
   For $i = 1 to _FileCountLines($file)
;~ 	  MsgBox($MB_SYSTEMMODAL, "", FileReadLine($file, $i))
	  ReDim $LinesArray[UBound($LinesArray) + 1]
	  $LinesArray[$i - 1] = FileReadLine($file, $i)
   Next
   FileClose($file)
   Return $LinesArray
   Else
   MsgBox($MB_SYSTEMMODAL, "", "Cannot Find IP List File")
   EndIf
EndFunc

Func GetCurrentDateTime()
   Return String(@YEAR & @MON & @MDAY & "-" &@HOUR & @MIN & @SEC)
EndFunc

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

Func RunPadvishConsole()
;~ RUN APPLICATION
Run("C:\Program Files (x86)\AmnPardaz\Server\AmnPardazManagementConsole.exe")
Sleep($SleepTime * 2)
Local $WindowTitle = WinGetTitle("[CLASS:Qt5QWindowIcon]")
WinWait($WindowTitle, "")
WinActivate($WindowTitle, "")
Send("{DOWN}")
sleep($SleepTime)
EndFunc

func PadvishConsoleLogIn()
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

Func AddNewAgent()
;~ ADD NEW AGENT TO CONSOLE
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
WinWait("[TITLE:Info]")
WinActivate("[TITLE:Info]")
Send("{TAB}")
Send("{ENTER}")
EndFunc

Func CreatePushInstallTask()
;~ CREATE PUSH INSTALL TASK
Local $WindowTitle = WinGetTitle("[CLASS:Qt5QWindowIcon]")
WinActivate($WindowTitle, "")
Send("+{F10}")
Sleep($SleepTime)
Send("{DOWN 5}")
Sleep($SleepTime)
Send("{RIGHT}")
Sleep($SleepTime)
Send("{DOWN 3}")
Sleep($SleepTime)
Send("{ENTER}")
WinWait("[TITLE:Push Install Wizard]","")
WinActivate("[TITLE:Push Install Wizard]","")
Sleep($SleepTime)
Send("{ENTER}")
Sleep($SleepTime)
Send( "^a" )
Sleep($SleepTime)
Send(GetCurrentDateTime())
Sleep($SleepTime)
Send("{TAB}")
Send(FileFindNextFile(FileFindFirstFile(@WorkingDir & "\PadvishTSAgent" & "*")))
Sleep($SleepTime)
Local $aPos = WinGetPos("[TITLE:Push Install Wizard]")
MouseClick($MOUSE_CLICK_LEFT, $aPos[0] + 380, $aPos[1] + 380, 1)
Send("{ENTER}")
Sleep($SleepTime)
Send("{SPACE 2}")
Sleep($SleepTime)
Send("{ENTER}")
Sleep($SleepTime)
Send("{TAB}")
Sleep($SleepTime)
Send("{SPACE}")
Sleep($SleepTime)
Send("{TAB 6}")
Sleep($SleepTime)
;~ SET CLIENT IP
for $ip in ClientIpList()
   Send($ip)
   Sleep($SleepTime)
   Send("{ENTER}")
next
Sleep($SleepTime)
Local $aPos = WinGetPos("[TITLE:Add IP]")
MouseClick($MOUSE_CLICK_LEFT, $aPos[0] + 270, $aPos[1] + 315, 1)
Sleep($SleepTime)
Send("{TAB 4}")
Sleep($SleepTime)
Send("{ENTER}")
Sleep($SleepTime)
;~ Add Acount
Send("{TAB}")
Sleep($SleepTime)
Send("{SPACE}")
Sleep($SleepTime)
Send("Administrator")
Sleep($SleepTime)
Send("{TAB}")
Sleep($SleepTime)
Send("1234567")
Sleep($SleepTime)
Send("{TAB}")
Sleep($SleepTime)
Send("1234567")
Sleep($SleepTime)
Send("{TAB 2}")
Sleep($SleepTime)
Send("{Enter}")
Sleep($SleepTime)
Send("{TAB 3}")
Sleep($SleepTime)
Send("{ENTER}")
Sleep($SleepTime)
Send("{TAB}")
Sleep($SleepTime)
Send("{SPACE}")
Sleep($SleepTime)
Send("{TAB 2}")
Sleep($SleepTime)
Send("{ENTER}")
Sleep($SleepTime)
Send("{ENTER}")
Sleep($SleepTime)
EndFunc







RunPadvishConsole()
PadvishConsoleLogIn()
CreatePushInstallTask()
FileOpen(@ScriptDir & "\TaskCreates", 1)
FileClose(@ScriptDir & "\TaskCreates")
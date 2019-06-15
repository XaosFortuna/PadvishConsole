#include <Array.au3>
#include <Constants.au3>

Local $aArray = _IPDetails()

Func _IPDetails()
    Local $oWMIService = ObjGet('winmgmts:{impersonationLevel = impersonate}!\\' & '.' & '\root\cimv2')
    Local $oColItems = $oWMIService.ExecQuery('Select * From Win32_NetworkAdapterConfiguration Where IPEnabled = True', 'WQL', 0x30), $aReturn[5] = [0]
    If IsObj($oColItems) Then
        For $oObjectItem In $oColItems
            If $oObjectItem.IPAddress(0) == @IPAddress1 Then
                $aReturn[0] = 4
                $aReturn[1] = $oObjectItem.IPAddress(0)
                $aReturn[2] = $oObjectItem.MACAddress
                $aReturn[3] = $oObjectItem.DefaultIPGateway(0)
                $aReturn[4] = _WMIArrayToString($oObjectItem.DNSServerSearchOrder(), ', ') ; You could use _ArrayToString() but I like creating my own Functions especially when I don't need alot of error checking.
            EndIf
        Next
    EndIf
    Return SetError($aReturn[0] = 0, 0, $aReturn)
EndFunc   ;==>_IPDetails

Func _WMIArrayToString($aArray, $sDelimeter = '|')
    Local $sString = 'Not Available'
    If UBound($aArray) Then
        For $i = 0 To UBound($aArray) - 1
            $sString &= $aArray[$i] & $sDelimeter
        Next
        $sString = StringTrimRight($sString, StringLen($sDelimeter))
    EndIf
    Return $sString
 EndFunc   ;==>_WMIArrayToString


Local $file = FileOpen("C:\ClientIP.txt", 1)
FileWrite($file, $aArray[1])
FileClose($file)
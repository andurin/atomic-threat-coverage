| Title              | DN_0006_2_windows_sysmon_process_changed_a_file_creation_time       |
|:-------------------|:------------------|
| **Author**         | @atc_project        |
| **Description**    | Explicit modification of file creation timestamp by a process |
| **Logging Policy** | <ul><li> Not existing </li></ul> |
| **References**     | <ul><li>[https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventid=90002](https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventid=90002)</li><li>[https://github.com/Cyb3rWard0g/OSSEM/blob/master/data_dictionaries/windows/sysmon/event-2.md](https://github.com/Cyb3rWard0g/OSSEM/blob/master/data_dictionaries/windows/sysmon/event-2.md)</li></ul> |
| **Platform**       | Windows    |
| **Type**           | Applications and Services Logs        |
| **Channel**        | Microsoft-Windows-Sysmon/Operational     |
| **Provider**       | Microsoft-Windows-Sysmon    |
| **Fields**         | <ul><li>EventID</li><li>Computer</li><li>Hostname</li><li>UtcTime</li><li>ProcessGuid</li><li>ProcessId</li><li>Image</li><li>TargetFilename</li><li>CreationUtcTime</li><li>PreviousCreationUtcTime</li></ul> |


## Log Samples

### Raw Log

```
- <Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">
  - <System>
    <Provider Name="Microsoft-Windows-Sysmon" Guid="{5770385F-C22A-43E0-BF4C-06F5698FFBD9}" /> 
    <EventID>2</EventID> 
    <Version>4</Version> 
    <Level>4</Level> 
    <Task>2</Task> 
    <Opcode>0</Opcode> 
    <Keywords>0x8000000000000000</Keywords> 
    <TimeCreated SystemTime="2018-12-10T15:08:56.961102400Z" /> 
    <EventRecordID>6994</EventRecordID> 
    <Correlation /> 
    <Execution ProcessID="2940" ThreadID="3576" /> 
    <Channel>Microsoft-Windows-Sysmon/Operational</Channel> 
    <Computer>atc-win-10.atc.local</Computer> 
    <Security UserID="S-1-5-18" /> 
  </System>
  - <EventData>
    <Data Name="RuleName" /> 
    <Data Name="UtcTime">2018-12-10 15:08:56.954</Data> 
    <Data Name="ProcessGuid">{9683FBB1-8164-5C0E-0000-00104B532800}</Data> 
    <Data Name="ProcessId">2788</Data> 
    <Data Name="Image">C:\Users\user1\AppData\Local\Temp\chocolatey\wireshark\2.6.5\Wireshark-win64-2.6.5.exe</Data> 
    <Data Name="TargetFilename">C:\Program Files\Wireshark\user-guide.chm</Data> 
    <Data Name="CreationUtcTime">2018-11-28 18:37:08.000</Data> 
  <Data Name="PreviousCreationUtcTime">2018-12-10 15:08:56.486</Data> 
  </EventData>
</Event>

```





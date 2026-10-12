# Read the selected NTLM authentication policy

Use the established Windows session on the owned host. Read only the named value, retaining host, time, OS build and errors:

~~~powershell
Get-ItemProperty -LiteralPath 'HKLM:\SYSTEM\CurrentControlSet\Control\Lsa' -Name LmCompatibilityLevel -ErrorAction Stop |
    Select-Object LmCompatibilityLevel
~~~

Missing or inaccessible data is unknown, not zero. Correlate the snapshot with the effective policy and that OS version's supported authentication behavior. A registry value alone does not show what a particular connection negotiated, which policy supplied it, or which other protections apply.

For the documented legacy policy mapping, 2 selects NTLMv1 authentication with NTLMv2 session security when supported; it does not mean the client falls back to NTLMv2 authentication. Value 3 selects outgoing NTLMv2 authentication but does not itself refuse incoming LM/NTLMv1 at the DC. Value 5 adds that refusal. Session security, outgoing response type and server acceptance are separate questions. Do not infer relay resistance, LDAP signing or channel binding from this one value.

Report the observed setting and any gap against the owner's intended policy. Use existing authentication events for a connection-level conclusion; do not induce authentication or weaken settings to validate the finding. Version defaults are not substitutes for current policy evidence.

Reference: [Microsoft's policy values and registry mapping](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/network-security-lan-manager-authentication-level).

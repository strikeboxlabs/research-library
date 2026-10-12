# Confirm one owned WinRM certificate session

Use only for one intended owned endpoint already configured for this client's certificate and account. Require trusted installed Ruby/WinRM dependencies, an issued PEM `client_cert`, its matching encrypted PEM `client_key`, and an independently trusted PEM `ca_bundle` for the server. Define `endpoint` as its approved HTTPS DNS URL including the configured WSMan path. An IP URL needs an IP SAN; disabling peer verification is not a hostname repair.

Review the client's installed WinRM version/API and intended startup environment. Current WinRM requires Ruby 3.2 or later; an old transcript does not establish that compatibility. This fixed command executes trusted local Ruby/library code and creates a remote PowerShell runspace solely for the identity query:

~~~bash
"$ruby_bin" - "$endpoint" "$client_cert" "$client_key" "$ca_bundle" <<'RUBY'
require 'winrm'
require 'io/console'
require 'uri'
endpoint, cert, key, trust = ARGV
uri = URI.parse(endpoint)
abort 'Expected an approved HTTPS endpoint without URL credentials' unless uri.scheme == 'https' && uri.host && !uri.userinfo
console = IO.console or abort 'An interactive console is required for the key passphrase'
key_pass = console.getpass('Private-key passphrase: ')
puts "Ruby=#{RUBY_DESCRIPTION}; WinRM=#{Gem.loaded_specs.fetch('winrm').version}"
connection = WinRM::Connection.new(
  endpoint: endpoint, transport: :ssl,
  client_cert: cert, client_key: key, key_pass: key_pass,
  ca_trust_path: trust, no_ssl_peer_verification: false
)
code = nil
connection.shell(:powershell) do |shell|
  result = shell.run('whoami') do |stdout, stderr|
    STDOUT.print stdout if stdout
    STDERR.print stderr if stderr
  end
  code = result.exitcode
end
abort 'No remote exit status returned' if code.nil?
exit code
RUBY
~~~

The passphrase unlocks the local private key; it is not the remote account password. WinRM's `key_pass` is forwarded to its certificate/key loader. The block closes the shell; retain Ruby status, remote output and any TLS/authentication diagnostic. A successful identity response establishes that mapped session at that time, not administrative rights or delegated credentials for a second service. A library/TLS/mapping failure needs that layer's evidence rather than an alternative account or disabled validation.

Microsoft documents certificate mapping to a local account. A historical domain-account identity without the server's mapping/configuration is insufficient to promise the same result elsewhere. CA issuance, server-certificate trust and account mapping remain separate prerequisites. No listener, mapping or trust settings are changed here.

References: [WinRM connection and shell API](https://github.com/WinRb/WinRM), [SSL transport/key loading](https://github.com/WinRb/WinRM/blob/main/lib/winrm/http/transport.rb), [Ruby console input](https://docs.ruby-lang.org/en/3.4/IO.html#method-i-getpass), and [Microsoft certificate authentication](https://learn.microsoft.com/en-us/windows/win32/winrm/authentication-for-remote-connections).

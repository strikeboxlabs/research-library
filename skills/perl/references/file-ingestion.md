# Review literal file ingestion before record validation

Require the complete acquired importer/wrapper source and its actual Perl generation. Inspect them as text; invoking the script or compiling imports is execution. Follow the wrapper's selected directories, checked cd, quoting/globs and argument list into the reader before examining its CSV/content checks.

Classic `<>` reads the magical ARGV handle through two-argument open semantics. Its arguments are not necessarily literal filesystem names, and an empty list falls back to standard input. In list context, `for (<>)` reads the input list before the loop processes records; a later record/field check does not validate earlier opens. Three-argument open on the output handle fixes that output operation only, leaving a separate diamond input path unchanged.

For owned source requiring literal filenames, use an explicit mode and filename with a lexical input handle. This **illustrative** read loop assumes the application has already chosen its permitted regular files and encoding; it does not modify the acquired source or enforce containment by itself:

~~~perl
use strict;
use warnings;
die "select at least one input file\n" unless @ARGV;
for my $path (@ARGV) {
    open(my $input, '<', $path) or die "input open failed: $!\n";
    while (my $record = readline($input)) {
        # Apply the application's actual parser and record contract here.
    }
    close($input) or die "input close failed: $!\n";
}
~~~

The literal read mode does not infer command execution from a pathname. It still follows filesystem resolution: symlinks, changing parents, special files, permissions and allowed roots need the task's actual selection policy. Explicit encoding layers can change the bytes; select them from the input contract. A read failure needs separate handling rather than being silently counted as successful EOF.

Perl5.22+ also supplies double-diamond `<<>>` with literal filename opens, including a literal `-` when passed as an argument. With no arguments it still reads stdin. Confirm interpreter support and whether the importer should permit that fallback; replacing an output open alone does not address the input operator.

For Text::CSV, inspect parser construction/options, record framing and error handling. Splitting a file into physical lines and parsing each line does not necessarily support quoted multiline fields. Successful parsing plus an expected field count establishes syntax/arity for that record, not field types, referential integrity or suitability for the chosen dataset. Preserve rejected/malformed counts and diagnostics. Appending the original line instead of the parser's fields also retains its original quoting/encoding.

Output append mode creates a missing file, and accepted earlier records can remain after a later failure. Check write and close results, output identity and the intended transactional/batch contract before deleting any source input. A wrapper that unconditionally deletes all directory contents after the importer runs can discard unrelated or rejected data. Retain these phase/status distinctions without launching an acquired cleanup job to inspect it.

References: [Perl open modes](https://perldoc.perl.org/functions/open), [ARGV and diamond input](https://perldoc.perl.org/perlop#I/O-Operators), [Text::CSV parser](https://metacpan.org/pod/Text::CSV).

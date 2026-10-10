// Inventory functions or decompile exact names/@entry-address selectors.
// @category CLI.Skills
import ghidra.app.util.headless.HeadlessScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;
import java.io.BufferedWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.List;

public class DecompileSelected extends HeadlessScript {
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (currentProgram == null || args.length < 1) {
            throw new IllegalArgumentException("Need a program and fresh output path, then optional names/@addresses");
        }
        List<Function> functions = new ArrayList<>();
        FunctionIterator it = currentProgram.getFunctionManager().getFunctions(true);
        while (it.hasNext()) {
            monitor.checkCancelled();
            functions.add(it.next());
        }
        try (BufferedWriter out = Files.newBufferedWriter(Path.of(args[0]), StandardCharsets.UTF_8,
                StandardOpenOption.CREATE_NEW, StandardOpenOption.WRITE)) {
            out.write("Program: " + currentProgram.getName() + "\nLanguage: " + currentProgram.getLanguageID()
                    + "\nAnalysis timeout in this run: " + analysisTimeoutOccurred() + "\n");
            if (args.length == 1) {
                for (Function f : functions) {
                    monitor.checkCancelled();
                    out.write(f.getEntryPoint() + "\t" + f.getName() + "\n");
                }
                out.write("END inventory count=" + functions.size() + "\n");
                return;
            }
            DecompInterface decompiler = new DecompInterface();
            int ok = 0, failed = 0;
            try {
                if (!decompiler.openProgram(currentProgram)) {
                    throw new IllegalStateException(decompiler.getLastMessage());
                }
                for (int i = 1; i < args.length; i++) {
                    monitor.checkCancelled();
                    String selector = args[i];
                    List<Function> matches = new ArrayList<>();
                    for (Function f : functions) {
                        boolean match = selector.startsWith("@")
                            ? f.getEntryPoint().equals(toAddr(selector.substring(1)))
                            : f.getName().equals(selector);
                        if (match) matches.add(f);
                    }
                    if (matches.size() != 1) {
                        out.write("FAILED " + selector + " matches=" + matches.size() + "\n");
                        failed++;
                        continue;
                    }
                    Function f = matches.get(0);
                    DecompileResults result = decompiler.decompileFunction(f, 60, monitor);
                    out.write("\nFUNCTION " + f.getEntryPoint() + " " + f.getName() + "\n");
                    if (!result.decompileCompleted() || result.getDecompiledFunction() == null) {
                        out.write("FAILED " + result.getErrorMessage() + "\n");
                        failed++;
                    } else {
                        out.write("OK\n" + result.getDecompiledFunction().getC() + "\n");
                        String message = result.getErrorMessage();
                        if (message != null && !message.isEmpty()) out.write("DIAGNOSTIC " + message + "\n");
                        ok++;
                    }
                }
                out.write("END selected ok=" + ok + " failed=" + failed + "\n");
            } finally {
                decompiler.dispose();
            }
        }
    }
}

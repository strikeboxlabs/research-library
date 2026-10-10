// Export a bounded mapped byte range without running the specimen.
// @category CLI.Skills
import ghidra.app.util.headless.HeadlessScript;
import ghidra.program.model.address.Address;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

public class ReadSelectedBytes extends HeadlessScript {
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (currentProgram == null || args.length != 3) {
            throw new IllegalArgumentException("Need program, fresh output path, mapped address, decimal count");
        }
        int count = Integer.parseInt(args[2]);
        if (count < 1 || count > 4096) {
            throw new IllegalArgumentException("Count must be 1..4096");
        }
        Address address = toAddr(args[1]);
        if (address == null) throw new IllegalArgumentException("Unknown address");
        monitor.checkCancelled();
        byte[] data = new byte[count];
        int read = currentProgram.getMemory().getBytes(address, data);
        if (read != count) throw new IllegalStateException("Short mapped read: " + read);
        Files.write(Path.of(args[0]), data, StandardOpenOption.CREATE_NEW, StandardOpenOption.WRITE);
        println("END bytes program=" + currentProgram.getName() + " address=" + address + " count=" + count);
    }
}

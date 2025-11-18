import subprocess
import os
from pathlib import Path
from typing import List, Optional

class CSharedLibraryCompiler:
    """
    A wrapper class to compile C source files into shared libraries (.so)
    using command line compilers (default: gcc).
    """

    def __init__(
        self,
        source_file,
        output_dir: Optional[str] = None,
        compiler: str = "gcc",
        flags: Optional[List[str]] = None
    ):
        """
        Initialize the compiler settings.
        Args:
            source_file: Path to the .c file (optional, can be passed to compile()).
            output_dir: Directory to save the library (default: same as source).
            compiler: Command to run compiler (default: 'gcc').
            flags: List of flags. If None, defaults to optimization and strictness.
        """
        self.source_file = Path(source_file).resolve() if source_file else None
        self.output_dir = Path(output_dir).resolve() if output_dir else None
        self.compiler = compiler

        # Default recommendation logic
        if flags is None:
            self.flags = ["-Wall", "-pedantic", "-Ofast", "-Wextra"]
        else:
            self.flags = flags

    def compile(self, source_override: Optional[str] = None, output_name: Optional[str] = None, ) -> str:
        """
        Compiles the C file.
        Args:
            source_override: specific file to compile if not set in __init__.
            output_name: custom name for the library (without extension).
        Returns:
            str: The absolute path to the compiled library.
        """
        # 1. Resolve Source File
        target_source = Path(source_override) if source_override else self.source_file

        if not target_source or not target_source.exists():
            raise FileNotFoundError(f"Source file not found: {target_source}")

        # 2. Resolve Output Directory
        # If output_dir is not set, use the directory where the source file lives
        target_dir = self.output_dir if self.output_dir else target_source.parent

        # Ensure output dir exists
        if not target_dir.exists():
            os.makedirs(target_dir)

        # 3. Resolve Output Filename
        lib_prefix = 'lib'
        lib_ext = '.so'

        if output_name:
            # Use custom name
            final_name = ""
            if lib_prefix != output_name[:len(lib_prefix)]:
                final_name += lib_prefix
            final_name += output_name
            if lib_ext != output_name[-len(lib_ext):]:
                final_name += lib_ext
        else:
            # Defaults to source filename: 'mylib.c' -> 'libmylib.so'
            final_name = lib_prefix + target_source.stem + lib_ext

        output_path = target_dir / final_name

        # 4. Construct Command
        # Start with compiler
        cmd = [self.compiler]

        # Add User Flags
        cmd.extend(self.flags)

        # Add Mandatory Flags for Shared Libraries
        # -shared: Create a shared library
        # -fPIC: Position Independent Code (Required for .so on Linux/Mac, ignored on Windows)
        if "-shared" not in self.flags:
            cmd.append("-shared")

        if "-fPIC" not in self.flags:
            cmd.append("-fPIC")

        # Add Output path
        cmd.extend(["-o", str(output_path)])

        # Add Source path
        cmd.append(str(target_source))

        # 5. Execute
        print(f"[Compiler] Executing: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"[Compiler] Success! Library created at: {output_path}")
            return str(output_path.absolute())

        except subprocess.CalledProcessError as e:
            print(f"[Compiler] Error:\n{e.stderr}")
            raise RuntimeError("Compilation failed.") from e


#!/usr/bin/env python3
"""
Script to check if all prerequisites for building the OpenTelemetry C++ bindings are met.
"""

import subprocess
import sys
import shutil
from pathlib import Path


def check_command(cmd, version_arg="--version", min_version=None):
    """Check if a command exists and optionally verify version."""
    if not shutil.which(cmd):
        return False, f"{cmd} not found in PATH"

    try:
        result = subprocess.run(
            [cmd, version_arg],
            capture_output=True,
            text=True,
            timeout=5
        )
        version_output = result.stdout or result.stderr
        return True, version_output.split('\n')[0]
    except Exception as e:
        return False, str(e)


def check_python_package(package):
    """Check if a Python package is installed."""
    try:
        __import__(package)
        return True, f"{package} is installed"
    except ImportError:
        return False, f"{package} not found"


def check_pkg_config(package):
    """Check if a package is findable via pkg-config."""
    try:
        result = subprocess.run(
            ["pkg-config", "--exists", package],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            version_result = subprocess.run(
                ["pkg-config", "--modversion", package],
                capture_output=True,
                text=True,
                timeout=5
            )
            version = version_result.stdout.strip()
            return True, f"Found via pkg-config (version {version})"
        return False, "Not found via pkg-config"
    except FileNotFoundError:
        return None, "pkg-config not available"
    except Exception as e:
        return False, str(e)


def check_cmake_package(package):
    """Check if a CMake package is findable."""
    cmake_code = f"""
cmake_minimum_required(VERSION 3.15)
project(test)
find_package({package} QUIET)
if({package}_FOUND)
    message(STATUS "FOUND")
else()
    message(STATUS "NOT_FOUND")
endif()
"""

    try:
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            cmake_file = Path(tmpdir) / "CMakeLists.txt"
            cmake_file.write_text(cmake_code)

            result = subprocess.run(
                ["cmake", "."],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=10
            )

            if "FOUND" in result.stderr or "FOUND" in result.stdout:
                return True, "Found via CMake"
            return False, "Not found via CMake"
    except Exception as e:
        return False, str(e)


def main():
    print("Checking prerequisites for OpenTelemetry C++ Python bindings...\n")

    all_ok = True

    # Check Python version
    print("=== Python ===")
    py_version = sys.version.split()[0]
    py_major, py_minor = sys.version_info[:2]
    if py_major >= 3 and py_minor >= 7:
        print(f"✓ Python {py_version}")
    else:
        print(f"✗ Python {py_version} (requires >= 3.7)")
        all_ok = False

    # Check CMake
    print("\n=== CMake ===")
    found, info = check_command("cmake", "--version")
    if found:
        print(f"✓ CMake: {info}")
    else:
        print(f"✗ CMake: {info}")
        print("  Install: brew install cmake (macOS) or apt-get install cmake (Linux)")
        all_ok = False

    # Check C++ compiler
    print("\n=== C++ Compiler ===")
    for compiler in ["g++", "clang++", "c++"]:
        found, info = check_command(compiler, "--version")
        if found:
            print(f"✓ {compiler}: {info}")
            break
    else:
        print("✗ No C++ compiler found")
        print("  Install: xcode-select --install (macOS) or apt-get install build-essential (Linux)")
        all_ok = False

    # Check pybind11
    print("\n=== pybind11 ===")
    found, info = check_python_package("pybind11")
    if found:
        try:
            import pybind11
            version = pybind11.__version__
            print(f"✓ pybind11 version {version}")
            if tuple(map(int, version.split('.'))) < (2, 10, 0):
                print("  ⚠ Warning: pybind11 >= 2.10.0 is recommended")
        except:
            print(f"✓ {info}")
    else:
        print(f"✗ {info}")
        print("  Install: pip install pybind11")
        all_ok = False

    # Check OpenTelemetry C++
    print("\n=== OpenTelemetry C++ ===")

    # Try pkg-config first
    found_pkg, info_pkg = check_pkg_config("opentelemetry-cpp")
    if found_pkg:
        print(f"✓ OpenTelemetry C++: {info_pkg}")
    elif found_pkg is None:
        # pkg-config not available, try CMake
        print("  pkg-config not available, checking via CMake...")
        found_cmake, info_cmake = check_cmake_package("opentelemetry-cpp")
        if found_cmake:
            print(f"✓ OpenTelemetry C++: {info_cmake}")
        else:
            print(f"✗ OpenTelemetry C++: {info_cmake}")
            print("  Install instructions:")
            print("    macOS: brew install opentelemetry-cpp")
            print("    Linux: See BUILD_INSTRUCTIONS.md")
            all_ok = False
    else:
        # pkg-config available but package not found
        print(f"  {info_pkg}, checking via CMake...")
        found_cmake, info_cmake = check_cmake_package("opentelemetry-cpp")
        if found_cmake:
            print(f"✓ OpenTelemetry C++: {info_cmake}")
        else:
            print(f"✗ OpenTelemetry C++: Not found")
            print("  Install instructions:")
            print("    macOS: brew install opentelemetry-cpp")
            print("    Linux: See BUILD_INSTRUCTIONS.md")
            all_ok = False

    # Summary
    print("\n" + "=" * 60)
    if all_ok:
        print("✓ All prerequisites are met!")
        print("\nYou can now build the extension:")
        print("  make build")
        print("  # or")
        print("  pip install -e .")
        return 0
    else:
        print("✗ Some prerequisites are missing.")
        print("\nPlease install the missing components and try again.")
        print("See BUILD_INSTRUCTIONS.md for detailed installation instructions.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

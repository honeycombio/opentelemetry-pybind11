# OpenTelemetry C++ Python Bindings

[![OSS Lifecycle](https://img.shields.io/osslifecycle/honeycombio/honeycomb-pycpp?color=success)](https://github.com/honeycombio/home/blob/main/honeycomb-oss-lifecycle-and-practices.md)
[![Build](https://github.com/honeycombio/honeycomb-pycpp/actions/workflows/build-wheels.yml/badge.svg)](https://github.com/honeycombio/honeycomb-pycpp/actions/workflows/build-wheels.yml)

Python bindings for the OpenTelemetry C++ SDK, providing high-performance tracing capabilities through a Pythonic interface. This library is **experimental**.

## Prerequisites

### System Dependencies

1. **OpenTelemetry C++ SDK**
   ```bash
   # macOS
   brew install opentelemetry-cpp

   # Ubuntu/Debian
   sudo apt-get install libopentelemetry-dev

   # From source
   git clone https://github.com/open-telemetry/opentelemetry-cpp.git
   cd opentelemetry-cpp
   mkdir build && cd build
   cmake -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
         -DWITH_OTLP_HTTP=ON \
         -DBUILD_TESTING=OFF \
         ..
   make -j
   sudo make install
   ```

2. **Python dev dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/honeycombio/honeycomb-pycpp
cd honeycomb-pycpp

# Install in development mode
pip install -e .

# Or build and install
pip install .
```

### Building

The build process uses CMake through setuptools:

```bash
python -m pip wheel . --wheel-dir=./build --no-deps -v

# Or use pip
pip install -v .
```

## Project Structure

```
honeycomb-pycpp/
├── CMakeLists.txt           # CMake build configuration
├── pyproject.toml           # Python project metadata
├── setup.py                 # Build script
├── include/
│   └── tracer_wrapper.h     # C++ wrapper headers
├── src/
│   ├── tracer_wrapper.cpp   # C++ wrapper implementation
│   └── bindings.cpp         # pybind11 bindings
├── examples/
│   └── basic_tracing.py     # Example usage
└── README.md                # This file
```

## Development

### Building for Development

```bash
# Install in editable mode
pip install -e .

# Rebuild after C++ changes
pip install -e . --force-reinstall --no-deps
```

### Requirements

- Python >= 3.10
- CMake >= 3.15
- C++17 compatible compiler
- OpenTelemetry C++ SDK
- pybind11 >= 2.10.0

### Troubleshooting

Running pip install is failing

```bash
# clean up cmake cache files
rm -rf CMakeCache.txt CMakeFiles/ cmake_install.cmake build/ dist/ *.egg-info/ *.so

# Install in editable mode
pip install -e .
```

## Performance Considerations

- The C++ SDK provides better performance than pure Python implementations
- Use the OTLP exporter with batch processing for production workloads
- Console exporter is useful for development and debugging
- Remember to call `provider.shutdown()` to flush buffered spans

## Limitations

- Only HTTP OTLP exporter is currently supported (not gRPC)
- Metrics and logs are not yet supported (tracing only)
- Links are not supported yet, requires an update to OTel C++'s ABI v2

## Future Enhancements

- [ ] Baggage propagation
- [ ] Metrics and logs support
- [ ] gRPC OTLP exporter
- [ ] Sampling configuration
- [ ] Custom span processors

## License

Apache License 2.0

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## Related Projects

- [OpenTelemetry C++](https://github.com/open-telemetry/opentelemetry-cpp)
- [OpenTelemetry Python](https://github.com/open-telemetry/opentelemetry-python)
- [pybind11](https://github.com/pybind/pybind11)

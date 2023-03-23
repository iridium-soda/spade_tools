# spade_tools
A toolbox designed for analysis of audit results from SAPDE about cross-namespace events.

# Reference
https://github.com/ashish-gehani/SPADE

# Example
`libnss_files.so2` in raw json is like:
```json
{
    "annotations":{
        "path":"/lib/x86_64-linux-gnu/libnss_files.so.2",
        "subtype":"file",
        "permissions":"0644",
        "epoch":"0",
        "source":"syscall",
        "version":"0"
    },
    "id":"406d863c2d3d03be3c2db1f23b267b97",
    "type":"Artifact"
}
```
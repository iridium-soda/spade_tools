# libnss_filter

A filter script to extract `libnss_files.so2` flow by ID from SPADE raw json.

# Data structure
Usually records from SPADE have two main categories:
- Node refers entity like files or processes;
- Edge refers operateion or relations marked as `USED`, `CLONE`, or more.

They are classified by its `type` field.
An artifact has the following field:
```json
{
    "annotations":{
        "path":"/etc/security/pam_env.conf",
        "subtype":"file",
        "permissions":"0644",
        "epoch":"0",
        "source":"syscall",
        "version":"0"
    },
    "id":"c42b141c1922ef08799ad00a2b4fde77",
    "type":"Artifact"
}
```
Process:
```json
{
    "annotations":{
        "gid":"0",
        "euid":"0",
        "children pid namespace":"4026531836",
        "start time":"1679540190.367",
        "ns pid":"2981",
        "pid":"2981",
        "source":"syscall",
        "net namespace":"4026531992",
        "ipc namespace":"4026531839",
        "ppid":"2906",
        "pid namespace":"4026531836",
        "uid":"0",
        "egid":"0",
        "exe":"/usr/bin/sudo",
        "mount namespace":"4026531840",
        "name":"sudo",
        "user namespace":"4026531837"
    },
    "id":"f25b0d40691d218ca120747c13fa5dfb",
    "type":"Process"
}
```

And each node is marked by its `id` field uniquely and edge is marked by its `event id` uniquely.
# TroubleShoot
`KeyError: 'Process'`: No record included in the data you provided has the `'Process'` key.

# TODO
- target file libnss should be `"path":"/lib/x86_64-linux-gnu/libnss_files.so.2","subtype":"file"` only. Maybe another `syscall`?
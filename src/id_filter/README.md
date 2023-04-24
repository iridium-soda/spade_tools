# Cross-namespace filter by id

As we all know, `uid` and `gid` is a way to decide if we are in a container as the isolation of user namespace. So when SAPDE is ubable to extract namespace information while auditing we can use `id` as another way. Maybe...

## Usage

```shell
python3 filter.py <path_of_file_from_sapde_to_be_filtered>
```

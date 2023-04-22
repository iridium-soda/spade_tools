# Simple-tracker

To analyse and trace the call chain of the given entity upward/downward from the given data from SPADE.

## Usage

```shell
python tracker.py
```

Check and set args in the global var before running.

And data will be saved in `./data/[target_id]/[layer]`.

## Items should be checked before running

- `DATA_PATH`: Raw data from SPADE
- `OUTPUT_PATH`: Where output data should be saved. Use `../data/` default.
- `TAR_ID`: `id` of artifact wanna trace.
- `DIRECTION`: `True`=Upward and `False`=Downward


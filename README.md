Backuprotation
==============

A minimalistic python tool which allows you to easily rotate your backups, whether they are a directory or files.


## Installation

`backuprotation` is available through `pip`

```shell
pip install backuprotation
```

## Usage

To rotate your backups which are stored in `./path` simply run

```shell
backuprotation ./path
```
and `backuprotation` will look through `./path` and keep the last ten directories while deleting the rest.

You can specify the amount of backups to keep with `-n` or `--number`
```shell
backuprotation -n 20 ./path
```

By default `backuprotation` looks for directories but it can also rotate files or both files and directories
```shell
backuprotation -f ./path        # files
backuprotation -fd ./path       # files and directories
```

If you're ever unsure of what effects `backuprotation` will have you can perform a dry-run to verify.
```shell
backuprotation --dry-run ./path
```
This will print out the changes that `backuprotation` would perform without actually changing the filesystem.

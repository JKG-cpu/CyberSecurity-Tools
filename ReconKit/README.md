# Recon Kit

A command line tool that scans hosts you specifiy + formates and saves them to an output file

## Help

Run the --help command for help on commands
```bash
reconkit --help  # INSTALLATION ONLY
```

Or if you have the repo locally
```bash
source .venv/bin/activate

python main.py --help
```

## Flags

| Flag | Description |
|------|-------------|
| `--report` | Generate a report on the last scan |
| `--scan` | Scan a host (host set in config settings) |
| `--config` | Open config settings |

## Requirements

- Python 3.11+
- [List Of Libraries](./requirements.txt)

## License

MIT
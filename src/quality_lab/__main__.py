"""CLI contract: validation succeeds with 0, processing errors return 2."""
import argparse
import json
import os
from pathlib import Path
import tempfile
from .data.validation import validate_manifest


def main():
    parser = argparse.ArgumentParser(prog='quality_lab')
    sub = parser.add_subparsers(dest='command', required=True)
    validate = sub.add_parser('validate')
    validate.add_argument('--config', required=True, type=Path)
    run = sub.add_parser('run')
    run.add_argument('--config', required=True, type=Path)
    run.add_argument('--limit', type=int)
    args = parser.parse_args()
    try:
        if args.command == 'run':
            from .runner.pilot import run_pilot
            return run_pilot(args.config, args.limit)
        config = json.loads(args.config.read_text(encoding='utf-8'))
        if not isinstance(config, dict) or config.get('schema_version') != '1.0':
            raise ValueError('Unsupported config version')
        base = args.config.resolve().parent
        result = validate_manifest(base / config['data_root'], config['manifest'])
        output = base / config['output']
        output.parent.mkdir(parents=True, exist_ok=True)
        name = None
        try:
            with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=output.parent,delete=False) as handle:
                name = handle.name
                json.dump(result,handle,ensure_ascii=False,indent=2,allow_nan=False)
                handle.write('\n'); handle.flush(); os.fsync(handle.fileno())
            os.replace(name,output)
        finally:
            if name and os.path.exists(name): os.unlink(name)
        print(json.dumps(result,ensure_ascii=False,allow_nan=False))
        return 0 if result['valid'] else 2
    except (OSError,ValueError,KeyError,TypeError,ImportError):
        print(json.dumps({'valid':False,'errors':[{'code':'configuration_or_io_error'}]}))
        return 2

if __name__ == '__main__':
    raise SystemExit(main())

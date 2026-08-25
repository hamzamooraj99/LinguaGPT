"""Command-line entry point for ``python -m viewer``."""

from __future__ import annotations

from argparse import ArgumentParser

import uvicorn

from .app import create_app
from .storage import resolve_data_root


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Run the read-only LinguaMCP Markdown viewer.")
    parser.add_argument("--host", default="127.0.0.1", help="Interface to bind (default: 127.0.0.1)")
    parser.add_argument("--port", default=8001, type=int, help="Port to bind (default: 8001)")
    parser.add_argument(
        "--data-root",
        default=None,
        help="Learner data root; otherwise LINGUAMCP_DATA_ROOT or repository tutor_data.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    application = create_app(data_root=resolve_data_root(args.data_root))
    uvicorn.run(application, host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main()

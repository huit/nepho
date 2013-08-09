from nepho.parser import parse_args
from nepho.plugin import serialize

__all__ = ["command"]

def command():
    args = parse_args()
    subcmd = args['subcommand']
    deployment  = args['deployment']
    # FIXME: check to see whether we know of such a plugin
    opts = dict( args['opts'] )
    serialized = serialize(subcmd,deployment,opts)
    return serialized

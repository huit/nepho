from hu.parser import parse_args
from hu.plugin import serialize

__all__ = ["command"]

def command():
    args = parse_args()
    plugin = args['subcommand']
    # FIXME: check to see whether we know of such a plugin
    opts = dict( args['opts'] )
    serialized = serialize(plugin,opts)
    return serialized

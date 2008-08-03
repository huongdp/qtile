"""
    A command shell for Qtile.
"""
import cmd, readline, sys, pprint, textwrap, traceback
import command


class Cmd(cmd.Cmd):
    prompt = "qsh> "
    def __init__(self, client):
        self.client = client
        self.builtins = []
        for i in client.commands.keys():
            self.builtins.append(i)
            def _closure():
                htext = client.commands.doc(i)
                commandName = i
                def help(self):
                    print htext
                def do(self, arg):
                    if not arg:
                        arg = "()"
                    try:
                        val = eval(
                                    "client.%s%s"%(commandName, arg),
                                    {},
                                    dict(client=client, commandName=commandName)
                              )
                    except command.CommandError, val:
                        print "Error: %s"%val
                    except command.CommandException, val:
                        print val
                    except Exception, val:
                        print val
                    else:
                        if val:
                            pprint.pprint(val)
                setattr(Cmd, "do_"+i, do)
                setattr(Cmd, "help_"+i, help)
            _closure()
        cmd.Cmd.__init__(self)

    def do_quit(self, arg):
        sys.exit(0)
    do_exit = do_quit
    do_q = do_quit
    do_EOF = do_quit

    def help_quit(self):
        return "Exit the program."

    def do_helpall(self, arg):
        for i in self.client.commands.keys():
            print self.client.commands.doc(i)
            print

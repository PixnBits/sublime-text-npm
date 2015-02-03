# copied from https://github.com/benschwarz/sublime-bower/blob/master/bower/utils/cli.py and modified
# original license:
# Copyright © 2013 Ben Schwarz
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# this is a modified version (ex: overcome python bug 6689)

import sublime
import os
import signal
import subprocess
import copy

if os.name == 'nt':
    LOCAL_PATH = ';' + os.getenv('APPDATA') + '\\npm'
    BINARY_NAME = 'npm.cmd'
else:
    LOCAL_PATH = ':/usr/local/bin:/usr/local/sbin:/usr/local/share/npm/bin'
    BINARY_NAME = 'npm'

class CLI():
    def find_binary(self):
        # TODO: memoize?
        appendedPath = os.environ['PATH']+LOCAL_PATH
        for dir in appendedPath.split(os.pathsep):
            path = os.path.join(dir, BINARY_NAME)
            if os.path.exists(path):
                #print("find_binary: "+path)
                return path
        #print("unable to find_binary with path "+appendedPath)
        sublime.error_message(BINARY_NAME + ' could not be found in your $PATH. Check the installation guidelines - https://github.com/PixnBits/sublime-text-npm')

    def _prepare_command(self, command):
        binary = self.find_binary()
        command.insert(0, binary)

        cflags = 0

        if os.name == 'nt':
            cflags = 0x08000000  # Avoid opening of a cmd on Windows (CREATE_NO_WINDOW)

        # per http://bugs.python.org/issue6689 Popen handles commands differently on Win vs *nix
        # see http://stackoverflow.com/a/1254322/2770309
        if os.name != 'nt':
            command = " ".join(command)

        return [command, cflags]

    def execute(self, command, cwd):
        command, cflags = self._prepare_command(command)
        # copy our extra places to look (#16)
        environ = copy.copy(os.environ)
        environ['PATH'] += LOCAL_PATH
        #print("environ[PATH]: "+environ['PATH'])

        proc = subprocess.Popen(command,
            shell=True,
            env=environ,
            cwd=cwd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            creationflags=cflags)

        stdout_data, stderr_data = proc.communicate()
        returncode = proc.wait()

        if stdout_data:
            stdout_data = stdout_data.decode('utf-8')
        if stderr_data:
            stderr_data = stderr_data.decode('utf-8')

        return [returncode, stdout_data, stderr_data]

    # based on http://stackoverflow.com/a/4418193
    def execute_long_running(self, command, cwd, on_readline, on_exit=None):
        command, cflags = self._prepare_command(command)
        process = subprocess.Popen(command,
            shell=True,
            cwd=cwd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            creationflags=cflags,
            #preexec_fn=os.setsid # http://stackoverflow.com/a/4791612/2770309
        )
        #process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        process_handler = CliLong()
        process_handler.set_process(process)
        process_handler.set_callback_line(on_readline)
        process_handler.set_callback_exit(on_exit)

        process_handler.start_reading()

        return process_handler


class CliLong(object):
    def set_process(self, process):
        self.process = process

    def set_callback_line(self, callback_line, callback_self=None):
        self.callback_line = callback_line
        if callback_self:
            self.callback_self = callback_self

    def set_callback_exit(self, callback_exit, callback_self=None):
        self.callback_exit = callback_exit
        if callback_self:
            self.callback_self = callback_self

    def start_reading(self):
        # in the api docs as set_async_timeout but
        # per http://sublimetext.userecho.com/topic/165027-typo-on-st3-api-documentation/
        # it is really set_timeout_async
        sublime.set_timeout_async(self._readlines, 0)

    def _readlines(self):
        process = self.process

        if not process:
            print("no process")
            return

        have_callback_line = hasattr(self, 'callback_line')

        nextline = True
        while nextline:

            nextline = process.stdout.readline()
            nextline = nextline.decode('utf-8')

            if have_callback_line:
                self.callback_line(nextline)

            if process.poll() != None:
                if have_callback_line:
                    output = process.communicate()[0]
                    self.callback_line(output)
                
                self.returncode = process.returncode
                if hasattr(self, 'callback_exit'):
                    self.callback_exit(self.returncode)
                return self.returncode

    def stop(self):
        process = self.process
        print("CliLong stop "+str(process.poll()))
        if None == process.poll():
            pid = process.pid
            print("stopping process "+str(pid))
            #print("dir process "+str(dir(process)))
            self.terminating = True
            process.terminate()
            if process._child_created:
                pid_child = pid + 1
                print("pid_child: "+str(pid_child))
                os.kill(pid_child, signal.SIGTERM)
        print("CliLong stopped? e "+str(process.poll()))

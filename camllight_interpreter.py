#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Caml Light interpreter written in Python 3 in order to get the output of
Caml Light programs as it was launched with the official interpreter."""

import click
import subprocess
import sys

INTERPRETER = "camllight"
TEMP_DIR = "/tmp/"
GIT_LINK = ("https://raw.githubusercontent.com/tbagrel1/" +
            "sublime_camllight/master/camllight_interpreter.py")
ERROR_MSG = "\n=== ERRORS ===\n"
SCRIPT_PATH = sys.argv[0]
CLEAN = True

def update(debug):
    """Update the current script by downloading the new one from GitHub."""
    # Downloading
    try:
        subprocess.run("cd \"{}\" && wget \"{}\"".format(TEMP_DIR, GIT_LINK),
                       shell=True, check=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        click.echo("\nUnable to retrieve the new version of the script. "
                   "Please try again later.\n")
        if debug:
            click.echo("Original error: [{}]\n".format(e.stderr.read()))
        return False
    # Move (may need superuser privileges)
    try:
        subprocess.run("cd {} && mv \"camllight_interpreter.py\" \"{}\""
                       .format(TEMP_DIR, SCRIPT_PATH), shell=True, check=True,
                       stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        click.echo("\nUnable to move the new script to the current script "
                   "directory. Please re-run the script with enough "
                   "privileges.\n")
        if debug:
            click.echo("Original error: [{}]\n".format(e.stderr.read()))
        return False
    click.echo("\nUpdate was successful!\n")
    return True

def clean_stdout(text):
    """Clean the stdout given by the Caml Light interpreter."""
    return "\n".join([line[1:] for line in text.split("\n")[2:]]) + "\n"

def clean_stderr(text):
    """Clean the stderr given by the Caml Light interpreter."""
    return "\n".join([line[1:] for line in text.split("\n")]) + "\n"

def run(in_path, out_file, show, debug):
    """Run the specified Caml Light file."""
    try:
        obj = None
        with open(in_path, "r", encoding="utf-8") as in_file:
            obj = subprocess.run(["camllight"], stdin=in_file,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        stdout = obj.stdout.read()
        stderr = obj.stderr.read()
        if CLEAN:
            stdout = clean_stdout(stdout)
            stderr = clean_stderr(stderr)
        result = stdout
        if [line for line in stderr.split("\n") if line.strip()]:
            result += ERROR_MSG + "\n" + stderr
        if out_file:
            out_file.write(result)
        if show:
            click.echo(result)
        return True
    except Exception as e:
        click.echo("\nUnexpected error happened.\n")
        if debug:
            click.echo("Original error: [{}]\n".format(e))
        return False

@click.command()
@click.argument("in-path",
                type=click.Path(
                    exists=True, file_okay=True, dir_okay=False, readable=True,
                    resolve_path=True))
@click.option("--out-file", "-o", type=click.File(mode="w", encoding="utf-8"))
@click.option("--run/--update", default=True)
@click.option("--show/--no-show", default=True)
@click.option("--debug/--no-debug", default=False)
def main(in_path, out_file, run, show, debug):
    """Launcher."""
    if not run:
        update(debug)
    else:
        run(in_path, out_file, show, debug)


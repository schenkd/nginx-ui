import subprocess


def run_subprocess(call):
    """
    Args:
        call (list): List of strings repr. the command to run (ex. ["git", "diff", "--name-only"])
    Returns:
        str: The stdout from the command that was run
    """
    branch_out = subprocess.Popen(
        call,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    stdout, stderr = branch_out.communicate()
    if stderr:
        raise Exception(stderr)
    return stdout

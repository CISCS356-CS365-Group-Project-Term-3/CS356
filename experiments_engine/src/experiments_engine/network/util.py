import subprocess

def run_except(command: list[str], shell=False):
    result = subprocess.run(command, shell=shell, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f'Network command {command} exited with error code {result.returncode} \nstderr: {result.stderr} \nstdout: {result.stdout} ')

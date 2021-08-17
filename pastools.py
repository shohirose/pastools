import os
import re


def parse_url(url):
    # type: (str) -> tuple[str, str]
    """Parse a URL

    URL is in the format of 'pbscp://host/path'.

    Args:
        url: URL

    Returns:
        Tuple of host and file path

    Raises:
        ValueError: An error occurs if the url does not follow the format.
    """
    m = re.match(r'^pbscp://([^/]*)(/.*$)', url)
    if m:
        host = m.group(1)
        path = m.group(2)
        return host, path
    else:
        raise ValueError('Incorrect URL format: ' + url)


def parse_export_env(env):
    # type: (str) -> dict[str, str]
    """Parse environment variables to a dictionary.

    Exmple:
        env_vars = parse_export_env(job.attr_export_env_to_job)
        primary_file = env_vars['PAS_PRIMARY_FILE']

    Args:
        env: Environment variables.

    Returns:
        Pairs of the name and value of environment variables.
    """
    env_vars = env.split(',')
    return dict([tuple(var.split('=')) for var in env_vars])


def create_access_env_vars(host, path):
    # type: (str, str) -> dict[str, str]
    """Create environment variables for Access.

    This function creates theree environment variables for jobs in shared
    file systems:
    - ACCESS_INPUT_FILES
    - ACCESS_OUTPUT_FILES
    - ACCESS_RUNNING_FILES

    Args:
        host: Host of the primary file
        path: Path to the primary file

    Returns:
        Environment variables for Access
    """
    filename = os.path.basename(path)
    dirname = os.path.dirname(path)
    return {'ACCESS_INPUT_FILES': filename + '@' + host + ':' + path,
            'ACCESS_OUTPUT_FILES': '*@' + host + ':' + dirname,
            'ACCESS_RUNNING_FILES': dirname}


def add_access_env_vars(env):
    # type: (str) -> str
    """Add environment variables for Access.

    Args:
        env: job.attr_export_env_to_job

    Returns:
        A new job.attr_export_env_to_job

    Raises:
        ValueError: If PAS_PRIMARY_FILE is not found.
    """
    env_vars = parse_export_env(env)
    if 'PAS_PRIMARY_FILE' in env_vars:
        url = env_vars['PAS_PRIMARY_FILE']
        host, path = parse_url(url)
        vars = create_access_env_vars(host, path)
        return env + \
            ',ACCESS_INPUT_FILES=' + vars['ACCESS_INPUT_FILES'] + \
            ',ACCESS_OUTPUT_FILES=' + vars['ACCESS_OUTPUT_FILES'] + \
            ',ACCESS_RUNNING_FILES=' + vars['ACCESS_RUNNING_FILES']
    else:
        raise ValueError('PAS_PRIMARY_FILE is not found in:\n' + env)


def create_logs(dirname, basename):
    # type: (str, str) -> tuple[str, str]
    """Create log files for stdout and strerr and returns those paths.

    The name of stdout and stderr log files are respectively
    basename.o.log and basename.e.log.
    Returned paths are expected to be set to job.attr_output_path and
    job.attr_error_path, respectively.

    Args:
        dirname: Directory where log files are created. Must be an absolute path.
        basename: Base name for log files.

    Returns:
        A tuple of stdout and stderr log files.

    Raises:
        ValueError: dirname must be an absolute path.
    """
    if not os.path.isabs(dirname):
        raise ValueError('Path must be an absolute path: ' + dirname)
    out_path = os.path.join(dirname, basename + '.o.log')
    err_path = os.path.join(dirname, basename + '.e.log')
    with open(out_path, mode='w') as fout, open(err_path, mode='w') as ferr:
        pass
    return out_path, err_path

# pastools
Python scripts for application definitions of Altair Access Web.
Please note that pastools does not support python3 because Altair Access Web only supports Python 2.7.

# How to use
Please copy `pastools.py` under the `submittime` directory of your application definition, and import `pastools` in the `presubmit.py`.

```python
import pastools
import os

"""Set Acceess environment variables for shared file systems."""
# Convert string to dictionary for easy access
env_vars = pastools.parse_export_env(job.attr_export_env_to_job)
# Split the url to the primary file into host and path
host, path = pastools.parse_url(env_vars['PAS_PRIMARY_FILE'])
# Create environment variables as a dictionary
access_vars = pastools.create_access_env_vars(host, path)
# Add the variables to job.attr_export_env_to_job
for key, value in access_vars.items():
    job.attr_export_env_to_job = job.attr_export_env_to_job + \
        ',' + key + '=' + value
```
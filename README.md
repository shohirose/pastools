# pastools
Python scripts for application definitions of Altair Access Web.
Please note that pastools does not support python3 because Altair Access Web only supports Python 2.7.

# How to use
Please copy `pastools.py` under the `submittime` directory of your application definition, and import `pastools` in the `presubmit.py`.

```python
from pastools import add_access_env_vars
import os

# Add Acceess environment variables for shared file systems.
job.attr_export_env_to_job = add_access_env_vars(job.attr_export_env_to_job)
```
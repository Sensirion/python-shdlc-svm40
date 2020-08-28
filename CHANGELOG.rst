CHANGELOG
---------

0.2.1
:::::
- First public release
- Use ``sphinx-versioning`` to build documentation
- Fix missing ``import time`` in quick start documentation

0.2.0
:::::
- Breaking change to support version 2 hardware
- Cleanup for SHDLC interface to match similar implementations
- ``set_compensation_temperature_offset()`` will no longer write the value
  directly to the flash. Use ``store_nv_data()`` to store the values.

0.1.0
:::::
- Initial release

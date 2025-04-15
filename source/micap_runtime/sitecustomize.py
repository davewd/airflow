# Create a file named sitecustomize.py in your Python site-packages directory
# This script runs every time Python starts


def custom_import_hook():
    """Add custom global import modifications
    - Extend import paths
    - Add logging
    - Inject custom modules
    """
    #import sys
    #sys.setdefaultencoding('utf-8')


    from dynamic_import_lib import setup_micap_importing
    setup_micap_importing()

    # Example: Set up global logging
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    logger.info("Sitecustomize Logging Initiated")
    print("Sitecustomize Logging Initiated.")
    # Optionally inject a custom module into builtins



print("Sitecustomize script Starting...")
custom_import_hook()
print("Sitecustomize script Finished.")

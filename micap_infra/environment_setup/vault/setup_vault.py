#!/usr/bin/env python3
import logging
import os
import sys

import hvac
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger('vault-setup')

# Load environment variables from .env file
load_dotenv()

# Vault configuration
VAULT_ADDR = os.getenv('VAULT_ADDR', 'http://127.0.0.1:8200')
VAULT_TOKEN = os.getenv('VAULT_TOKEN')  # Root token for initial setup

# Policy definitions
admin_policy = '''
# Admin policy
path "sys/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

path "auth/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

path "identity/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

path "secret/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}
'''

developer_policy = '''
# Developer policy
path "secret/data/dev/*" {
  capabilities = ["create", "read", "update", "list"]
}

path "secret/metadata/dev/*" {
  capabilities = ["list", "read"]
}

path "auth/token/lookup-self" {
  capabilities = ["read"]
}

path "auth/token/renew-self" {
  capabilities = ["update"]
}
'''

# New read-only policy
readonly_policy = '''
# Read-only policy
path "secret/data/*" {
  capabilities = ["read", "list"]
}

path "secret/metadata/*" {
  capabilities = ["list", "read"]
}

path "auth/token/lookup-self" {
  capabilities = ["read"]
}

path "auth/token/renew-self" {
  capabilities = ["update"]
}
'''

client = None

def client_setup():
    """Setup and authenticate Vault client."""
    global client

    if not VAULT_TOKEN:
        logger.error("VAULT_TOKEN environment variable not set. Please set it in your .env file.")
        sys.exit(1)

    client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)
    if not client.is_authenticated():
        logger.error("Failed to authenticate with Vault. Check your token and Vault address.")
        sys.exit(1)

    logger.info(f"Successfully connected to Vault at {VAULT_ADDR}")
    return client

def setup_policies():
    """Create admin, developer, and readonly policies."""
    try:
        client.sys.create_or_update_policy(
            name='admin',
            policy=admin_policy
        )
        logger.info("Admin policy created successfully")

        client.sys.create_or_update_policy(
            name='developer',
            policy=developer_policy
        )
        logger.info("Developer policy created successfully")

        # Add readonly policy
        client.sys.create_or_update_policy(
            name='readonly',
            policy=readonly_policy
        )
        logger.info("Read-only policy created successfully")

    except Exception as e:
        logger.error(f"Failed to create policies: {e!s}")
        sys.exit(1)

def setup_auth_methods():
    """Setup authentication methods for users."""
    try:
        # Enable userpass auth method if not already enabled
        if 'userpass/' not in client.sys.list_auth_methods():
            client.sys.enable_auth_method(
                method_type='userpass',
                path='userpass'
            )
            logger.info("Userpass auth method enabled")

        # Create admin user
        admin_password = os.getenv('ADMIN_PASSWORD', 'changeme_admin')
        client.auth.userpass.create_or_update_user(
            username='admin',
            password=admin_password,
            policies=['admin']
        )
        logger.info("Admin user created with admin policy")

        # Create developer user
        dev_password = os.getenv('DEV_PASSWORD', 'changeme_dev')
        client.auth.userpass.create_or_update_user(
            username='developer',
            password=dev_password,
            policies=['developer']
        )
        logger.info("Developer user created with developer policy")

        # Create readonly user
        readonly_password = os.getenv('READONLY_PASSWORD', 'changeme_readonly')
        client.auth.userpass.create_or_update_user(
            username='readonly',
            password=readonly_password,
            policies=['readonly']
        )
        logger.info("Read-only user created with readonly policy")

    except Exception as e:
        logger.error(f"Failed to setup auth methods: {e!s}")
        sys.exit(1)

def enable_secrets_engine():
    """Enable KV secrets engine version 2."""
    try:
        if 'secret/' not in client.sys.list_mounted_secrets_engines():
            client.sys.enable_secrets_engine(
                backend_type='kv',
                path='secret',
                options={'version': '2'}
            )
            logger.info("KV version 2 secrets engine enabled at 'secret/'")
    except Exception as e:
        logger.error(f"Failed to enable secrets engine: {e!s}")
        sys.exit(1)

def upload_secrets_from_env():
    """Upload secrets from .env file to Vault."""
    try:
        # Get all environment variables from .env
        dotenv_dict = {
            key: value for key, value in os.environ.items()
            if not key.startswith('VAULT_') and
            key not in ['ADMIN_PASSWORD', 'DEV_PASSWORD', 'READONLY_PASSWORD']
        }

        # Group secrets by prefixes to organize them
        dev_secrets = {}
        prod_secrets = {}
        other_secrets = {}

        for key, value in dotenv_dict.items():
            if key.startswith('DEV_'):
                dev_secrets[key] = value
            elif key.startswith('PROD_'):
                prod_secrets[key] = value
            else:
                other_secrets[key] = value

        # Upload secrets to appropriate paths
        if dev_secrets:
            client.secrets.kv.v2.create_or_update_secret(
                path='dev/config',
                secret=dev_secrets
            )
            logger.info(f"Uploaded {len(dev_secrets)} development secrets to 'secret/dev/config'")

        if prod_secrets:
            client.secrets.kv.v2.create_or_update_secret(
                path='prod/config',
                secret=prod_secrets
            )
            logger.info(f"Uploaded {len(prod_secrets)} production secrets to 'secret/prod/config'")

        if other_secrets:
            client.secrets.kv.v2.create_or_update_secret(
                path='general/config',
                secret=other_secrets
            )
            logger.info(f"Uploaded {len(other_secrets)} general secrets to 'secret/general/config'")

    except Exception as e:
        logger.error(f"Failed to upload secrets: {e!s}")
        sys.exit(1)

def revoke_root_token():
    """Create a new admin token and revoke the root token"""
    try:
        # Before revoking root, create a new admin token for emergencies
        admin_token = client.auth.token.create(
            policies=['admin'],
            ttl='8760h'  # 1 year
        )

        admin_token_value = admin_token['auth']['client_token']

        # Save the emergency admin token to a file
        with open('emergency_admin_token.txt', 'w') as f:
            f.write(f"Emergency Admin Token: {admin_token_value}\n")
            f.write("This token expires in 1 year. Keep this secure!\n")

        os.chmod('emergency_admin_token.txt', 0o600)  # Secure permissions
        logger.info("Emergency admin token created and saved to emergency_admin_token.txt")

        # Revoke root token
        root_token = client.token

        # Create a new client with the admin token to revoke the root
        admin_client = hvac.Client(url=VAULT_ADDR, token=admin_token_value)
        admin_client.auth.token.revoke(root_token)

        logger.info("Root token revoked successfully")
        logger.info("⚠️  IMPORTANT: The root token has been revoked. Use the emergency admin token or the admin user credentials from now on.")

    except Exception as e:
        logger.error(f"Failed to revoke root token: {e!s}")
        logger.error("Root token is still active. Manual revocation recommended.")

def main():
    """Run the complete setup process."""
    logger.info("Starting Vault setup process...")

    # Initialize client before using it
    client_setup()

    setup_policies()
    enable_secrets_engine()
    setup_auth_methods()
    upload_secrets_from_env()

    # Confirm before revoking root token
    logger.info("\n⚠️  WARNING: About to revoke the root token. This action cannot be undone.")
    response = input("Proceed with revoking the root token? (yes/no): ")

    if response.lower() in ['yes', 'y']:
        revoke_root_token()
    else:
        logger.info("Root token revocation skipped. You should revoke it manually when ready.")

    logger.info("Vault setup completed successfully!")


if __name__ == "__main__":
    main()

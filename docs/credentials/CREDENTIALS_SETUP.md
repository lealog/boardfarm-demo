# Credentials Management with Environment Variables

This project uses environment variable substitution to keep sensitive credentials out of version control.

## How It Works

1. **`inventory.json`** contains environment variable placeholders like `${CPE_USERNAME}`, `${CPE_PASSWORD}`, etc.
2. **`~/.boardfarm.env`** file (outside git repo) contains the actual credential values
3. **`conftest.py`** automatically loads the .env file and substitutes variables when tests run
4. No special import commands needed - everything works transparently!

## Setup

### 1. Create your credentials file

Copy the example and fill in your actual credentials:

```bash
cp .env.example ~/.boardfarm.env
nano ~/.boardfarm.env
```

Edit `~/.boardfarm.env` with your actual values:

```bash
CPE_USERNAME=your_actual_username
CPE_PASSWORD=your_actual_password
CPE_SHELL_PROMPT=root@.*#
CPE_GUI_PASSWORD=your_actual_gui_password
```

### 2. Run tests normally

No special commands needed:

```bash
pytest --station=my_ssh_cpe -v
```

The environment variables will be automatically loaded and substituted!

## How inventory.json Works

The `inventory.json` file uses placeholders:

```json
{
  "my_ssh_cpe": {
    "devices": [{
      "username": "${CPE_USERNAME}",
      "password": "${CPE_PASSWORD}",
      "shell_prompt": "${CPE_SHELL_PROMPT}"
    }]
  }
}
```

At runtime, these are automatically replaced with values from `~/.boardfarm.env`.

## .env File Locations

The system checks for credentials in this order:

1. `~/.boardfarm.env` (recommended - outside git repo)
2. `~/.env` (alternative location)
3. `.env` (project directory - not recommended)

## Files

- **`inventory.json`** - Contains `${VAR}` placeholders (committed to git)
- **`.env.example`** - Template file (committed to git)
- **`~/.boardfarm.env`** - Your actual credentials (outside git, NOT committed)
- **`conftest.py`** - Auto-loads .env and substitutes variables

## Security

- ✅ `inventory.json` with placeholders is safe to commit
- ✅ Actual credentials are in `~/.boardfarm.env` (outside git repository)
- ✅ `.env` files are already in `.gitignore`
- ✅ No special import commands needed
- ✅ Variables are substituted automatically at runtime

## For New Developers

When setting up on a new machine:

1. Clone the repository
2. Copy the example: `cp .env.example ~/.boardfarm.env`
3. Edit with your credentials: `nano ~/.boardfarm.env`
4. Run tests normally: `pytest --station=my_ssh_cpe -v`

## Adding New Variables

To add new credential variables:

1. Add placeholder to `inventory.json`: `"new_field": "${NEW_VAR}"`
2. Add value to `~/.boardfarm.env`: `NEW_VAR=actual_value`
3. Add to `.env.example`: `NEW_VAR=placeholder_value`
4. Done! No code changes needed.

## Verification

To verify the substitution is working:

```bash
# Check that .boardfarm.env exists
ls -la ~/.boardfarm.env

# Run a test to see if credentials are being used
pytest --station=my_ssh_cpe -v -k "test_basic"
```

The system will automatically substitute `${CPE_PASSWORD}` with your actual password from the .env file.

# EG4 Integration

## Overview
The EG4 Integration is a Home Assistant custom component designed to monitor and control EG4 battery systems. It provides real-time data, configuration options, and a dashboard for visualizing system performance.

## Features
- Support for multiple EG4 inverters.
- Real-time data polling for battery status, charge levels, and inverter performance metrics.
- Configuration UI for selecting inverter models and serial numbers.
- Alerts and notifications based on system performance.
- Dashboard visualization using YAML configuration.

## Installation via HACS

To install the EG4 Integration using HACS (Home Assistant Community Store), follow these steps:

1. **Ensure HACS is Installed**:
   - If you haven't installed HACS yet, visit [HACS Installation Guide](https://hacs.xyz/docs/setup/prerequisites) and follow the instructions.

2. **Add the Custom Repository**:
   - Open Home Assistant.
   - Navigate to **HACS** > **Integrations**.
   - Click the three dots in the top-right corner and select **Custom Repositories**.
   - Enter the following repository URL: `https://github.com/n2aws/hacs-eg4-integration`.
   - Set the category to **Integration**.

3. **Install the Integration**:
   - After adding the custom repository, search for "EG4 Integration" in the HACS Integrations section.
   - Click **Install**.

4. **Restart Home Assistant**:
   - Once the installation is complete, restart Home Assistant to load the integration.

5. **Configure the Integration**:
   - Navigate to **Settings** > **Devices & Services**.
   - Click **Add Integration** and search for "EG4 Integration".
   - Follow the configuration steps to set up your EG4 hardware.

6. **Import the Dashboard**:
   - Navigate to **Settings** > **Dashboards** in Home Assistant.
   - Click **Create Dashboard** and provide a name for the dashboard (e.g., "EG4 Battery System").
   - Click **Take Control** to enable manual configuration.
   - Open the `config/dashboard.yaml` file from the repository.
   - Copy the contents of the `dashboard.yaml` file.
   - Paste the copied YAML into the dashboard editor in Home Assistant.
   - Click **Save** to apply the changes.
   - Navigate to the newly created dashboard to view battery status, charge levels, inverter performance, alerts, and notifications.

For additional help, visit the [GitHub Repository](https://github.com/n2aws/hacs-eg4-integration).

## Configuration
1. Navigate to the Home Assistant Integrations page.
2. Search for "EG4 Integration" and click "Configure".
3. Select the EG4 inverter model(s), input serial numbers, and specify GridBoss details if applicable.

## Dashboard Setup
1. Import the `config/dashboard.yaml` file into your Home Assistant dashboard.
2. Navigate to the dashboard to view battery status, charge levels, inverter performance, alerts, and notifications.

## Usage Examples
- **Monitor Battery Status**: View real-time battery status and charge levels on the dashboard.
- **Enable Notifications**: Use the switch to enable notifications for system alerts.
- **Track Performance**: Use the history graph to track inverter performance over time.

## Troubleshooting
- **Error Logs**: Check Home Assistant logs for error messages.
- **Configuration Issues**: Ensure all serial numbers and models are correctly entered.
- **Network Connectivity**: Verify TCP/IP or USB-to-serial adapter connections.
- **Compatibility**: Ensure the integration is compatible with the latest Home Assistant version.

## Development
- Follow PEP 8 standards for code formatting.
- Use Python 3.9 or later.
- Run pre-commit hooks for linting and formatting checks.

## Support
For issues or feature requests, visit the [issue tracker](https://github.com/n2aws/hacs-eg4-integration/issues).

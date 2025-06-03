# EG4 Integration

## Overview
The EG4 Integration is a Home Assistant custom component designed to monitor and control EG4 battery systems. It provides real-time data, configuration options, and a dashboard for visualizing system performance.

## Features
- Support for multiple EG4 inverters.
- Real-time data polling for battery status, charge levels, and inverter performance metrics.
- Configuration UI for selecting inverter models and serial numbers.
- Alerts and notifications based on system performance.
- Dashboard visualization using YAML configuration.

## Installation
1. Clone this repository into your Home Assistant `custom_components` directory:
   ```bash
   git clone https://github.com/n2aws/hacs-eg4-integration.git custom_components/eg4_integration
   ```
2. Restart Home Assistant.
3. Add the integration via the Home Assistant UI.

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

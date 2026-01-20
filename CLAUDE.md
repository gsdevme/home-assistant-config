# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Home Assistant configuration repository for a home automation system running Home Assistant OS. The configuration manages a smart home with solar panels, battery storage (Solis inverter), energy management, lighting automation, climate control, and various IoT devices.

## Key Architecture Patterns

### Configuration Structure

The main `configuration.yaml` uses Home Assistant's `!include` directives to split configuration across multiple files:

- `automations/` - Individual automation files organized by room/function
- `templates/` - Template sensors for calculations (power usage, costs, heating)
- `sensors/` - Sensor definitions
- `binary-sensors/` - Binary sensor definitions
- `mqtt-sensors/` - MQTT sensor/switch configurations for Solis inverter, boiler, Tesla
- `python_scripts/` - Custom Python scripts (e.g., energy usage calculations)
- `blueprints/` - Reusable automation blueprints
- `www/` - Static web resources for Lovelace UI

### Energy Management System

The core functionality centers around energy optimization with a Solis solar inverter and battery:

- **MQTT Integration**: The Solis inverter publishes metrics to MQTT topics (see `mqtt-sensors/solis.yaml`)
- **Cheap Rate Charging**: Automations in `automations/charge_off_grid_inverter.yaml`, `automations/overnight_charge.yaml`, `automations/set_overnight_charge.yaml` manage battery charging during off-peak electricity rates
- **Power Usage Tracking**: Template sensors calculate real-time power usage, battery estimates, and efficiency (see `templates/power_usage.yaml`)
- **Grid Export**: Solar export management via `automations/solar_export.yaml`
- **Octopus Energy**: Integration with Octopus Energy tariffs for dynamic pricing

### Automation Organization

Automations follow two patterns:
1. **UI-based**: Stored in `automations.yaml` (managed through Home Assistant UI)
2. **Manual YAML**: Individual files in `automations/` directory for better version control

All automations include `source: /config/automations/[filename].yaml` for tracking.

### Custom Components

- `custom_components/solcast_solar/` - Solar forecasting integration (DO NOT modify without understanding the full component)

### Template Sensors

Template sensors use Jinja2 templating to calculate derived values:
- Battery life estimates based on current usage
- Power usage calculations combining grid, solar, and battery
- Cost calculations based on time-of-use tariffs
- Temperature averaging across multiple sensors

## Important Entity Patterns

- **Battery**: `sensor.solis_inverter_battery` (percentage)
- **Solar Generation**: `sensor.solis_inverter_pv` (watts)
- **Power Usage**: `sensor.power_usage` (calculated template sensor)
- **Cheap Rate**: `input_boolean.is_cheap_rate` (triggers charging automations)
- **Charge Control**: `input_number.charge_amps` (controls battery charging rate)

## Database Access

The Python script `python_scripts/get_energy_usage.py` directly queries the Home Assistant SQLite database at `/config/home-assistant_v2.db`. When modifying:
- Queries use UNIX timestamps
- Entity IDs must match exactly
- The `states` table contains historical sensor data

## Development Workflow

### Validating Configuration

Home Assistant validates YAML on restart. When making changes:
1. Check YAML syntax (Home Assistant is strict about indentation and data types)
2. Test automations using the "Execute" button in the UI before committing
3. Monitor Home Assistant logs for errors after changes

### Automation Development

When creating or modifying automations:
- Use unique IDs for all automations to enable UI editing
- Follow the existing pattern: `trigger` → `condition` → `action`
- Always include `mode:` (single, restart, parallel, queued)
- Add descriptive aliases
- For energy-related automations, consider `input_boolean.is_cheap_rate` as a condition

### Template Sensor Development

Template sensors must:
- Include `unique_id` for entity registry persistence
- Use `| float(0)` or similar filters to handle unavailable states
- Specify `unit_of_measurement` for numeric sensors
- Consider using `availability` templates to prevent errors when dependencies are unavailable

### MQTT Sensors

MQTT sensors for external devices (Solis inverter, boiler, Tesla):
- Use `expire_after` to mark stale data as unavailable
- Define `unique_id` for all entities
- Use `value_template` with JSON parsing for complex payloads
- Set appropriate `device_class` for Home Assistant categorization

## File Conventions

- All automation files should be in `automations/` and named by function (e.g., `automations/battery.yaml`)
- Template sensors go in `templates/` organized by domain (e.g., `templates/power_usage.yaml`)
- Use YAML anchors sparingly; Home Assistant's `!include` is preferred for reusability
- Secrets belong in `secrets.yaml` (git-ignored) and referenced with `!secret key_name`

## Integration-Specific Notes

### Solis Inverter
The Solis inverter is controlled via MQTT. Key topics:
- `solis/metrics` - Publishes battery, solar, and power data
- `solar_inverter_manager/set_optimal_income` - Controls grid charging mode

### Octopus Energy
Dynamic tariff integration affects charging schedules. The `is_cheap_rate` input boolean is the central control point for cost-optimized automations.

### InfluxDB
Selected sensors are exported to InfluxDB for long-term analytics. See `configuration.yaml` lines 236-264 for the entity list.

## Common Gotchas

- Template sensors with division must handle zero denominators (use `| float(1)` as divisor default)
- MQTT sensors need `expire_after` to avoid stale data
- Light groups defined in `configuration.yaml` (lines 266-298) don't auto-update when members change
- Automations using `state` triggers should specify `for:` duration to avoid false triggers
- The `!include_dir_merge_list` directive expects YAML files containing lists, not dictionaries
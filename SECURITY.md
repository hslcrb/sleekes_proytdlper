# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

Security is a core pillar of the Sleekes project. If you find a security vulnerability, please do not disclose it publicly. Instead, report it directly to the maintainers.

### IP Exposure & Anti-Ban
Sleekes includes advanced measures to protect your IP from being flagged as a bot by major platforms. These include:
- **Mobile Emulation**: Spoofing request headers to appear as a legitimate mobile client (Android/iOS).
- **UA Rotation**: Dynamic switching of browser identities.
- **Randomized Throttling**: Variable sleep intervals to mimic human behavior.

If you discover a way these measures can be bypassed or manipulated to expose user data or risk IP safety, please report it immediately.

### Data Privacy
Sleekes is a local-first application. 
- No metadata or personal information is transmitted to external servers.
- Auth cookies are used only locally to communicate with the target platform.

## Response Process
1. Acknowledgment within 48 hours.
2. Draft fix prepared for testing.
3. Coordinated public disclosure after the fix is merged.

---
*Stay Pure. Stay Secure.*

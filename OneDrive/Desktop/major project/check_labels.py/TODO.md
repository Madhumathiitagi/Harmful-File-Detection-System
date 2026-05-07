# TODO: Modernize Harmful File Detector GUI

## Approved Plan Breakdown
- [x] Update requirements.txt to include matplotlib and pillow for pie chart and icons.
- [x] Create gui_app_modern.py with modernized visuals:
  - Set cyber-purple accent theme.
  - Add subtle gradients/shadows with higher corner_radius.
  - Header: Add 🛡️ logo, animate title fade-in, glowing hover.
  - Theme: Keep toggle, add smooth transition, optional color dropdown.
  - Buttons: Add emojis as icons, glowing hover, pulse on click.
  - Logs: Translucent background, soft scroll, fade-in messages, timestamps.
  - Stats: Colored rounded cards, larger fonts, embedded matplotlib pie chart.
  - Progress: Glowing when active, "Scanning..." with looping dots.
  - Footer: Right-align, smaller font, fade-in.
  - Loading: Spinning 🛡️ overlay during scan.
  - Optional: Toast notifications, hover tooltips.
- [x] Preserve all existing functionality, threading, and backend logic.
- [ ] Test GUI for functionality preservation.
- [ ] Run scan to verify pie chart updates and animations.
- [ ] Ensure no backend performance impact.

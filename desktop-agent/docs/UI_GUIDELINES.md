# UthyAgent UI Guidelines

## Visual direction

Combine GNOME-native layout and typography with translucent Liquid Glass-inspired surfaces and restrained 3D soft-clay controls. Keep the application practical and readable on Zorin OS.

## Design tokens

- Base background: deep navy #0B1F2A.
- Main text: #F2F8F7.
- Secondary text: #B5C8C8.
- Mint accent: #B6F2D8.
- Raised surfaces: translucent pale mint over navy.
- Borders: thin, low-contrast white/mint strokes.
- Corner radii: 12 px for controls, 16 px for cards, 22 px for large panels.
- Shadows: soft ambient shadow plus a subtle lower-right contact shadow.

## Liquid Glass principles

1. Use translucency to establish hierarchy, never at the expense of text contrast.
2. Blur only decorative backgrounds. Keep labels and task status crisp.
3. Use thin highlights and subtle edge refraction rather than strong gradients.
4. Respect light and dark system preferences.
5. Provide solid-surface fallbacks when blur or transparency is unavailable.
6. Keep motion short and optional. Respect reduced-motion preferences.
7. Avoid stacking too many glass layers.

## Soft-clay icon principles

- Icons are raised, rounded, tactile 3D objects.
- Use soft clay or polished matte polymer shading with a clear light source.
- Use transparent backgrounds for standalone icon assets.
- Do not place icons inside circles, squares, badges, or decorative frames.
- Do not use sparkle icons anywhere in the app.
- Do not use emoji as UI icons.
- Maintain consistent perspective, scale, lighting, and shadow direction.
- Pair icons with text labels for important navigation and actions.
- Use standard accessible labels even when the visible icon is decorative.

## Interaction

- Every active task shows current status and last verified action.
- Mouse actions display a concise pointer tooltip such as "Clicking Save button".
- Tooltips must not obscure the target or remain indefinitely.
- Pause and emergency stop controls must remain easy to reach.
- Sensitive operations require an explicit confirmation dialog.
- Provide keyboard navigation, focus indicators, screen-reader labels, and sufficient contrast.

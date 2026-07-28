# Maharashtra Health Intelligence

A Marathi-first public health situation dashboard for Maharashtra.

## Important

- `data/dashboard.json` contains reviewed, executive-facing items.
- `data/review_queue.json` is automatically collected public news and must **not** be treated as verified.
- The scheduled workflow refreshes the review queue every three hours.
- Human verification is required before moving any item into the dashboard.

## Publish

1. In **Settings → Pages**, select **GitHub Actions** as the source.
2. Run the `Deploy dashboard to GitHub Pages` workflow.

Expected URL: `https://smaskar.github.io/maharashtra-health-intelligence/`

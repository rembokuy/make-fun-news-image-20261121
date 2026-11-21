[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/rembokuy/make-fun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/rembokuy/make-fun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

# The World Today — 21 November 2026

A one-page newspaper front page drawn entirely in code: seven verified
world news stories from Saturday, 21 November 2026.

- **Lead story:** magnitude 6.8 earthquake near Carhuamayo, Junín, Peru
- **Also inside:** COP31 talks overrun in Antalya · Houthi missiles hit
  a Saudi power plant · KL Rahul's SENA-history century in Wellington ·
  Lebanon's 83rd Independence Day · Yellow Vest marches in France ·
  SpaceX Dragon splashdown off California

## Run

Requires Python 3 and Pillow, plus the Liberation fonts shipped with
most Linux systems. No network access is used.

```sh
python3 main.py
```

This writes a single deterministic 1024×1024 PNG to `/output/entry.png`
(under 1 MiB). Running it twice produces a byte-identical file.

## Files

- `main.py` — the whole program: masthead, hero panel, six-panel grid,
  and footer, all drawn with Pillow
- `LICENSE` — MIT

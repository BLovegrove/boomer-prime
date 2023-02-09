from datetime import timedelta

import StringProgressBar
from StringProgressBar import progressBar as ProgressBar

# progress bar data
total = 234685
current = 77446
progress = ProgressBar.splitBar(total, current, 20)

# embed.set_author(
#     name=f"Info requested by: {sender.display_name}",
#     url=.embed.author.url,
#     icon_url=.embed.author.icon_url,
# )
# .embed.set_footer(text=f"🎵 {timeFormat(durationCurrent, { leading: true })} {progress} {timeFormat(durationTotal, { leading: true })} 🎵")
# embed.set_footer(
timestamp_current = str(timedelta(milliseconds=current)).split(".")[0]
timestamp_total = str(timedelta(milliseconds=total)).split(".")[0]
print(f"🎵 {timestamp_current} {progress[0]} {timestamp_total} 🎵")
# )

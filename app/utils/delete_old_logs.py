import os
import time
import re

LOG_FILE = "/home/ec2-user/ec2-c/app.log"
DAYS_TO_KEEP = 90

# Log satırındaki tarih formatı örneği: 2025-07-02 09:08:03,996
DATETIME_REGEX = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})")
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def delete_old_log_lines():
    if not os.path.exists(LOG_FILE):
        print("Log dosyası bulunamadı.")
        return

    now = time.time()
    cutoff = now - DAYS_TO_KEEP * 24 * 60 * 60
    new_lines = []
    removed = 0

    with open(LOG_FILE, "r") as f:
        for line in f:
            match = DATETIME_REGEX.match(line)
            if match:
                try:
                    log_time = time.mktime(time.strptime(match.group(1), DATETIME_FORMAT))
                    if log_time >= cutoff:
                        new_lines.append(line)
                    else:
                        removed += 1
                except Exception:
                    # Tarih parse edilemiyorsa satırı silme, ekle
                    new_lines.append(line)
            else:
                # Tarih yoksa satırı silme, ekle
                new_lines.append(line)

    with open(LOG_FILE, "w") as f:
        f.writelines(new_lines)

    print(f"{removed} satır silindi. Kalan satır: {len(new_lines)}")

if __name__ == "__main__":
    delete_old_log_lines()

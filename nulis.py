#!/usr/bin/env python3
# nulis.py
import requests
import urllib.parse
import os
import datetime
import math
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.table import Table

# ---------------- Config ----------------
API_URL = "https://api-nulis-iota.vercel.app/api/generate"
MAX_LINES = 28
AVG_CHAR_PER_LINE = 75
MAX_CHARS = 2400
MIN_CHUNK_CHARS = 50
OUTPUT_BASE = "/storage/emulated/0/NULIS"  # folder tujuan di Android
REQUEST_FILE = "request_nulis.txt"
console = Console()
# ----------------------------------------

def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    lines = [ln.rstrip() for ln in raw.replace("\r", "").split("\n")]
    clean = []
    blank = False
    for ln in lines:
        if ln.strip() == "":
            if not blank:
                clean.append("")
            blank = True
        else:
            clean.append(ln)
            blank = False
    return "\n".join(clean).strip()

def make_run_folder():
    hari_dict = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    now = datetime.datetime.now()
    hari = hari_dict[now.weekday()]
    folder_name = f"{hari}_{now.day:02d}_{now.hour:02d}-{now.minute:02d}-{now.second:02d}"
    folder_path = os.path.join(OUTPUT_BASE, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def prepare_next_slice(full_text, start_idx, target_len):
    end_idx = min(start_idx + target_len, len(full_text))
    chunk = full_text[start_idx:end_idx]
    if end_idx < len(full_text):
        split_at = max(chunk.rfind("\n"), chunk.rfind(" "), chunk.rfind("."), chunk.rfind("!"), chunk.rfind("?"))
        if split_at > max(0, int(target_len * 0.5)):
            chunk = chunk[:split_at+1]
            end_idx = start_idx + len(chunk)
    return chunk, end_idx

def send_chunk_get_save(chunk_text, out_dir, index):
    encoded = urllib.parse.quote(chunk_text)
    url = f"{API_URL}?text={encoded}"
    resp = requests.get(url, timeout=60)
    if resp.status_code == 200:
        fn = f"xyzresp_{index}.png"
        fp = os.path.join(out_dir, fn)
        with open(fp, "wb") as f:
            f.write(resp.content)
        return {"ok": True, "path": fp}
    else:
        try:
            j = resp.json()
        except Exception:
            j = None
        return {"ok": False, "status": resp.status_code, "json": j, "text": resp.text}

def smart_send(full_text, out_dir):
    total_len = len(full_text)
    ptr = 0
    file_index = 1
    progress = Progress(SpinnerColumn(), TextColumn("{task.description}"), BarColumn(), TimeElapsedColumn())
    task = progress.add_task("Mengirim...", total=None)
    console.print(Panel.fit("[bold cyan]XYZ NULIS GENERATOR[/bold cyan]\nMembagi teks jadi beberapa gambar bila perlu", title="Status", border_style="blue"))
    with progress:
        while ptr < total_len:
            target = MAX_CHARS
            chunk, new_ptr_candidate = prepare_next_slice(full_text, ptr, target)
            attempt_loop_count = 0
            while True:
                attempt_loop_count += 1
                progress.update(task, description=f"[cyan]Batch {file_index} - {len(chunk)} chars...")
                res = send_chunk_get_save(chunk, out_dir, file_index)
                if res["ok"]:
                    console.print(f"[green]✓[/green] Disimpan: {res['path']}")
                    ptr += len(chunk)
                    file_index += 1
                    break
                if res.get("json") and isinstance(res["json"], dict):
                    info = res["json"].get("info") or {}
                    j = info.get("jumlah_baris")
                    batas = info.get("batas_maksimum") or MAX_LINES
                    try:
                        j = int(j)
                    except Exception:
                        j = None
                    if j:
                        overflow_lines = max(0, j - MAX_LINES)
                        reduce_chars = int(math.ceil(overflow_lines * AVG_CHAR_PER_LINE * 1.1))
                        new_len = max(MIN_CHUNK_CHARS, len(chunk) - reduce_chars)
                        if new_len >= len(chunk):
                            new_len = max(MIN_CHUNK_CHARS, len(chunk) - int(AVG_CHAR_PER_LINE))
                        chunk = chunk[:new_len]
                        split_at = max(chunk.rfind("\n"), chunk.rfind(" "), chunk.rfind("."), chunk.rfind("!"), chunk.rfind("?"))
                        if split_at > max(0, int(new_len * 0.4)):
                            chunk = chunk[:split_at+1]
                        if attempt_loop_count > 6:
                            chunk = chunk[:max(MIN_CHUNK_CHARS, len(chunk)//2)]
                        continue
                chunk = chunk[:max(MIN_CHUNK_CHARS, len(chunk)//2)]
                if len(chunk) < MIN_CHUNK_CHARS:
                    console.print(f"[red]Gagal batch {file_index}. Status: {res.get('status')}[/red]")
                    console.print(res.get("json") or res.get("text"))
                    return file_index - 1
        return file_index - 1

def main():
    if not os.path.exists(REQUEST_FILE):
        console.print(f"[red]File '{REQUEST_FILE}' tidak ditemukan.[/red]")
        return
    text = load_text(REQUEST_FILE)
    if not text:
        console.print("[red]File request kosong setelah pembersihan.[/red]")
        return
    out_dir = make_run_folder()
    console.print(f"[bold]Output folder:[/bold] {out_dir}\n")
    total_saved = smart_send(text, out_dir)
    console.print()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Total Gambar")
    table.add_column("Folder")
    table.add_row(str(total_saved), out_dir)
    console.print(table)
    console.print(Panel.fit(f"[bold green]Selesai[/bold green]\nTotal {total_saved} file.\nFolder: {out_dir}", title="Hasil", border_style="green"))

if __name__ == "__main__":
    main()
import os
import time
import subprocess
import re
import csv

# Constants
README_FILE = "README.md"
CSV_FILE = "times.csv"
MARKDOWN_START = "<!-- START AOC TIMINGS -->"
MARKDOWN_END = "<!-- END AOC TIMINGS -->"


# Function to time a script
def time_script(filepath, input_file, runs=10):
    times = []
    print(f"Timing {filepath} with input {input_file}: ", end="", flush=True)
    binary = None

    # For C programs, compile first (but don't include this time in the timing)
    if filepath.endswith(".c"):
        binary = filepath.replace(".c", ".out")
        try:
            subprocess.run(["gcc", filepath, "-O2", "-o", binary], check=True)
        except Exception as e:
            print(f"\nCompilation Error: {e}")
            return f"Error: {e}"

    for i in range(runs):
        start_time = None
        end_time = None
        try:
            if filepath.endswith(".py"):
                # Time Python script execution
                start_time = time.time()
                subprocess.run(
                    ["python", filepath, input_file],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                end_time = time.time() - start_time
            elif filepath.endswith(".c"):
                # Time only the execution of the compiled binary
                start_time = time.time()
                subprocess.run(
                    [f"./{binary}", input_file],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                end_time = time.time() - start_time
        except Exception as e:
            print(f"\nError: {e}")
            return f"Error: {e}"
        times.append(end_time)
        # Print progress indicator
        print("." if i < runs - 1 else "*", end="", flush=True)

    if binary and os.path.exists(binary):
        os.remove(binary)  # Clean up the compiled binary

    print()  # Newline after progress indicators
    return {"best": min(times), "worst": max(times), "average": sum(times) / len(times)}


# Parse folder and group scripts
def parse_folder(folder):
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    problem_data = {}
    for file in files:
        match = re.match(r"day(\d+)-(part\d+)", file)
        if match:
            day, part = match.groups()
            problem_key = f"Day {day} {part}"
            if problem_key not in problem_data:
                problem_data[problem_key] = []
            problem_data[problem_key].append(
                (file, day)
            )  # Include day for input lookup
    return problem_data


# Load existing times from CSV
def load_csv(csv_file):
    if not os.path.exists(csv_file):
        return {}
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        return {row["File"]: row for row in reader}


# Save updated times to CSV
def save_csv(data, csv_file):
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["Day", "Part", "File", "Best", "Worst", "Average"]
        )
        writer.writeheader()
        writer.writerows(data.values())


# Load existing markdown
def load_markdown():
    if os.path.exists(README_FILE):
        with open(README_FILE, "r") as f:
            content = f.read()
        start_index = content.find(MARKDOWN_START)
        end_index = content.find(MARKDOWN_END)
        if start_index != -1 and end_index != -1:
            return (
                content[: start_index + len(MARKDOWN_START)] + "\n",
                content[end_index:],
            )
    return MARKDOWN_START + "\n", MARKDOWN_END + "\n"


# Save updated markdown
def save_markdown(before, table, after):
    with open(README_FILE, "w") as f:
        f.write(before)
        f.write(table)
        f.write(after)


def main(folder=".", input_folder="input"):
    problem_data = parse_folder(folder)
    existing_data = load_csv(CSV_FILE)
    new_data = existing_data.copy()

    print(f"Found {len(problem_data)} problems to process.\n")

    # Time new or missing scripts
    for problem, scripts in problem_data.items():
        match = re.match(r"Day (\d+) part(\d+)", problem)
        if not match:
            print(f"Skipping invalid problem key: {problem}")
            continue
        day, part = match.groups()

        input_file = os.path.join(input_folder, f"day{day}-input.txt")
        if not os.path.exists(input_file):
            print(f"Input file {input_file} not found for {problem}, skipping...")
            continue

        for script, script_day in scripts:
            if script not in existing_data:
                print(f"Processing {script} (Day {day}, Part {part})...")
                times = time_script(script, input_file)
                if isinstance(times, dict):  # Ensure no errors occurred
                    new_data[script] = {
                        "Day": day,
                        "Part": f"part{part}",
                        "File": script,
                        "Best": round(times["best"], 6),
                        "Worst": round(times["worst"], 6),
                        "Average": round(times["average"], 6),
                    }

    # Save updated times to CSV
    save_csv(new_data, CSV_FILE)

    # Generate markdown with separate tables for each day
    markdown_content = ""
    last_day = None  # Keep track of the previous day

    for entry in sorted(
        new_data.values(),
        key=lambda x: (int(x["Day"]), x["Part"], (len(x["File"]), x["File"])),
    ):
        if entry["Day"] != last_day:
            if last_day is not None:
                markdown_content += "\n"  # Separate days with a blank line
            markdown_content += f"### Day {entry['Day']}\n"
            markdown_content += "| Part | File                | Best Time (s) | Worst Time (s) | Average Time (s) |\n"
            markdown_content += "|------|---------------------|---------------|----------------|------------------|\n"
            last_day = entry["Day"]

        markdown_content += f"| {entry['Part']}  | {entry['File']:<19} | {entry['Best']:<13} | {entry['Worst']:<14} | {entry['Average']:<16} |\n"

    # Load markdown sections and update README
    before, after = load_markdown()
    save_markdown(before, markdown_content, after)
    print("\nProcessing complete. README.md updated!")


if __name__ == "__main__":
    main()

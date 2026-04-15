import gradio as gr
import copy

# -----------------------------------------
# Default playlist data
# -----------------------------------------
DEFAULT_ROWS = [
    ["Blinding Lights", "The Weeknd", 88, 200],
    ["Good Days", "SZA", 65, 279],
    ["Levitating", "Dua Lipa", 92, 203],
    ["Someone Like You", "Adele", 35, 285],
    ["As It Was", "Harry Styles", 72, 167],
    ["Stay", "The Kid LAROI", 85, 141],
    ["Sunflower", "Post Malone", 78, 158],
    ["Yellow", "Coldplay", 40, 269],
]

# -----------------------------------------
# Clean and validate table rows
# -----------------------------------------
def clean_rows(rows):
    songs = []

    if hasattr(rows, "values"):
        rows = rows.values.tolist()

    if rows is None or len(rows) == 0:
        raise ValueError("Please enter at least one song.")

    for i, row in enumerate(rows, start=1):
        if row is None or len(row) < 4:
            raise ValueError(f"Row {i} is incomplete.")

        title = str(row[0]).strip() if row[0] is not None else ""
        artist = str(row[1]).strip() if row[1] is not None else ""

        if title == "" or artist == "":
            raise ValueError(f"Row {i} must have a title and artist.")

        try:
            energy = int(float(row[2]))
            duration = int(float(row[3]))
        except Exception:
            raise ValueError(f"Row {i} must have numeric energy and duration.")

        if not (0 <= energy <= 100):
            raise ValueError(f"Row {i}: energy must be between 0 and 100.")

        if duration <= 0:
            raise ValueError(f"Row {i}: duration must be greater than 0.")

        songs.append(
            {
                "title": title,
                "artist": artist,
                "energy": energy,
                "duration": duration,
            }
        )

    return songs

# -----------------------------------------
# Format playlist nicely
# -----------------------------------------
def playlist_text(songs, sort_key=None):
    if not songs:
        return "No songs to display."

    lines = []
    if sort_key:
        lines.append(f"Sorted by {sort_key}:\n")

    for i, song in enumerate(songs, start=1):
        lines.append(
            f"{i}. {song['title']} by {song['artist']} "
            f"(Energy: {song['energy']}, Duration: {song['duration']} sec)"
        )

    return "\n".join(lines)

# -----------------------------------------
# Make simple bar chart text
# -----------------------------------------
def make_bar(value, max_value, width=24):
    if max_value <= 0:
        return ""
    filled = max(1, int((value / max_value) * width))
    return "█" * filled

# -----------------------------------------
# Render one visual step
# -----------------------------------------
def render_visual_step(step, sort_key):
    songs = step["songs"]
    pivot_index = step.get("pivot_index")
    compare_index = step.get("compare_index")
    swap_indices = step.get("swap_indices", [])
    low = step.get("low")
    high = step.get("high")

    if not songs:
        return "No songs available."

    values = [song[sort_key] for song in songs]
    max_value = max(values) if values else 1

    lines = []
    lines.append("Tags: [ACT]=active subarray  [PIV]=pivot  [CMP]=compare  [SWP]=swap")
    lines.append("")
    lines.append(f"{'TAG':<16}{'TITLE':<22}{sort_key.upper():<10}BAR")
    lines.append("-" * 70)

    for i, song in enumerate(songs):
        tags = []

        if low is not None and high is not None and low <= i <= high:
            tags.append("ACT")
        if i == pivot_index:
            tags.append("PIV")
        if i == compare_index:
            tags.append("CMP")
        if i in swap_indices:
            tags.append("SWP")

        tag_text = ",".join(tags) if tags else "-"
        title = song["title"][:20]
        value = song[sort_key]
        bar = make_bar(value, max_value)

        lines.append(f"{tag_text:<16}{title:<22}{str(value):<10}{bar}")

    return "```text\n" + "\n".join(lines) + "\n```"

# -----------------------------------------
# Store one recorded step
# -----------------------------------------
def record_step(
    steps,
    songs,
    message,
    low=None,
    high=None,
    pivot_index=None,
    compare_index=None,
    swap_indices=None,
    done=False,
):
    if swap_indices is None:
        swap_indices = []

    steps.append(
        {
            "songs": copy.deepcopy(songs),
            "message": message,
            "low": low,
            "high": high,
            "pivot_index": pivot_index,
            "compare_index": compare_index,
            "swap_indices": swap_indices,
            "done": done,
        }
    )

# -----------------------------------------
# Quick Sort with recorded steps
# -----------------------------------------
def quick_sort_steps(songs, sort_key):
    arr = copy.deepcopy(songs)
    steps = []

    if not arr:
        record_step(steps, arr, "No songs to sort.", done=True)
        return steps, arr

    record_step(
        steps,
        arr,
        "Starting Quick Sort.",
        low=0,
        high=len(arr) - 1,
    )

    def partition(low, high):
        pivot = arr[high]
        pivot_value = pivot[sort_key]
        i = low - 1

        record_step(
            steps,
            arr,
            f"Choose pivot: {pivot['title']} ({sort_key}={pivot_value})",
            low=low,
            high=high,
            pivot_index=high,
        )

        for j in range(low, high):
            record_step(
                steps,
                arr,
                f"Compare {arr[j]['title']} ({sort_key}={arr[j][sort_key]}) with pivot {pivot['title']} ({sort_key}={pivot_value})",
                low=low,
                high=high,
                pivot_index=high,
                compare_index=j,
            )

            if arr[j][sort_key] <= pivot_value:
                i += 1

                if i != j:
                    left_name = arr[i]["title"]
                    right_name = arr[j]["title"]
                    arr[i], arr[j] = arr[j], arr[i]

                    record_step(
                        steps,
                        arr,
                        f"Swap {left_name} and {right_name}.",
                        low=low,
                        high=high,
                        pivot_index=high,
                        compare_index=j,
                        swap_indices=[i, j],
                    )
                else:
                    record_step(
                        steps,
                        arr,
                        f"{arr[j]['title']} stays on the left side.",
                        low=low,
                        high=high,
                        pivot_index=high,
                        compare_index=j,
                        swap_indices=[j],
                    )

        pivot_name = arr[high]["title"]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]

        record_step(
            steps,
            arr,
            f"Move pivot {pivot_name} into its final position.",
            low=low,
            high=high,
            pivot_index=i + 1,
            swap_indices=[i + 1, high],
        )

        return i + 1

    def quick_sort(low, high):
        if low < high:
            p = partition(low, high)
            quick_sort(low, p - 1)
            quick_sort(p + 1, high)
        elif low == high:
            record_step(
                steps,
                arr,
                f"Single song subarray: {arr[low]['title']} is already in place.",
                low=low,
                high=high,
            )

    quick_sort(0, len(arr) - 1)

    record_step(
        steps,
        arr,
        "Sorting complete. Playlist ranked from smallest to largest by the selected key.",
        done=True,
    )

    return steps, arr

# -----------------------------------------
# Show one step
# -----------------------------------------
def show_step(step_index, steps, sort_key):
    if not steps:
        return "", "Run Quick Sort first.", ""

    step_index = max(0, min(int(step_index), len(steps) - 1))
    step = steps[step_index]

    visual = render_visual_step(step, sort_key)
    message = f"Step {step_index + 1}/{len(steps)}\n\n{step['message']}"

    if step.get("done"):
        ranked = playlist_text(step["songs"], sort_key)
    else:
        ranked = playlist_text(step["songs"])

    return visual, message, ranked

# -----------------------------------------
# Main run button
# -----------------------------------------
def run_sort(rows, sort_key):
    try:
        songs = clean_rows(rows)
        steps, final_sorted = quick_sort_steps(songs, sort_key)

        visual, message, ranked = show_step(0, steps, sort_key)

        return (
            steps,
            0,
            gr.update(maximum=len(steps) - 1, value=0),
            visual,
            message,
            playlist_text(final_sorted, sort_key),
            "Sorting steps recorded successfully.",
            gr.update(active=False),
        )

    except Exception as e:
        return (
            [],
            0,
            gr.update(maximum=0, value=0),
            "",
            f"Error: {str(e)}",
            "",
            "Fix the input and try again.",
            gr.update(active=False),
        )

# -----------------------------------------
# Slider change
# -----------------------------------------
def step_from_slider(step_index, steps, sort_key):
    visual, message, ranked = show_step(step_index, steps, sort_key)
    return int(step_index), visual, message, ranked

# -----------------------------------------
# Next step
# -----------------------------------------
def next_step(step_index, steps, sort_key):
    if not steps:
        return 0, gr.update(value=0), "", "Run Quick Sort first.", ""

    step_index = min(step_index + 1, len(steps) - 1)
    visual, message, ranked = show_step(step_index, steps, sort_key)
    return step_index, gr.update(value=step_index), visual, message, ranked

# -----------------------------------------
# Previous step
# -----------------------------------------
def prev_step(step_index, steps, sort_key):
    if not steps:
        return 0, gr.update(value=0), "", "Run Quick Sort first.", ""

    step_index = max(step_index - 1, 0)
    visual, message, ranked = show_step(step_index, steps, sort_key)
    return step_index, gr.update(value=step_index), visual, message, ranked

# -----------------------------------------
# Reset to first step
# -----------------------------------------
def reset_demo(steps, sort_key):
    if not steps:
        return 0, gr.update(value=0), "", "Run Quick Sort first.", "", gr.update(active=False)

    visual, message, ranked = show_step(0, steps, sort_key)
    return 0, gr.update(value=0), visual, message, ranked, gr.update(active=False)

# -----------------------------------------
# Start autoplay
# -----------------------------------------
def start_autoplay(steps):
    if not steps:
        return gr.update(active=False)
    return gr.update(active=True)

# -----------------------------------------
# Pause autoplay
# -----------------------------------------
def pause_autoplay():
    return gr.update(active=False)

# -----------------------------------------
# Timer tick for autoplay
# -----------------------------------------
def autoplay_step(step_index, steps, sort_key):
    if not steps:
        return 0, gr.update(value=0), "", "Run Quick Sort first.", "", gr.update(active=False)

    if step_index >= len(steps) - 1:
        visual, message, ranked = show_step(step_index, steps, sort_key)
        return (
            step_index,
            gr.update(value=step_index),
            visual,
            message,
            ranked,
            gr.update(active=False),
        )

    step_index += 1
    visual, message, ranked = show_step(step_index, steps, sort_key)

    active = step_index < len(steps) - 1

    return (
        step_index,
        gr.update(value=step_index),
        visual,
        message,
        ranked,
        gr.update(active=active),
    )

# -----------------------------------------
# Gradio UI
# -----------------------------------------
with gr.Blocks() as demo:
    gr.Markdown("# Quick Sort Playlist Visualiser")
    gr.Markdown(
        "Use Quick Sort to rank songs by energy or duration, and move through the sorting process step by step."
    )

    steps_state = gr.State([])
    current_step_state = gr.State(0)

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## Playlist Data")

            playlist_df = gr.Dataframe(
                headers=["Title", "Artist", "Energy", "Duration"],
                datatype=["str", "str", "number", "number"],
                value=DEFAULT_ROWS,
                row_count=(8, "dynamic"),
                col_count=(4, "fixed"),
                interactive=True,
                label="Enter or edit songs",
            )

            sort_key = gr.Dropdown(
                choices=["energy", "duration"],
                value="energy",
                label="Choose Sorting Key",
            )

            run_button = gr.Button("Run Quick Sort", variant="primary")

            status_box = gr.Textbox(
                label="Status",
                lines=2,
                interactive=False,
            )

        with gr.Column(scale=2):
            gr.Markdown("## Visualisation")

            visual_output = gr.Markdown()

            current_step_box = gr.Textbox(
                label="Current Step",
                lines=5,
                interactive=False,
            )

            final_output = gr.Textbox(
                label="Final Ranked Playlist",
                lines=12,
                interactive=False,
            )

    step_slider = gr.Slider(
        minimum=0,
        maximum=0,
        value=0,
        step=1,
        label="Step",
    )

    with gr.Row():
        prev_button = gr.Button("Prev")
        next_button = gr.Button("Next")
        autoplay_button = gr.Button("Autoplay")
        pause_button = gr.Button("Pause")
        reset_button = gr.Button("Reset")

    timer = gr.Timer(1.2, active=False)

    run_button.click(
        fn=run_sort,
        inputs=[playlist_df, sort_key],
        outputs=[
            steps_state,
            current_step_state,
            step_slider,
            visual_output,
            current_step_box,
            final_output,
            status_box,
            timer,
        ],
    )

    step_slider.release(
        fn=step_from_slider,
        inputs=[step_slider, steps_state, sort_key],
        outputs=[current_step_state, visual_output, current_step_box, final_output],
    )

    next_button.click(
        fn=next_step,
        inputs=[current_step_state, steps_state, sort_key],
        outputs=[current_step_state, step_slider, visual_output, current_step_box, final_output],
    )

    prev_button.click(
        fn=prev_step,
        inputs=[current_step_state, steps_state, sort_key],
        outputs=[current_step_state, step_slider, visual_output, current_step_box, final_output],
    )

    reset_button.click(
        fn=reset_demo,
        inputs=[steps_state, sort_key],
        outputs=[current_step_state, step_slider, visual_output, current_step_box, final_output, timer],
    )

    autoplay_button.click(
        fn=start_autoplay,
        inputs=[steps_state],
        outputs=[timer],
    )

    pause_button.click(
        fn=pause_autoplay,
        inputs=[],
        outputs=[timer],
    )

    timer.tick(
        fn=autoplay_step,
        inputs=[current_step_state, steps_state, sort_key],
        outputs=[current_step_state, step_slider, visual_output, current_step_box, final_output, timer],
    )

if __name__ == "__main__":
    demo.launch()

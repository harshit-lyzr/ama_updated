import re
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url):
    # Regular expression to capture video ID
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None


def get_transcript(video_id):
    try:
        # Fetch the transcript using the video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        paragraphs = []
        paragraph = ""
        paragraph_start = 0
        paragraph_duration = 0

        for i, entry in enumerate(transcript):
            start_time = entry['start']
            duration = entry['duration']
            text = entry['text']

            # If paragraph is empty, mark start time of this paragraph
            if not paragraph:
                paragraph_start = start_time

            # Add text and update duration
            if len(paragraph) + len(text) + 1 <= 200:
                paragraph += " " + text
                paragraph_duration = (start_time + duration) - paragraph_start
            else:
                # Append the paragraph to result with the start and duration fields
                paragraphs.append({
                    'text': paragraph.strip(),
                    'start': paragraph_start,
                    'duration': paragraph_duration
                })
                # Start a new paragraph
                paragraph = text
                paragraph_start = start_time
                paragraph_duration = duration

        # Add the last paragraph
        if paragraph:
            paragraphs.append({
                'text': paragraph.strip(),
                'start': paragraph_start,
                'duration': paragraph_duration
            })
        print(paragraphs)
        return paragraphs

    except Exception as e:
        return str(e)


# Function to generate YouTube URL starting at a specific time given in 'seconds:milliseconds' format
def generate_youtube_url(video_id, time_str):
    # Split the input string into seconds and milliseconds using the colon
    seconds_str, milliseconds_str = time_str.split(".")

    # Convert the string values to integers
    seconds = int(seconds_str)
    milliseconds = int(milliseconds_str)

    # Convert milliseconds to seconds and add to total time
    total_time = seconds + (milliseconds / 1000)

    # Create YouTube URL with 't' parameter (rounded to 3 decimal places for precision)
    youtube_url = f"https://www.youtube.com/watch?v={video_id}&t={total_time:.3f}s"

    return youtube_url

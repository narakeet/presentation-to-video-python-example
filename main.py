import os
from narakeet_api import PresentationToVideoAPI

#######################################################################
# SECTION 1: Configuration
#
#
# change this to use an API key that is configured somehow differently

api_key = os.environ['NARAKEET_API_KEY']

if not api_key:
    sys.exit("Error: NARAKEET_API_KEY is not set or is empty.")

# change this to localize the warning messages

warning_messages = {
    "no-embedded-fonts": "Fonts are not embedded in this document, the output might look different than on your screen. Save the presentation with fonts embedded if possible.",
    "missing-fonts": "Some fonts are missing from the document,  the output might look different than on your screen.",
    "too-many-slides": "This presentation has more slides than your allowed account limit. Some slides will not be processed.",
    "invalid-audio": "The slide contains an invalid audio file or an unsupported audio format, it will not be included in the result.",
    "audio-too-long": "The slide contains an audio that exceeds your account limit for embedded audios.",
    "linked-audio": "This slide is linking to an external audio that is not included in the presentation file. Embed audio files instead of linking them.",
    "invalid-video": "The slide contains an invalid video file or an unsupported video format, it will not be included in the result.",
    "video-too-long": "The slide contains a video that exceeds your account limit for embedded audios.",
    "linked-video": "This slide is linking to an external video that is not included in the presentation file. Embed video videos instead of linking them",
    "static-slide-only": "This slide has no audio or narration. It will only show a static image.",
    "animated": "This slide is using Powerpoint animations, which are not currently supported",
    "transition": "This slide is using Powerpoint transitions which are not currently supported."
};

# change this to use a different file somewhere else on your file system!

def get_pptx_file_path():
    pptx_file = os.getenv("PPTX_FILE")
    if not pptx_file:
        sys.exit("Error: PPTX_FILE key not set or is empty.")
    return os.path.realpath(os.path.join(os.path.dirname(__file__), pptx_file))

# change this to configure the video build

def get_video_settings():
    return {
        "voice": "victoria",
        "size": "720p",
        "background": "corporate-1 fade-in 0.4"
    }


# change this to do something smarter with percent, message and thumbnail
def show_progress(progress_data):
    print(progress_data)

# change this to somehow better display import warnings, and allow a user to stop the process
# and re-upload the powerpoint

def show_warnings(warnings):
    for index, warning in enumerate(warnings):
        warning_type = warning["type"]
        slide = warning["scene"] + 1
        detail = warning.get("detail", "")
        message = warning_messages.get(warning_type, warning_type)
        print(f"Warning in slide #{slide}: {message} {detail}")

#######################################################################
#
# SECTION 2: Build process
#

api = PresentationToVideoAPI(api_key)

# step 1: upload the pptx to Narakeet

pptx_path = get_pptx_file_path()

upload_token = api.request_upload_token()

api.upload_file(upload_token, pptx_path)

# step 2: kick-off a conversion task to import the PPTX into Narakeet video format

conversion_task = api.request_conversion(upload_token)

conversion_task_result = api.poll_until_finished(conversion_task['statusUrl'], show_progress)

if conversion_task_result["succeeded"]:
    if "warnings" in conversion_task_result and isinstance(conversion_task_result["warnings"], list):
        show_warnings(conversion_task_result["warnings"])
else:
    raise Exception(f"there was a problem converting the presentation: {conversion_task_result['message']}")

# step 3: start a build task using the imported presentation
# and wait for it to finish

build_settings = {
    "description": pptx_path,
    "settings": get_video_settings()
}

task = api.request_build_task(upload_token, conversion_task, build_settings)

task_result = api.poll_until_finished(task['statusUrl'], show_progress)

# grab the result file
if task_result['succeeded']:
    file = api.download_to_temp_file(task_result['result'])
    print(f'downloaded to {file}')
else:
    raise Exception(task_result['message'])


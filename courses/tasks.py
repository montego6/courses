from celery import shared_task
from moviepy.editor import VideoFileClip
from ..core.consts import LESSON_VIDEO_FPS


@shared_task
def change_uploaded_video_fps(filename):
    lesson_clip = VideoFileClip(filename)
    new_clip = lesson_clip.set_fps(LESSON_VIDEO_FPS)
    new_clip.write_videofile(filename)
    lesson_clip.close()
    new_clip.close()

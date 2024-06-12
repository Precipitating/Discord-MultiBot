import discord
import helper_functions
from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.audio.AudioClip import CompositeAudioClip
import numpy as np
import os


def remove_audio(videoPath: str, outputPath: str):
    finalVid = VideoFileClip(videoPath).without_audio()
    finalVid.write_videofile(outputPath, fps=60)


def bgm_add(videoPath: str, audioPath: str, outputPath: str):
    videoFile = VideoFileClip(videoPath)
    audioFile = AudioFileClip(audioPath)
    # loop audio to video length
    loopedAudio = audio_loop(audioFile, duration=videoFile.duration)
    # combine both tracks
    addedAudio = CompositeAudioClip([videoFile.audio, loopedAudio])
    # set to source video
    final = videoFile.set_audio(addedAudio)
    # save to disk
    final.write_videofile(outputPath, fps=60)


def extract_audio(filePath: str, outputPath: str):
    mp3Format = outputPath.replace(helper_functions.extract_file_format(outputPath), "")
    mp3Format += ".mp3"
    print(mp3Format)
    VideoFileClip(filePath).audio.write_audiofile(mp3Format)

    return mp3Format


def audio_concatenate(clips):
    durations = [c.duration for c in clips]
    tt = np.cumsum([0] + durations)  # start times, and end time.
    newclips = [c.set_start(t) for c, t in zip(clips, tt)]
    return CompositeAudioClip(newclips).set_duration(tt[-1])


def audio_loop(clip, duration):
    nloops = int(duration / clip.duration) + 1
    return audio_concatenate(nloops * [clip]).set_duration(duration)

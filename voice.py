import discord
from discord.ext import voice_recv, tasks
from typing import Final
import os

AUDIO_SAVE_PATH: Final[str] = "voiceRecordOutput/output.mp3"


async def start_voice_recording(interaction: discord.Interaction):
    vc = await interaction.user.voice.channel.connect(cls=voice_recv.VoiceRecvClient)
    vc.listen(voice_recv.SilenceGeneratorSink(voice_recv.FFmpegSink(filename=AUDIO_SAVE_PATH)))


async def stop_voice_recording(interaction: discord.Interaction):
    await interaction.guild.voice_client.disconnect()


# bot auto leaves if it is recording and user who sent cmd left channel
@tasks.loop(seconds=30.0)
async def auto_leave_vc(interaction: discord.Interaction):
    print("works")
    if interaction.guild.voice_client:
        if not interaction.user.voice:
            await stop_voice_recording(interaction)
            os.remove(AUDIO_SAVE_PATH)
            auto_leave_vc.stop()

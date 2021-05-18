__name__ = "audioplayer"
__package__ = "audioplayer"
__version__ = "0.6"

from platform import system

if system() == 'Windows':
    from tocadordemusicas.libs.audioplayer.audioplayer_windows import AudioPlayerWindows as AudioPlayer
elif system() == 'Darwin':
    from tocadordemusicas.libs.audioplayer.audioplayer_macos import AudioPlayerMacOS as AudioPlayer
else:
    from tocadordemusicas.libs.audioplayer.audioplayer_linux import AudioPlayerLinux as AudioPlayer


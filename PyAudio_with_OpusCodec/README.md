# Audio streaming example using PyAudio + opuslib
- Change self._sendingPeer_ip, self._sendingPeer_port, self._receivingPeer_ip and self._receivingPeer_port accordingly
- Note: setting these ip to 'localhost' will prevent socket to bind to your external/LAN IP
- Use self._mode = "loop" to stream audio to own host. In loop mode it will work if you set the ip's to 'localhost'
- Run this script with self._mode = "sender" in the computer that will stream the audio and with self._mode = "receiver" on computer that will receive the stream. Set IP's accordingly

- This script uses version 3.0.1 of opuslib python binds of https://github.com/OnBeep/opuslib
- https://wiki.xiph.org/index.php?title=Opus_Recommended_Settings&mobileaction=toggle_view_desktop

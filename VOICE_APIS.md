# Free / low-cost voice API options

## Speech-to-text
- Browser Web Speech API: no API key; availability depends on browser/OS.
- Local Whisper: no API key and no hosted quota; requires local model/runtime.
- Hosted APIs can be plugged in later through environment variables.

## Text-to-speech
- FreeTTS documents a free API key tier, with rate and character limits.
- Keep API keys in local environment variables, never in GitHub source.

## Jarvis integration rule
The voice layer should be replaceable. Jarvis should continue to work with a local speech engine when an API is unavailable.

No secret keys are committed to this repository.

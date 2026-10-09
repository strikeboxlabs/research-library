---
name: text2wave
description: Produce reproducible speech test audio with Festival text2wave. Use when a speech-input application needs WAV fixtures and synthesis, transcription or shell quoting must be distinguished.
---

# Festival speech fixtures

`text2wave` synthesizes speech from text; it does not recognize speech or guarantee how a downstream recognizer transcribes it. Inspect `text2wave -help` and the installed Festival voices. Missing voice/data packages can prevent synthesis even when the executable exists.

Define `text_file` as an existing UTF-8/plain-text fixture compatible with the installed voice, `wav_file` as a fresh output path, and `sample_rate` as the receiver's documented rate in Hz:

~~~bash
text2wave -otype riff -F "$sample_rate" -o "$wav_file" "$text_file"
~~~

For one already-defined text value, pass it as data:

~~~bash
printf '%s\n' "$utterance" | text2wave -otype riff -o "$wav_file"
~~~

Do not construct an `echo ... | text2wave` shell command by interpolating arbitrary text into code. Apostrophes, dollar signs and shell metacharacters belong in the text input, not an evaluated command string. Explicit `-o` also avoids mixing binary stdout with terminal/log output.

Check exit diagnostics, nonempty output, actual format/sample rate and duration; listen to the fixture when pronunciation matters. `-F` resamples output, and `-scale` changes volume; neither guarantees recognition quality. Punctuation, numbers and abbreviations are interpreted by the voice's text normalization, so compare the receiving application's transcript with the intended phrase before attributing application behavior to it.

Keep the exact text, voice/configuration and resulting audio together for reproducibility. The script loads Festival initialization and the user's `.festivalrc`; `-eval` runs Scheme code rather than selecting inert metadata. Use only intentional local voice/configuration expressions there.

Documentation reviewed 2026-10-09; Linux execution untested. Case: AI pp. 5–8. Source: [Festival text2wave implementation and help](https://github.com/festvox/festival/blob/master/examples/text2wave.sh).

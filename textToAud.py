import os
from elevenlabs.client import ElevenLabs

client = ElevenLabs(api_key="sk_fc5ba4406996ce6a52f6aa532fed97e04a2feb96dd919744")
def text_to_speech_file(text: str, folder: str, output_file: str) -> str:
    response = client.text_to_speech.convert(
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        text=text,
        output_format="mp3_22050_32"
    )

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{output_file}: A new audio file was saved successfully!")
    return output_file
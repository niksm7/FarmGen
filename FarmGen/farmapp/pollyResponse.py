import boto3
from farmapp.intialize import aws_polly_voice_data
from django.conf import settings
import time
import os


def getPollyResponse(given_text, given_language="English (US)"):
    polly_client = boto3.client('polly', region_name='us-east-1')
    given_text = given_text.replace("<br>", "")
    voice_id = aws_polly_voice_data.get(given_language).get("VoiceName")
    response = polly_client.synthesize_speech(VoiceId=voice_id,
                    OutputFormat='mp3', 
                    Text = given_text,
                    Engine = 'neural')
    time_stamp = int(time.time())
    file_name = "audio_file_" + str(time_stamp) + ".mp3"
    ouput_audio_path = os.path.join(settings.MEDIA_ROOT,"audiofiles",file_name)
    ouput_audio_file = open(ouput_audio_path,'wb')
    ouput_audio_file.write(response['AudioStream'].read())
    ouput_audio_file.close()
    return file_name
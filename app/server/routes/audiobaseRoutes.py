from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    add_audio,
    delete_audio,
    retrieve_audio,
    retrieve_audios,
    update_audio,
)
from app.server.models.audiobaseModel import (
    ErrorResponseModel,
    ResponseModel,
    Song,
    Podcast,
    AudioBook,
    AudioFileType,
    audioFileMetadata
)

router = APIRouter()

#Create
@router.post("/", response_description="Data related to audio files added successfully into the database")
# x = isinstance(audio, Song)
# y = isinstance(audio, Podcast)
# z = isinstance(audio, AudioBook)
# if x:
async def add_audio_data(audio: Song = Body(...)):
    audio = jsonable_encoder(audio)
    new_audio = await add_audio(audio)
    return ResponseModel(new_audio, "Song added successfully.")
# elif y:
async def add_audio_data(audio: Podcast = Body(...)):
    audio = jsonable_encoder(audio)
    new_audio = await add_audio(audio)
    return ResponseModel(new_audio, "Podcast added successfully.")
# elif z:
async def add_audio_data(audio: AudioBook = Body(...)):
    audio = jsonable_encoder(audio)
    new_audio = await add_audio(audio)
    return ResponseModel(new_audio, "AudioBook added successfully.")


#Delete
@router.delete("AudioFileType/{id}", response_description="Audio data deleted from the database")
async def delete_audio_data(id: int):
    deleted_audio = await delete_audio(id)
    if deleted_audio:
        return ResponseModel(
            "Audio with ID: {} removed".format(id), "Audio deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "audio with id {0} doesn't exist".format(id)
    )

#Update
@router.put("AudioFileType/{id}")
async def update_audio_data(id: int, req: AudioFileType = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_audio = await update_audio(id, req)
    if updated_audio:
        return ResponseModel(
            "Audio with ID: {} file update is successful".format(id),
            "Audio file updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the audio data.",
    )

#Get
@router.get("/", response_description="Audios retrieved")
async def get_audios():
    audios = await retrieve_audios()
    if audios:
        return ResponseModel(audios, "Audios retrieved successfully")
    return ResponseModel(audios, "Empty list returned")


@router.get("audioFileType/{id}", response_description=" audio for particular file types data retrieved")
async def get_audio_data(id):
    audio = await retrieve_audio(id)
    if audio:
        return ResponseModel(audio, "audio for particular file types data retrieved")
    return ErrorResponseModel("An error occurred.", 404, "Audio data doesn't exist.")
    
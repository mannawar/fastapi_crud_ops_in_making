from bson.objectid import ObjectId
import motor.motor_asyncio

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.audiobase

audio_collection = database.get_collection("audio_collections")

#helper functions
def song_helper(Song) -> dict:
    return {
        "id": int(Song["_id"]),
        "name": Song["name"],
        "duration": int(Song["duration"]),
        "uploaded_time": Song["uploaded_time"]
    },

def podcast_helper(Podcast) -> dict:
    return {
        "id": int(Podcast["_id"]),
        "name": Podcast["name"],
        "duration": int(Podcast["duration"]),
        "uploaded_time": Podcast["uploaded_time"],
        "host": str(Podcast["host"]),
        "participants": str(Podcast["participants"]),
    },
    
def audiobook_helper(AudioBook) -> dict:
    return {
        "id": int(AudioBook["_id"]),
        "title": str(AudioBook["title"]),
        "author": str(AudioBook["author"]),
        "narrator": str(AudioBook["narrator"]),
        "duration": int(AudioBook["duration"]),
        "uploaded_time": datetime(AudioBook["uploaded_time"]),
    },

# Retrieve all audios of a particular file type
async def retrieve_audios(audio):
    audios = []
    async for audio in audio_collections.find():
        if isinstance(audio, Song):
            audios.append(song_helper(audio))
        elif isinstance(audio, Podcast):
            audios.append(podcast_helper(audio))
        else:
            audios.append(audiobook_helper(audio))
    return audios

# Add a new field
async def add_audio(audio_data: dict) -> dict:
    if isinstance(audio, Song):
        audio = await audio_collection.insert_one(audio_data)
        new_audio = await audio_collection.find_one({"_id": audio.inserted_id})
        return song_helper(new_audio)
    elif isinstance(audio, Podcast):
        audio = await audio_collection.insert_one(audio_data)
        new_audio = await audio_collection.find_one({"_id": audio.inserted_id})
        return podcast_helper(new_audio)
    else:
        audio = await audio_collection.insert_one(audio_data)
        new_audio = await audio_collection.find_one({"_id": audio.inserted_id})
        return audiobook_helper(new_audio)

# Retrieve an audio with a matching ID
async def retrieve_audio(id: int) -> dict:
    audio = await audio_collection.find_one({"_id": ObjectId(id)})
    if isinstance(audio, Song):
        return song_helper(audio)
    elif isinstance(audio, Podcast):
        return podcast_helper(audio)
    else:
        return audiobook_helper(audio)

#update audio with a matching id
async def update_audio(id: int, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    audio = await audio_collection.find_one({"_id": ObjectId(id)})
    if isinstance(audio, Song):
        updated_audio = await audio_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_audio:
            return True
        return False
    elif isinstance(audio, Podcast):
        updated_audio = await audio_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_audio:
            return True
        return False
    else:
        updated_audio = await audio_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_audio:
            return True
        return False

# Delete an audio from the database
async def delete_audio(id: int):
    audio = await audio_collection.find_one({"_id": ObjectId(id)})
    if isinstance(audio, Song):
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True
    elif isinstance(audio, Podcast):
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True
    else:
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True
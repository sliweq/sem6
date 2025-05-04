
export class Chat{
    constructor(id, name, owner){
        this.id = id
        this.name = name
        this.messages = []
        this.owner = owner
        this.created_at = new Date()
        this.users = 0
    }
}

export class Message{
    constructor(sender,sender_id ,text, picture = null, sound = null){
        this.sound = sound
        this.sender_id = sender_id
        this.sender = sender
        this.text = text
        this.picture = picture
        this.time = new Date()
    }
}


package com.amessage.data

enum class MessageStatus { SENDING, DELIVERED, READ }
enum class TapbackType(val symbol: String) {
    HEART("❤️"), LIKE("👍"), DISLIKE("👎"), LAUGH("😂"), EXCLAIM("‼️"), QUESTION("❓")
}
data class Tapback(val type: TapbackType, val sender: String)
data class Message(
    val id: String,
    val text: String,
    val sender: String,
    val isFromMe: Boolean,
    val timestamp: Long = System.currentTimeMillis(),
    val status: MessageStatus = MessageStatus.DELIVERED,
    val tapbacks: List<Tapback> = emptyList()
)
data class Conversation(
    val id: String,
    val participantHandle: String,
    val displayName: String,
    val lastMessage: String
)

package com.amessage

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.runtime.*
import com.amessage.data.Conversation
import com.amessage.service.APNsService
import com.amessage.ui.screens.ChatScreen
import com.amessage.ui.screens.ConversationListScreen
import com.amessage.ui.theme.AMessageTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        startService(Intent(this, APNsService::class.java))
        setContent {
            AMessageTheme {
                var selectedConversation by remember { mutableStateOf<Conversation?>(null) }
                if (selectedConversation != null) {
                    ChatScreen(
                        contactName = selectedConversation!!.displayName,
                        contactHandle = selectedConversation!!.participantHandle,
                        onBack = { selectedConversation = null }
                    )
                } else {
                    ConversationListScreen(
                        onSelectConversation = { conv -> selectedConversation = conv },
                        onOpenSettings = {}
                    )
                }
            }
        }
    }
}

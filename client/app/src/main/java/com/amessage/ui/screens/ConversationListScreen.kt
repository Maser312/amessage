package com.amessage.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.amessage.data.Conversation
import com.amessage.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ConversationListScreen(onSelectConversation: (Conversation) -> Unit, onOpenSettings: () -> Unit) {
    val isDark = isSystemInDarkTheme()
    val conversations = listOf(
        Conversation("1", "alice@icloud.com", "Alice (iPhone 15 Pro)", "Blue bubbles on Android?!"),
        Conversation("2", "bob@apple.com", "Bob Smith", "Connected to APNs courier push gateway")
    )

    Scaffold(
        topBar = {
            LargeTopAppBar(title = { Text("Messages", fontWeight = FontWeight.Bold) })
        }
    ) { p ->
        LazyColumn(modifier = Modifier.fillMaxSize().padding(p)) {
            items(conversations) { c ->
                Row(modifier = Modifier.fillMaxWidth().clickable { onSelectConversation(c) }.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                    Box(modifier = Modifier.size(48.dp).clip(CircleShape).background(Color(0xFF8E8E93)), contentAlignment = Alignment.Center) {
                        Text(c.displayName.first().toString(), color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                    }
                    Spacer(modifier = Modifier.width(14.dp))
                    Column {
                        Text(c.displayName, fontWeight = FontWeight.SemiBold, fontSize = 16.sp)
                        Text(c.lastMessage, color = SecondaryGray, fontSize = 14.sp)
                    }
                }
            }
        }
    }
}

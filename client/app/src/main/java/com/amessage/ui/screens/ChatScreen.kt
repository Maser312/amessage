package com.amessage.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.ArrowUpward
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.amessage.data.Message
import com.amessage.ui.components.MessageBubble
import com.amessage.ui.theme.*
import java.util.UUID

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ChatScreen(contactName: String, contactHandle: String, onBack: () -> Unit) {
    var text by remember { mutableStateOf("") }
    val isDark = isSystemInDarkTheme()
    val messages = remember {
        mutableStateListOf(
            Message("1", "Hey! Blue bubbles on Android?!", contactHandle, false),
            Message("2", "Yes! AMessage with native iMessage reverse engineering 🍏", "me", true)
        )
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(contactName, fontSize = 17.sp, fontWeight = FontWeight.SemiBold) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back", tint = iMessageBlue)
                    }
                }
            )
        },
        bottomBar = {
            Row(modifier = Modifier.fillMaxWidth().imePadding().padding(8.dp), verticalAlignment = Alignment.CenterVertically) {
                Box(modifier = Modifier.weight(1f).clip(RoundedCornerShape(20.dp)).background(if (isDark) Color(0xFF2C2C2E) else Color.White).padding(12.dp)) {
                    if (text.isEmpty()) Text("iMessage", color = SecondaryGray)
                    BasicTextField(value = text, onValueChange = { text = it }, textStyle = TextStyle(color = if (isDark) Color.White else Color.Black, fontSize = 16.sp), modifier = Modifier.fillMaxWidth())
                }
                Spacer(modifier = Modifier.width(6.dp))
                IconButton(onClick = {
                    if (text.isNotBlank()) {
                        messages.add(Message(UUID.randomUUID().toString(), text.trim(), "me", true))
                        text = ""
                    }
                }) {
                    Box(modifier = Modifier.size(32.dp).clip(CircleShape).background(iMessageBlue), contentAlignment = Alignment.Center) {
                        Icon(Icons.Default.ArrowUpward, contentDescription = "Send", tint = Color.White)
                    }
                }
            }
        }
    ) { p ->
        LazyColumn(modifier = Modifier.fillMaxSize().padding(p)) {
            items(messages) { msg ->
                MessageBubble(message = msg, showStatus = msg == messages.lastOrNull { it.isFromMe })
            }
        }
    }
}

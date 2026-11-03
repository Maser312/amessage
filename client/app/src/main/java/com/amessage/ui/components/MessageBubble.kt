package com.amessage.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.amessage.data.Message
import com.amessage.ui.theme.*

@Composable
fun MessageBubble(message: Message, showStatus: Boolean = false, onLongPress: () -> Unit = {}) {
    val isDark = isSystemInDarkTheme()
    val bg = if (message.isFromMe) iMessageBlue else (if (isDark) iMessageIncomingDark else iMessageIncomingLight)
    val textCol = if (message.isFromMe || isDark) Color.White else Color.Black
    val shape = if (message.isFromMe) RoundedCornerShape(18.dp, 18.dp, 4.dp, 18.dp) else RoundedCornerShape(18.dp, 18.dp, 18.dp, 4.dp)

    Column(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 2.dp),
        horizontalAlignment = if (message.isFromMe) Alignment.End else Alignment.Start
    ) {
        Box(modifier = Modifier.clip(shape).background(bg).padding(horizontal = 14.dp, vertical = 10.dp)) {
            Text(text = message.text, color = textCol, fontSize = 16.sp)
        }
        if (message.isFromMe && showStatus) {
            Text("Delivered", color = DeliveryGray, fontSize = 11.sp, modifier = Modifier.padding(top = 2.dp, end = 4.dp))
        }
    }
}

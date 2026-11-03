package com.amessage.service

import android.app.*
import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat
import kotlinx.coroutines.*
import javax.net.ssl.SSLSocket
import javax.net.ssl.SSLSocketFactory

class APNsService : Service() {
    private val job = Job()
    private val scope = CoroutineScope(Dispatchers.IO + job)
    private var socket: SSLSocket? = null

    override fun onCreate() {
        super.onCreate()
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel("apns", "APNs", NotificationManager.IMPORTANCE_LOW)
            (getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager).createNotificationChannel(channel)
        }
        val notif = NotificationCompat.Builder(this, "apns")
            .setContentTitle("AMessage Active")
            .setContentText("Connected to Apple APNs")
            .setSmallIcon(android.R.drawable.ic_dialog_email)
            .build()
        startForeground(101, notif)

        scope.launch {
            while (isActive) {
                try {
                    val factory = SSLSocketFactory.getDefault() as SSLSocketFactory
                    socket = factory.createSocket("courier.push.apple.com", 5223) as SSLSocket
                    socket?.startHandshake()
                    while (isActive && socket?.isConnected == true) {
                        delay(120_000)
                    }
                } catch (_: Exception) {
                    delay(5_000)
                }
            }
        }
    }

    override fun onBind(intent: Intent?): IBinder? = null
    override fun onDestroy() {
        super.onDestroy()
        job.cancel()
        try { socket?.close() } catch (_: Exception) {}
    }
}

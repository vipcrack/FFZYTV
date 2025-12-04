package com.example.ffzytv.ui

import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.view.KeyEvent
import androidx.appcompat.app.AppCompatActivity
import com.example.ffzytv.databinding.ActivityPlayerBinding
import com.example.ffzytv.model.VodItem
import com.example.ffzytv.utils.PlayUrlParser
import com.google.android.exoplayer2.ExoPlayer
import com.google.android.exoplayer2.MediaItem

class PlayerActivity : AppCompatActivity() {
    private lateinit var binding: ActivityPlayerBinding
    private lateinit var player: ExoPlayer

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityPlayerBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val vod = intent.getSerializableExtra(EXTRA_VOD) as VodItem
        player = ExoPlayer.Builder(this).build()
        binding.playerView.player = player

        val sources = PlayUrlParser.parse(vod.playFrom, vod.playUrl)
        val ep = (sources.find { it.name.contains("m3u8", ignoreCase = true) } 
                  ?: sources.firstOrNull())?.episodes?.firstOrNull()

        if (ep != null) {
            player.setMediaItem(MediaItem.fromUri(Uri.parse(ep.url)))
            player.prepare()
            player.playWhenReady = true
        }
    }

    override fun onDestroy() {
        player.release()
        super.onDestroy()
    }

    override fun onKeyDown(keyCode: Int, event: KeyEvent?): Boolean {
        if (keyCode == KeyEvent.KEYCODE_BACK) {
            finish()
            return true
        }
        return super.onKeyDown(keyCode, event)
    }

    companion object {
        private const val EXTRA_VOD = "vod"
        fun start(ctx: Context, vod: VodItem) {
            ctx.startActivity(Intent(ctx, PlayerActivity::class.java).putExtra(EXTRA_VOD, vod))
        }
    }
}

package com.ffzy.movie.ui
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.ffzy.movie.model.VodItem
import com.google.android.exoplayer2.ExoPlayer
import com.google.android.exoplayer2.MediaItem
class PlayerActivity : AppCompatActivity() {
    private lateinit var player: ExoPlayer
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        player = ExoPlayer.Builder(this).build()
        setContentView(player.videoSurfaceView)
        val vod = intent.getSerializableExtra("vod") as VodItem
        val url = vod.playUrl.split("\$\$\$").firstOrNull()?.split("#")?.firstOrNull()
            ?.split("\$", limit = 2)?.getOrNull(1)
        if (url != null) {
            player.setMediaItem(MediaItem.fromUri(Uri.parse(url)))
            player.prepare()
            player.playWhenReady = true
        }
    }
    override fun onDestroy() {
        player.release()
        super.onDestroy()
    }
    companion object {
        fun start(ctx: Context, vod: VodItem) {
            ctx.startActivity(Intent(ctx, PlayerActivity::class.java).putExtra("vod", vod))
        }
    }
}

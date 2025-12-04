package com.example.ffzytv.utils

data class PlaySource(val name: String, val episodes: List<Episode>)
data class Episode(val title: String, val url: String)

object PlayUrlParser {
    fun parse(playFrom: String, playUrl: String): List<PlaySource> {
        val froms = playFrom.split("\$\$\$")
        val urls = playUrl.split("\$\$\$")
        return froms.zip(urls) { f, u ->
            PlaySource(f, u.split("#").mapNotNull { e ->
                e.split("\$", limit = 2).takeIf { it.size == 2 }?.let { Episode(it[0], it[1]) }
            })
        }
    }
}

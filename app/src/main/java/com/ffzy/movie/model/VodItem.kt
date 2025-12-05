package com.ffzy.movie.model
import java.io.Serializable
data class VodItem(
    val id: Int,
    val name: String,
    val remarks: String,
    val pic: String,
    val playFrom: String,
    val playUrl: String
) : Serializable

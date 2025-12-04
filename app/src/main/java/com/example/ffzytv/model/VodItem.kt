package com.example.ffzytv.model
import java.io.Serializable
data class VodItem(
    val id: Int,
    val name: String,
    val typeName: String,
    val remarks: String,
    val pic: String,
    val content: String?,
    val actor: String?,
    val year: String?,
    val area: String?,
    val playFrom: String,
    val playUrl: String
) : Serializable

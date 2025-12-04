package com.example.ffzytv.model
import com.google.gson.annotations.SerializedName
data class ApiResponse(
    val code: Int,
    val msg: String,
    val page: Int,
    val pagecount: Int,
    val limit: String,
    val total: Int,
    val list: List<VodItem>
)
